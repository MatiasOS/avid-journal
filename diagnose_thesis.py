"""
Diagnostico de la tesis para AViD Journal.

Ejecuta SOLO el parser (sin gastar tokens de Claude) y reporta:
- Numero de bloques por tipo
- Cuantos tienen label / dependencias
- Detecta \\input/\\include externos
- Sample de los primeros bloques
- Estimacion de costo y tiempo proyectado
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.parser.latex_parser import LaTeXParser

THESIS = ROOT / "examples" / "thesis_ayrton_porto" / "paper.tex"

# Costos reales del sample paper (3 bloques): $1.66 / 25 min
COST_PER_BLOCK_USD = 1.66 / 3  # ~$0.55
TIME_PER_BLOCK_MIN = 25 / 3    # ~8.3 min

print("=" * 70)
print("DIAGNOSTICO DE TESIS PARA AViD")
print("=" * 70)
print(f"Archivo: {THESIS.name}")
print(f"Tamano: {THESIS.stat().st_size / 1024:.1f} KB")

raw = THESIS.read_text(encoding="utf-8", errors="replace")
print(f"Caracteres: {len(raw):,}")

inputs = re.findall(r"\\(?:input|include)\{([^}]+)\}", raw)
print(f"\\input/\\include externos detectados: {len(inputs)}")
if inputs:
    for x in inputs[:10]:
        print(f"   - {x}")
    if len(inputs) > 10:
        print(f"   ... y {len(inputs)-10} mas")

print()
print("-" * 70)
print("PARSEANDO BLOQUES MATEMATICOS...")
print("-" * 70)

parser = LaTeXParser()
blocks = parser.parse_file(str(THESIS))
print(f"Total bloques extraidos: {len(blocks)}")

by_type = {}
with_label = 0
with_proof = 0
with_deps = 0
total_deps = 0
total_proof_chars = 0
total_stmt_chars = 0
labels_seen = []

for b in blocks:
    t = b.get("type", "unknown")
    by_type[t] = by_type.get(t, 0) + 1
    if b.get("label"):
        with_label += 1
        labels_seen.append(b["label"])
    if b.get("proof_latex"):
        with_proof += 1
        total_proof_chars += len(b["proof_latex"])
    deps = b.get("references_local", []) or b.get("references", []) or []
    if deps:
        with_deps += 1
        total_deps += len(deps)
    if b.get("content_latex"):
        total_stmt_chars += len(b["content_latex"])

print()
print("Distribucion por tipo:")
for t, n in sorted(by_type.items(), key=lambda x: -x[1]):
    print(f"   {t:15s}: {n}")

print()
print(f"Bloques con label:           {with_label}/{len(blocks)} ({100*with_label/max(len(blocks),1):.0f}%)")
print(f"Bloques con proof_latex:     {with_proof}/{len(blocks)} ({100*with_proof/max(len(blocks),1):.0f}%)")
print(f"Bloques con dependencias:    {with_deps}/{len(blocks)} ({100*with_deps/max(len(blocks),1):.0f}%)")
print(f"Total referencias detectadas: {total_deps}")
print(f"Promedio statement: {total_stmt_chars // max(len(blocks),1)} chars")
print(f"Promedio proof:     {total_proof_chars // max(with_proof,1)} chars (entre los que tienen)")

print()
print("-" * 70)
print("ESTIMACION DE COSTO Y TIEMPO (basado en sample real)")
print("-" * 70)
total_cost = len(blocks) * COST_PER_BLOCK_USD
total_time_min = len(blocks) * TIME_PER_BLOCK_MIN
print(f"Bloques a procesar: {len(blocks)}")
print(f"Costo estimado:     ${total_cost:.2f} USD")
print(f"Tiempo estimado:    {total_time_min:.0f} min  ({total_time_min/60:.1f} horas)")
print(f"Presupuesto $20 da para aprox: {int(20/COST_PER_BLOCK_USD)} bloques")

print()
print("-" * 70)
print("PRIMEROS 3 BLOQUES (sample)")
print("-" * 70)
def _safe(s):
    return (s or "")

for i, b in enumerate(blocks[:5], 1):
    print(f"\n[{i}] type={b.get('type')} label={b.get('label')!r}")
    print(f"    title: {_safe(b.get('title'))[:80]}")
    stmt = _safe(b.get("content_latex")).strip().replace("\n", " ")
    print(f"    statement[:200]: {stmt[:200]}")
    if b.get("proof_latex"):
        proof = b["proof_latex"].strip().replace("\n", " ")
        print(f"    proof[:200]:     {proof[:200]}")
    deps = b.get("references_local", []) or b.get("references", []) or []
    if deps:
        print(f"    deps: {deps[:5]}")

print()
print("-" * 70)
print("MUESTRA INTERMEDIA: 3 bloques con DEPENDENCIAS y proof")
print("-" * 70)
shown = 0
for i, b in enumerate(blocks):
    deps = b.get("references_local", []) or b.get("references", []) or []
    if deps and b.get("proof_latex") and shown < 3:
        shown += 1
        print(f"\n[{i+1}] type={b.get('type')} label={b.get('label')!r}")
        print(f"    title: {_safe(b.get('title'))[:80]}")
        stmt = _safe(b.get("content_latex")).strip().replace("\n", " ")
        print(f"    statement[:200]: {stmt[:200]}")
        proof = b["proof_latex"].strip().replace("\n", " ")
        print(f"    proof[:300]:     {proof[:300]}")
        print(f"    deps: {deps}")

print()
print("-" * 70)
print("ULTIMOS 3 BLOQUES")
print("-" * 70)
for i, b in enumerate(blocks[-3:], 1):
    idx = len(blocks)-3+i
    print(f"\n[{idx}] type={b.get('type')} label={b.get('label')!r}")
    print(f"    title: {_safe(b.get('title'))[:80]}")
    stmt = _safe(b.get("content_latex")).strip().replace("\n", " ")
    print(f"    statement[:150]: {stmt[:150]}")

print()
print("=" * 70)
print("FIN DEL DIAGNOSTICO")
print("=" * 70)
