"""Verifica filtrado por rango y modo resume sobre la tesis (dry_run, sin Claude)."""
import sys
import os
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)

sys.path.insert(0, os.path.dirname(__file__))

from pathlib import Path
from src.formalization.orchestrator import formalize_paper, _parse_blocks_range

# Test 1: parser de rangos
print("=" * 70)
print("TEST 1: _parse_blocks_range")
print("=" * 70)
cases = [
    ("1-13", 100, list(range(1, 14))),
    ("5-", 20, list(range(5, 21))),
    ("10", 100, [10]),
    ("1,3,7-9", 100, [1, 3, 7, 8, 9]),
    ("", 5, [1, 2, 3, 4, 5]),
    ("90-200", 100, list(range(90, 101))),  # clamping
    ("0-3", 100, [1, 2, 3]),                  # clamping inferior
]
for spec, total, expected in cases:
    got = _parse_blocks_range(spec, total)
    status = "OK" if got == expected else "FAIL"
    print(f"  [{status}] '{spec}' (total={total}) -> {got[:6]}{'...' if len(got)>6 else ''}")
    if got != expected:
        print(f"        esperado: {expected[:6]}...")
print()

# Test 2: orquestador en dry_run sobre la tesis con --blocks-range 1-13
print("=" * 70)
print("TEST 2: formalize_paper(blocks_range='1-13', dry_run=True) sobre tesis")
print("=" * 70)
THESIS = str(Path(__file__).resolve().parent / "examples" / "thesis_ayrton_porto" / "paper.tex")

summary = formalize_paper(
    tex_path=THESIS,
    paper_title="AyrtonPortoTesisDryTest",
    dry_run=True,
    blocks_range="1-13",
    resume=True,
)
print()
print(f"Procesados (en dry-run): {summary['total_blocks']}")
print(f"Counts: {summary['counts']}")
print(f"Project: {summary['project_dir']}")

assert summary["total_blocks"] == 13, f"Esperado 13, fue {summary['total_blocks']}"
print("\n[PASS] Filtro de rango 1-13 funciona en dry_run.")
