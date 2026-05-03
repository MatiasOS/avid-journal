"""Repro test: check_lean_files_parallel (con multiprocessing) sobre el archivo."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.formalization.scripts.lean_checker import check_lean_files_parallel

target = REPO_ROOT / "lean_project" / "Papers" / "AyrtonPortoTesis" / "Blocks" / "def_espacios_T.lean"

print(f"Verificando con multiprocessing: {target}")

if __name__ == "__main__":
    results = check_lean_files_parallel([target])
    print(f"Resultados: {len(results)}")
    for f, has_error, has_sorry, stdout, stderr in results:
        print(f"  file: {f}")
        print(f"  has_error: {has_error}")
        print(f"  has_sorry: {has_sorry}")
        print(f"  STDOUT (len={len(stdout)}): {repr(stdout[:300])}")
        print(f"  STDERR (len={len(stderr)}): {repr(stderr[:300])}")
