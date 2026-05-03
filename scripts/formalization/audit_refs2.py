"""Investiga si las refs detectadas como deps matchean con labels reales."""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.parser.latex_parser import LaTeXParser

THESIS = REPO_ROOT / "examples" / "thesis_ayrton_porto" / "paper.tex"

parser = LaTeXParser()
blocks = parser.parse_file(str(THESIS))

# Set de labels declarados por bloques formalizables
formalizable = {"definition", "theorem", "lemma", "proposition", "corollary"}
block_labels = set()
for b in blocks:
    if (b.get("type") or "").lower() in formalizable:
        if b.get("label"):
            block_labels.add(b["label"])

# Todos los labels en el archivo
data = THESIS.read_text(encoding="utf-8")
all_labels = set(re.findall(r"\\label\{([^}]+)\}", data))
all_refs = re.findall(r"\\ref\{([^}]+)\}", data)
ref_counter = {}
for r in all_refs:
    ref_counter[r] = ref_counter.get(r, 0) + 1

print(f"Total \\label declarados: {len(all_labels)}")
print(f"Labels asociados a bloques formalizables: {len(block_labels)}")
print(f"Otros labels (capitulos, secciones, ecuaciones, figuras, etc.): {len(all_labels - block_labels)}")
print()
print("Sample de OTROS labels (no formalizables):")
others = sorted(all_labels - block_labels)[:20]
for x in others:
    print(f"   {x}")

print()
print(f"Total \\ref distintos: {len(ref_counter)}")
referenced = set(ref_counter.keys())
print(f"  Refs a labels de bloques formalizables: {len(referenced & block_labels)}")
print(f"  Refs a otros labels (capitulos/figuras/etc): {len(referenced & (all_labels - block_labels))}")
print(f"  Refs a labels INEXISTENTES (typos): {len(referenced - all_labels)}")

print()
print("Refs a labels INEXISTENTES (typos en la tesis):")
broken = sorted(referenced - all_labels)
for x in broken[:15]:
    print(f"   {x!r}  (citada {ref_counter[x]} veces)")
if len(broken) > 15:
    print(f"   ... y {len(broken)-15} mas")

print()
print("Bloques formalizables sin dependencias detectadas que SI tienen \\ref a otros bloques:")
formalizable_blocks = [b for b in blocks if (b.get("type") or "").lower() in formalizable]
for b in formalizable_blocks[:20]:
    deps = b.get("references_local") or b.get("references") or []
    if deps:
        continue
    body = (b.get("content_latex") or "") + (b.get("proof_latex") or "")
    refs_in_body = re.findall(r"\\ref\{([^}]+)\}", body)
    refs_to_blocks = [r for r in refs_in_body if r in block_labels]
    if refs_to_blocks:
        print(f"   {b.get('label')!r} ({b.get('type')}): {refs_to_blocks}")
