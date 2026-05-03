"""Detecta el encoding real del .tex de la tesis."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
p = REPO_ROOT / "examples" / "thesis_ayrton_porto" / "paper.tex"
data = p.read_bytes()
print(f"Tamano: {len(data)} bytes")
print(f"BOM UTF-8?: {data[:3] == b'\\xef\\xbb\\xbf'}")
print()
print("Probando encodings (busco una palabra con tilde como 'algebraico' o 'lenguaje'):")
for enc in ["utf-8", "utf-8-sig", "cp1252", "latin-1", "iso-8859-1", "cp850"]:
    try:
        s = data.decode(enc)
        broken = s.count("\ufffd")
        # Busco la palabra "algebraico" en su contexto
        idx = s.find("algebraico")
        if idx > 0:
            ctx = s[max(0, idx-30):idx+30]
        else:
            ctx = "(no encontrada)"
        print(f"  {enc:12s} -> OK, replacement chars: {broken}")
        print(f"               contexto 'algebraico': {ctx!r}")
    except UnicodeDecodeError as e:
        print(f"  {enc:12s} -> FAIL at byte {e.start}: {e.reason}")
print()
print("Buscando declaracion de encoding LaTeX (\\usepackage[...]{inputenc}):")
import re
data_text = data.decode("latin-1", errors="replace")
m = re.search(r"\\usepackage\[([^\]]*)\]\{inputenc\}", data_text)
if m:
    print(f"  Encontrado: {m.group(0)}")
else:
    print("  No declarado")

print()
print("Sample de los primeros 5 bloques de tipo definition (con encoding correcto):")
# Detecto cual es el bueno
best = None
for enc in ["utf-8", "cp1252", "latin-1", "iso-8859-1"]:
    try:
        s = data.decode(enc)
        broken = s.count("\ufffd")
        idx = s.find("algebraico")
        if idx > 0:
            ctx = s[max(0, idx-30):idx+30]
            if "lenguaje" in ctx:
                print(f"  Mejor candidato: {enc}  (contexto: {ctx!r})")
                best = enc
                break
    except UnicodeDecodeError:
        continue
