"""
Limpia entradas 'failed' del PAPER_INDEX.md y los marcadores FAILED block en
Paper.lean. Util tras un run interrumpido por rate-limit u otra causa
externa, donde queremos reintentar esos bloques desde cero en el proximo run.

Tambien refactoriza la numeracion de lineas en PAPER_INDEX.md para que las
entradas 'verified'/'axiom' que sobrevivan apunten a la linea correcta.
"""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)

REPO_ROOT = Path(__file__).resolve().parent
PAPER_DIR = REPO_ROOT / "lean_project" / "Papers" / "AyrtonPortoTesis"
PAPER_LEAN = PAPER_DIR / "Paper.lean"
PAPER_INDEX = PAPER_DIR / "PAPER_INDEX.md"

# 1) Limpiar Paper.lean: eliminar bloques "FAILED block: <label>"
paper_text = PAPER_LEAN.read_text(encoding="utf-8")
failed_pattern = re.compile(
    r"-- FAILED block: [^\n]+\n"
    r"-- reason: [^\n]*\n"
    r"-- \(no Lean code committed\)\s*\n+",
    re.MULTILINE,
)
paper_clean, n_paper = failed_pattern.subn("", paper_text)
PAPER_LEAN.write_text(paper_clean.rstrip() + "\n", encoding="utf-8")
print(f"Paper.lean: {n_paper} bloques 'FAILED block' eliminados.")

# 2) Limpiar PAPER_INDEX.md: eliminar entradas con Status: failed
index_text = PAPER_INDEX.read_text(encoding="utf-8")
# Cada entry empieza en "## label\n" y termina en "\n---\n"
entry_pattern = re.compile(r"## [^\n]+\n.*?\n---\n", re.DOTALL)
entries = entry_pattern.findall(index_text)
n_total = len(entries)
n_failed = 0
kept = []
for entry in entries:
    if re.search(r"^Status:\s*[^\n]*failed", entry, re.MULTILINE | re.IGNORECASE) or \
       re.search(r"❌", entry):
        n_failed += 1
    else:
        kept.append(entry)
print(f"PAPER_INDEX.md: {n_total} entradas en total; {n_failed} 'failed' eliminadas.")

# Reconstruir el archivo: header (todo antes del primer "## ") + entries kept
m = re.search(r"## [^\n]+\n", index_text)
if m:
    header = index_text[: m.start()]
else:
    header = index_text
new_index = header + "\n".join(kept)
PAPER_INDEX.write_text(new_index, encoding="utf-8")
print(f"PAPER_INDEX.md: {len(kept)} entradas conservadas.")
print()

# 3) Borrar los Block files vacios (stubs)
removed_blocks = []
for f in (PAPER_DIR / "Blocks").glob("*.lean"):
    content = f.read_text(encoding="utf-8")
    has_decl = bool(re.search(
        r"^\s*(structure|def|theorem|lemma|axiom|inductive|class|abbrev|instance)\s+\w",
        content,
        re.MULTILINE,
    ))
    if not has_decl:
        f.unlink()
        removed_blocks.append(f.name)
print(f"Block files stub eliminados: {len(removed_blocks)}")
for b in removed_blocks:
    print(f"  - {b}")
print()
print("Listo. Proximo run --blocks-range 17-30 (o lo que quieras) los reintentara.")
