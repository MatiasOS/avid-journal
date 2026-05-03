"""Audita los tipos de \\ref en la tesis."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
p = ROOT / "examples" / "thesis_ayrton_porto" / "paper.tex"
data = p.read_text(encoding="utf-8")

patterns = [
    (r"\\ref\{", r"\ref"),
    (r"\\eqref\{", r"\eqref"),
    (r"\\autoref\{", r"\autoref"),
    (r"\\cref\{", r"\cref"),
    (r"\\Cref\{", r"\Cref"),
    (r"\\nameref\{", r"\nameref"),
    (r"\\pageref\{", r"\pageref"),
    (r"\\hyperref\[", r"\hyperref"),
]

print("Conteo de cada tipo de referencia en la tesis:")
for pat, name in patterns:
    n = len(re.findall(pat, data))
    print(f"  {name:20s}: {n}")

print()
print("Sample de cada tipo encontrado:")
for pat, name in patterns:
    m = re.search(pat + r"[^}\]]+[\}\]]", data)
    if m:
        idx = m.start()
        ctx = data[max(0, idx-30):idx+60].replace("\n", " ")
        print(f"  {name:20s}: ...{ctx}...")

print()
print("Buscando como aparece 'def:lenguaje-algebraico' citado en otros lugares:")
for m in re.finditer(r"\S{0,15}\{def:lenguaje-algebraico\}", data):
    idx = m.start()
    ctx = data[max(0, idx-40):idx+60].replace("\n", " ")
    print(f"  ...{ctx}...")

print()
print("Lista completa de comandos LaTeX que reciben labels (heuristica):")
labels_in_text = set(re.findall(r"\\label\{([^}]+)\}", data))
print(f"  Total labels declarados: {len(labels_in_text)}")
# Para cada label, contar cuantas veces se cita con cualquier comando
cites = {}
for label in labels_in_text:
    label_esc = re.escape(label)
    pat = re.compile(r"\\(\w+)\{" + label_esc + r"\}")
    for cmd in pat.findall(data):
        cites[cmd] = cites.get(cmd, 0) + 1
print("  Comandos que citan labels (top 10):")
for cmd, n in sorted(cites.items(), key=lambda x: -x[1])[:10]:
    print(f"    \\{cmd}: {n}")
