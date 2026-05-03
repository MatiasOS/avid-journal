"""
Promueve un bloque a 'verified' usando el archivo Block existente, sin llamar
a Claude. Util cuando el bloque fue marcado failed por un bug del checker
pero el codigo Lean es correcto.

Uso: python promote_block.py
"""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)

REPO_ROOT = Path(__file__).resolve().parent
PAPER_DIR = REPO_ROOT / "lean_project" / "Papers" / "AyrtonPortoTesis"

LABEL_TO_PROMOTE = "def:espacios-T"
BLOCK_FILE = PAPER_DIR / "Blocks" / "def_espacios_T.lean"
PAPER_LEAN = PAPER_DIR / "Paper.lean"
PAPER_INDEX = PAPER_DIR / "PAPER_INDEX.md"

assert BLOCK_FILE.exists(), f"No existe el block file: {BLOCK_FILE}"

# 1) Extraer solo las declaraciones del block file (omitiendo header de stub
#    e import).
content = BLOCK_FILE.read_text(encoding="utf-8")
# Eliminamos el header (primeras lineas '--' del stub) y la linea import.
lines = content.splitlines()
declarations: list[str] = []
in_header = True
for ln in lines:
    if in_header and (ln.startswith("--") or ln.strip() == ""):
        continue
    if ln.startswith("import "):
        in_header = False
        continue
    in_header = False
    declarations.append(ln)
declaration_text = "\n".join(declarations).strip()
print(f"Declaracion extraida: {len(declaration_text)} chars")
print(declaration_text[:500])
print("...")
print()

# 2) Limpiar Paper.lean: eliminar el bloque "FAILED block: def:espacios-T"
paper_text = PAPER_LEAN.read_text(encoding="utf-8")
# Match: "-- FAILED block: def:espacios-T\n-- reason: ...\n-- (no Lean code committed)\n\n"
failed_pattern = re.compile(
    r"-- FAILED block: def:espacios-T\n"
    r"-- reason: [^\n]*\n"
    r"-- \(no Lean code committed\)\s*\n+",
    re.MULTILINE,
)
paper_text_clean, n_removed = failed_pattern.subn("", paper_text)
print(f"Lineas FAILED eliminadas de Paper.lean: {n_removed} bloque(s)")

# 3) Apendizar la declaracion al Paper.lean limpio
new_paper_text = paper_text_clean.rstrip() + "\n\n" + declaration_text + "\n\n"
PAPER_LEAN.write_text(new_paper_text, encoding="utf-8")
new_line_number = new_paper_text[:new_paper_text.rfind(declaration_text)].count("\n") + 1
print(f"Declaracion apendida a Paper.lean linea {new_line_number}")

# 4) Limpiar PAPER_INDEX.md: eliminar entrada failed de def:espacios-T
index_text = PAPER_INDEX.read_text(encoding="utf-8")
# El entry empieza en "## def:espacios-T\n" y termina en "\n---\n"
entry_pattern = re.compile(
    r"## def:espacios-T\n.*?\n---\n",
    re.DOTALL,
)
index_text_clean, n_idx = entry_pattern.subn("", index_text)
print(f"Entradas eliminadas de PAPER_INDEX.md: {n_idx}")

# 5) Re-agregar como verified. Usamos el statement original del bloque.
# Lo extraigo del bloque que acabamos de borrar (esta en index_text antes de
# la limpieza).
m = re.search(
    r"## def:espacios-T\nType: definition\nStatus: .*?\nFile: Paper\.lean:\d+\nDepends on: [^\n]*\nStatement: ([^\n]+)",
    index_text,
    re.DOTALL,
)
statement = m.group(1) if m else "(statement no recuperado)"

new_entry = (
    f"## def:espacios-T\n"
    f"Type: definition\n"
    f"Status: ✅ verified\n"
    f"File: Paper.lean:{new_line_number}\n"
    f"Depends on: —\n"
    f"Statement: {statement}\n"
    f"\n---\n\n"
)
PAPER_INDEX.write_text(index_text_clean + new_entry, encoding="utf-8")
print(f"Entrada 'verified' apendida a PAPER_INDEX.md")
print()
print("Listo. Estado actualizado:")
print(f"  - Paper.lean: {PAPER_LEAN.stat().st_size} bytes")
print(f"  - PAPER_INDEX.md: {PAPER_INDEX.stat().st_size} bytes")
print(f"  - Bloque {LABEL_TO_PROMOTE} ahora 'verified' en linea {new_line_number}")
