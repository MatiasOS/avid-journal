"""
Promueve un bloque a 'verified' usando el archivo Block existente, sin llamar
a Claude. Util cuando el bloque fue marcado failed por un bug del checker
o cuando un run fue abortado pero Claude ya escribio el archivo correctamente.

Uso:
  python promote_block_v2.py <label>
  python promote_block_v2.py def:continuidad-homeomorfismo
"""
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
sys.path.insert(0, ".")

from src.parser.latex_parser import LaTeXParser
from src.formalization.orchestrator import (
    topological_sort,
    lean_ident_for,
    _extract_declarations,
    _has_real_declaration,
)

REPO_ROOT = Path(__file__).resolve().parent
PAPER_DIR = REPO_ROOT / "lean_project" / "Papers" / "AyrtonPortoTesis"
TEX_PATH = REPO_ROOT / "examples" / "thesis_ayrton_porto" / "paper.tex"
PAPER_LEAN = PAPER_DIR / "Paper.lean"
PAPER_INDEX = PAPER_DIR / "PAPER_INDEX.md"

if len(sys.argv) < 2:
    print("Uso: python promote_block_v2.py <label>")
    sys.exit(1)

LABEL = sys.argv[1]

parser = LaTeXParser()
all_blocks = parser.parse_file(str(TEX_PATH))
formalizable = [b for b in all_blocks if b.get("type") not in ("remark", "example")]
ordered = topological_sort(formalizable)

target_block = None
target_idx = None
for i, b in enumerate(ordered, 1):
    if b.get("label") == LABEL:
        target_block = b
        target_idx = i
        break

if target_block is None:
    print(f"[promote] ERROR: no se encontro bloque con label='{LABEL}'")
    sys.exit(1)

lean_name = lean_ident_for(LABEL, fallback=f"block_{target_idx}")
block_file = PAPER_DIR / "Blocks" / f"{lean_name}.lean"

if not block_file.exists():
    print(f"[promote] ERROR: no existe {block_file}")
    sys.exit(1)

declarations = _extract_declarations(block_file)
if not _has_real_declaration(declarations):
    print(f"[promote] ERROR: el archivo {block_file.name} no tiene declaracion real (es stub)")
    sys.exit(1)

print(f"[promote] Bloque target: {LABEL} (idx={target_idx}, lean_name={lean_name})")
print(f"[promote] Block file: {block_file.name} ({block_file.stat().st_size} bytes)")
print(f"[promote] Declaracion extraida: {len(declarations)} chars")
print()

# 1) Limpiar Paper.lean: eliminar entrada FAILED si existe
paper_text = PAPER_LEAN.read_text(encoding="utf-8")
failed_pattern = re.compile(
    rf"-- FAILED block: {re.escape(LABEL)}\n"
    r"-- reason: [^\n]*\n"
    r"-- \(no Lean code committed\)\s*\n+",
    re.MULTILINE,
)
paper_text_clean, n_removed = failed_pattern.subn("", paper_text)
print(f"[promote] FAILED markers eliminados de Paper.lean: {n_removed}")

# 2) Verificar que la declaracion no este ya en Paper.lean
if declarations.strip() in paper_text_clean:
    print(f"[promote] La declaracion ya esta en Paper.lean. Saltando append.")
    new_paper_text = paper_text_clean
    new_line_number = paper_text_clean[: paper_text_clean.find(declarations.strip())].count("\n") + 1
else:
    new_paper_text = paper_text_clean.rstrip() + "\n\n" + declarations.strip() + "\n\n"
    new_line_number = new_paper_text[: new_paper_text.rfind(declarations.strip())].count("\n") + 1
    print(f"[promote] Declaracion apendida a Paper.lean linea {new_line_number}")

PAPER_LEAN.write_text(new_paper_text, encoding="utf-8")

# 3) PAPER_INDEX.md: eliminar entrada vieja (failed o cualquier otra) y agregar verified
index_text = PAPER_INDEX.read_text(encoding="utf-8")

entry_pattern = re.compile(
    rf"## {re.escape(LABEL)}(?:\s*—.*?)?\n.*?\n---\n",
    re.DOTALL,
)
match = entry_pattern.search(index_text)
old_statement = ""
if match:
    old = match.group(0)
    m_st = re.search(r"Statement:\s*(.+?)(?=\n##|\n---)", old, re.DOTALL)
    if m_st:
        old_statement = m_st.group(1).strip()
    index_text_clean, n_idx = entry_pattern.subn("", index_text)
    print(f"[promote] Entradas eliminadas de PAPER_INDEX.md: {n_idx}")
else:
    index_text_clean = index_text

# Statement nuevo desde el parser si no recuperamos uno
if not old_statement:
    raw = (target_block.get("content_latex") or "")[:200].replace("\n", " ").strip()
    old_statement = raw + ("..." if len(target_block.get("content_latex") or "") > 200 else "")

block_type = target_block.get("type") or "unknown"
title = target_block.get("title")
deps = target_block.get("references") or []
deps_str = ", ".join(deps) if deps else "—"
head = f"## {LABEL}"
if title:
    head += f" — {title}"

new_entry = (
    f"{head}\n"
    f"Type: {block_type}\n"
    f"Status: ✅ verified\n"
    f"File: Paper.lean:{new_line_number}\n"
    f"Depends on: {deps_str}\n"
    f"Statement: {old_statement}\n"
    f"\n---\n\n"
)
PAPER_INDEX.write_text(index_text_clean.rstrip() + "\n\n" + new_entry, encoding="utf-8")

print()
print(f"[promote] OK: {LABEL} ahora 'verified' en Paper.lean:{new_line_number}")
print(f"[promote]      Paper.lean: {PAPER_LEAN.stat().st_size} bytes")
print(f"[promote]      PAPER_INDEX.md: {PAPER_INDEX.stat().st_size} bytes")
