"""Comprueba si encoding cp1252 vs utf-8 en subprocess da resultados diferentes."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
target = REPO_ROOT / "lean_project" / "Papers" / "AyrtonPortoTesis" / "Blocks" / "def_espacios_T.lean"
project_root = REPO_ROOT / "lean_project"

print("=== Test 1: subprocess con text=True (encoding por defecto Windows) ===")
result = subprocess.run(
    ["lake", "env", "lean", str(target)],
    capture_output=True,
    text=True,
    timeout=60,
    cwd=str(project_root),
)
print(f"returncode: {result.returncode}")
print(f"stdout (len={len(result.stdout)}): {repr(result.stdout[:500])}")
print(f"stderr (len={len(result.stderr)}): {repr(result.stderr[:500])}")
print(f"'error' in stdout.lower(): {'error' in result.stdout.lower()}")
print(f"'error' in stderr.lower(): {'error' in result.stderr.lower()}")
print(f"'sorry' in stdout.lower(): {'sorry' in result.stdout.lower()}")
print(f"'sorry' in stderr.lower(): {'sorry' in result.stderr.lower()}")
print()

print("=== Test 2: subprocess con bytes, decodificando UTF-8 ===")
result2 = subprocess.run(
    ["lake", "env", "lean", str(target)],
    capture_output=True,
    timeout=60,
    cwd=str(project_root),
)
print(f"returncode: {result2.returncode}")
print(f"stdout bytes (len={len(result2.stdout)}): {result2.stdout[:200]}")
print(f"stderr bytes (len={len(result2.stderr)}): {result2.stderr[:200]}")
print()

print("=== Test 3: encoding del runner script - verificar si hay 'error' en logs de import ===")
for tup in [(b"error\xe3", "cp1252"), (b"\xc4\x91error", "utf-8")]:
    s, enc = tup
    decoded = s.decode(enc, errors="replace")
    print(f"  '{enc}' decode of {s}: {repr(decoded)} - has 'error': {'error' in decoded.lower()}")
