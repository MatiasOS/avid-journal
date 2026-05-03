"""Repro test: check_lean_file directamente sobre def_espacios_T.lean."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.formalization.scripts.lean_checker import check_lean_file

target = REPO_ROOT / "lean_project" / "Papers" / "AyrtonPortoTesis" / "Blocks" / "def_espacios_T.lean"

print(f"Verificando: {target}")
print(f"Existe: {target.exists()}")
print()

has_error, has_sorry, stdout, stderr = check_lean_file(target)
print(f"has_error: {has_error}")
print(f"has_sorry: {has_sorry}")
print()
print(f"STDOUT (len={len(stdout)}):")
print(repr(stdout[:500]))
print()
print(f"STDERR (len={len(stderr)}):")
print(repr(stderr[:500]))
