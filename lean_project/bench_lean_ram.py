"""
Benchmark de RAM y tiempo para `lake env lean <archivo>`.

Lanza `lake env lean <archivo>`, sondea cada 100 ms el arbol de procesos
(lake + lean.exe + cualquier hijo) y registra:
  - tiempo total (segundos)
  - RAM pico (suma de RSS de todos los procesos del arbol)
  - RAM disponible del sistema antes/durante/despues
  - swap usado antes/durante/despues

Uso:
    python bench_lean_ram.py BenchFull.lean
    python bench_lean_ram.py BenchMid.lean
    python bench_lean_ram.py BenchNarrow.lean
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

import psutil


def fmt_mb(b: int | float) -> str:
    return f"{b / (1024 * 1024):8.1f} MB"


def fmt_gb(b: int | float) -> str:
    return f"{b / (1024 ** 3):6.2f} GB"


def tree_rss(root: psutil.Process) -> int:
    total = 0
    try:
        total += root.memory_info().rss
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return 0
    for child in root.children(recursive=True):
        try:
            total += child.memory_info().rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return total


def snapshot_system() -> dict:
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()
    return {
        "ram_total": vm.total,
        "ram_available": vm.available,
        "ram_used": vm.used,
        "swap_used": sw.used,
        "swap_total": sw.total,
    }


def print_sys(label: str, snap: dict) -> None:
    print(
        f"  [{label:^14}] RAM disp: {fmt_gb(snap['ram_available'])}  "
        f"usada: {fmt_gb(snap['ram_used'])}  swap: {fmt_gb(snap['swap_used'])}"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="Archivo .lean a chequear (relativo a lean_project/)")
    ap.add_argument(
        "--project",
        default=Path(__file__).resolve().parent,
        type=Path,
        help="Ruta al proyecto Lean (por defecto: el directorio del script)",
    )
    ap.add_argument(
        "--poll-ms",
        type=int,
        default=100,
        help="Intervalo de muestreo en milisegundos (default: 100)",
    )
    args = ap.parse_args()

    project = args.project.resolve()
    target = (project / args.file).resolve()
    if not target.exists():
        print(f"[ERROR] No existe: {target}", file=sys.stderr)
        return 2

    print("=" * 72)
    print(f"BENCH: {target.name}")
    print(f"  proyecto: {project}")
    print(f"  archivo : {target}")
    print("=" * 72)

    snap0 = snapshot_system()
    print_sys("antes", snap0)

    cmd = ["lake", "env", "lean", str(target)]
    print(f"\n  CMD: {' '.join(cmd)}\n")

    t0 = time.perf_counter()
    proc = subprocess.Popen(
        cmd,
        cwd=str(project),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        ps_root = psutil.Process(proc.pid)
    except psutil.NoSuchProcess:
        print("[WARN] El proceso termino antes de poder atacharlo.")
        ps_root = None

    peak_rss = 0
    peak_children = 0
    min_avail = snap0["ram_available"]
    max_swap = snap0["swap_used"]
    samples = 0
    poll_s = args.poll_ms / 1000.0

    while proc.poll() is None:
        if ps_root is not None:
            rss = tree_rss(ps_root)
            if rss > peak_rss:
                peak_rss = rss
            try:
                n_children = len(ps_root.children(recursive=True))
                if n_children > peak_children:
                    peak_children = n_children
            except psutil.NoSuchProcess:
                pass
        vm = psutil.virtual_memory()
        sw = psutil.swap_memory()
        if vm.available < min_avail:
            min_avail = vm.available
        if sw.used > max_swap:
            max_swap = sw.used
        samples += 1
        time.sleep(poll_s)

    elapsed = time.perf_counter() - t0
    output = proc.stdout.read() if proc.stdout else ""
    rc = proc.returncode

    snap1 = snapshot_system()

    print_sys("durante (min)", {
        "ram_available": min_avail,
        "ram_used": snap0["ram_total"] - min_avail,
        "swap_used": max_swap,
    })
    print_sys("despues", snap1)

    print()
    print(f"  exit code      : {rc}")
    print(f"  tiempo         : {elapsed:7.2f} s")
    print(f"  RSS pico arbol : {fmt_mb(peak_rss)}")
    print(f"  procesos hijos pico: {peak_children}")
    print(f"  muestras       : {samples}")
    print(f"  RAM consumida  : {fmt_mb(snap0['ram_available'] - min_avail)}  (delta vs antes)")
    print(f"  swap consumido : {fmt_mb(max_swap - snap0['swap_used'])}  (delta vs antes)")

    if output.strip():
        print("\n  --- salida lean ---")
        for line in output.splitlines()[:40]:
            print(f"    {line}")
        extra = len(output.splitlines()) - 40
        if extra > 0:
            print(f"    ... (+{extra} lineas)")

    return rc


if __name__ == "__main__":
    sys.exit(main())
