"""
Lista completa de bloques formalizables de la tesis con su contexto:
numero, label, tipo, capitulo/seccion, chars de prueba, deps.
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.parser.latex_parser import LaTeXParser

THESIS = REPO_ROOT / "examples" / "thesis_ayrton_porto" / "paper.tex"
data = THESIS.read_text(encoding="utf-8")

# Localizar capitulos y secciones
chapter_pattern = re.compile(r"\\chapter\*?\{([^}]+)\}", re.MULTILINE)
section_pattern = re.compile(r"\\section\*?\{([^}]+)\}", re.MULTILINE)

chapters = [(m.start(), m.group(1)) for m in chapter_pattern.finditer(data)]
sections = [(m.start(), m.group(1)) for m in section_pattern.finditer(data)]

def context_at(pos: int) -> str:
    ch = next((name for off, name in reversed(chapters) if off < pos), "(preambulo)")
    sec = next((name for off, name in reversed(sections) if off < pos), "")
    if sec:
        return f"{ch} > {sec}"
    return ch

# Parsear bloques
parser = LaTeXParser()
blocks = parser.parse_file(str(THESIS))

FORMALIZABLE = {"definition", "theorem", "lemma", "proposition", "corollary"}
formalizable_blocks = [b for b in blocks if (b.get("type") or "").lower() in FORMALIZABLE]

print(f"Capitulos detectados: {len(chapters)}")
for off, name in chapters:
    print(f"   - {name}")
print()
print(f"Secciones detectadas: {len(sections)}  (sample 10 primeras)")
for off, name in sections[:10]:
    print(f"   - {name}")
print()
print(f"Total bloques formalizables: {len(formalizable_blocks)}")
print()

# Encontrar la posicion de cada bloque en el .tex (por su label si tiene)
def find_block_pos(b):
    label = b.get("label")
    if label:
        m = re.search(r"\\label\{" + re.escape(label) + r"\}", data)
        if m:
            return m.start()
    # Si no, buscar el begin{type}
    btype = (b.get("type") or "").lower()
    return None

print("=" * 90)
print(f"{'#':>4} | {'TIPO':12s} | {'LABEL':45s} | PRUEBA | DEPS")
print("=" * 90)

current_chapter = None
current_section = None
for i, b in enumerate(formalizable_blocks, 1):
    pos = find_block_pos(b)
    if pos is None:
        ctx = "?"
        ch = "?"
    else:
        ch = next((name for off, name in reversed(chapters) if off < pos), "(preambulo)")
        sec = next((name for off, name in reversed(sections) if off < pos), "")
    if ch != current_chapter:
        current_chapter = ch
        current_section = None
        print()
        print(f"### CAPITULO: {ch}")
    if pos is not None:
        sec = next((name for off, name in reversed(sections) if off < pos), "")
        if sec != current_section:
            current_section = sec
            if sec:
                print(f"  -- Seccion: {sec}")
    label = b.get("label") or "(sin label)"
    btype = b.get("type", "?")
    proof_len = len(b.get("proof_latex") or "")
    deps = b.get("references_local") or b.get("references") or []
    deps_str = ",".join(deps[:3]) + ("..." if len(deps) > 3 else "")
    proof_str = f"{proof_len:5d}c" if proof_len else "  -  "
    print(f"{i:>4} | {btype:12s} | {label:45s} | {proof_str} | {deps_str}")

print()
print("Resumen por capitulo:")
counts = {}
for i, b in enumerate(formalizable_blocks):
    pos = find_block_pos(b)
    if pos is None:
        ch = "?"
    else:
        ch = next((name for off, name in reversed(chapters) if off < pos), "(preambulo)")
    counts[ch] = counts.get(ch, 0) + 1
for ch, n in counts.items():
    print(f"   {ch:50s}: {n} bloques")
