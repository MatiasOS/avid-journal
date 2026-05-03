"""
Micro-bench: cuanto tarda una invocacion *trivial* de Claude Code?

Hace 3 llamadas:
  1) "responde solo OK" (mide overhead puro: arranque del CLI + 1 token)
  2) "lista los archivos del directorio actual con LS, luego responde OK"
     (mide overhead + un round-trip de tool use)
  3) "lee el archivo bench_minimal.lean con Read y luego responde OK"
     (mide overhead + read tool)

Resultado: tiempo total por invocacion. Asi medimos el "piso" del coste
por bloque del orquestrador actual.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path


CLAUDE = shutil.which("claude") or "claude"


def run(prompt: str, label: str, cwd: Path) -> float:
    print(f"\n--- {label} ---")
    print(f"prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    cmd = [
        CLAUDE,
        "-p",
        "--output-format",
        "stream-json",
        "--verbose",
        "--permission-mode",
        "bypassPermissions",
        prompt,
    ]
    t0 = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    elapsed = time.perf_counter() - t0
    print(f"exit={proc.returncode}  tiempo={elapsed:6.2f} s")
    last = ""
    for line in (proc.stdout or "").splitlines():
        if line.strip():
            last = line
    if last:
        try:
            import json
            parsed = json.loads(last)
            if parsed.get("type") == "result":
                txt = parsed.get("result", "").strip()
                print(f"resultado: {txt[:120]}")
                usage = parsed.get("usage", {})
                if usage:
                    print(
                        f"tokens: in={usage.get('input_tokens',0)} "
                        f"out={usage.get('output_tokens',0)} "
                        f"cache_read={usage.get('cache_read_input_tokens',0)}"
                    )
        except Exception as e:
            print(f"(no se pudo parsear ultima linea: {e})")
    return elapsed


def main() -> int:
    cwd = Path(__file__).resolve().parent
    (cwd / "bench_minimal.lean").write_text(
        "-- archivo trivial para medir Read tool\n"
        "def hello : Nat := 42\n",
        encoding="utf-8",
    )

    print(f"claude: {CLAUDE}")
    print(f"cwd:    {cwd}")

    times = []
    times.append(("trivial", run("Responde solo con: OK", "1) trivial", cwd)))
    times.append(("ls",      run("Lista los archivos del cwd con LS y luego responde OK.", "2) con LS", cwd)))
    times.append(("read",    run("Lee bench_minimal.lean con Read y luego responde OK.", "3) con Read", cwd)))

    print("\n=== Resumen ===")
    for label, t in times:
        print(f"  {label:<8} {t:6.2f} s")
    total = sum(t for _, t in times)
    print(f"  total    {total:6.2f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
