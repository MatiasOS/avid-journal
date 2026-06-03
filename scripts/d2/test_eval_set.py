"""Test de D2 (trivialidad) sobre T14-T18 y T23 del eval set.

Ejecutar desde WSL, desde la raíz del repo:

    python scripts/d2/test_eval_set.py \
        --lean-project /home/ayrton/avid-journal/lean_project

Si --lean-project no se especifica, se intenta detectar automáticamente
(útil si el repo está en el filesystem nativo de WSL).

Tiempo estimado por caso: 10-90 s (carga de ambiente Mathlib primera vez).
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Permite importar src/ desde repo root aunque se llame como script suelto.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.novelty_v2.dimensions.d2_triviality import check_triviality

# ---------------------------------------------------------------------------
# Enunciados del eval set en Lean 4 + Mathlib
# ---------------------------------------------------------------------------

# NOTA sobre T23: SimpleGraph.IsTree en Mathlib v4.29.0 está definido como
# una estructura con campos `isConnected : G.Connected` y `IsAcyclic : G.IsAcyclic`.
# Por eso el enunciado es provable trivialmente con aesop (es el constructor
# de la estructura). Esto es el falso positivo esperado del eval set.
#
# Si la versión de Mathlib instalada define IsTree de forma distinta, T23 puede
# no cerrar. Registrar el resultado real.

TEST_CASES = [
    {
        "id": "T14",
        "desc": "La suma de cuatro números enteros pares es par",
        "lean_statement": (
            "∀ (a b c d : Int), "
            "Even a → Even b → Even c → Even d → Even (a + b + c + d)"
        ),
        "expected_trivial": True,
        "notas": "Caso testigo original. Cierra omega o simp.",
    },
    {
        "id": "T15",
        "desc": "2 + 2 = 4",
        "lean_statement": "(2 : Nat) + 2 = 4",
        "expected_trivial": True,
        "notas": "Cierra decide o norm_num.",
    },
    {
        "id": "T16",
        "desc": "Para todo natural n, n + 0 = n",
        "lean_statement": "∀ (n : Nat), n + 0 = n",
        "expected_trivial": True,
        "notas": "Cierra simp u omega.",
    },
    {
        "id": "T17",
        "desc": "Para todo natural n, n ≤ n + 1",
        "lean_statement": "∀ (n : Nat), n ≤ n + 1",
        "expected_trivial": True,
        "notas": "Cierra omega.",
    },
    {
        "id": "T18",
        "desc": "Para todo natural n, suma de los primeros n impares = n² (TRAMPA)",
        "lean_statement": (
            "∀ (n : Nat), "
            "(Finset.range n).sum (fun k => 2 * k + 1) = n ^ 2"
        ),
        "expected_trivial": False,
        "notas": (
            "TRAMPA: necesita inducción. Ninguna táctica de T_auto debería cerrar esto. "
            "Si aesop lo cierra, es falso positivo inesperado."
        ),
    },
    {
        "id": "T23",
        "desc": "Para todo grafo finito G, si G es conexo y acíclico entonces G es árbol",
        "lean_statement": (
            "∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V), "
            "G.Connected → G.IsAcyclic → G.IsTree"
        ),
        "expected_trivial": "probable (falso positivo esperado)",
        "notas": (
            "CASO FALLA ESPERADO: IsTree = Connected ∧ IsAcyclic en Mathlib, "
            "así que aesop puede cerrar el enunciado aunque el teorema no sea trivial. "
            "Si cierra → registrar falso positivo de D2. Si no cierra → D2 correcto."
        ),
    },
]


def _fmt_attempts(all_attempts, max_show=3):
    """Muestra los primeros max_show intentos fallidos y el ganador."""
    lines = []
    shown = 0
    for tactic, success, elapsed, out in all_attempts:
        if success:
            lines.append(f"    ✓ {tactic:<12} {elapsed:.1f}s")
            break
        if shown < max_show:
            short_out = (out or "")[:80].replace("\n", " ")
            lines.append(f"    ✗ {tactic:<12} {elapsed:.1f}s  {short_out}")
            shown += 1
        elif shown == max_show:
            remaining = sum(1 for _, s, _, _ in all_attempts if not s)
            lines.append(f"    ... ({remaining - max_show} más fallaron)")
            shown += 1
    return "\n".join(lines)


def run_tests(lean_project_dir: Path, verbose: bool = False) -> None:
    total = len(TEST_CASES)
    passed = 0
    unexpected = []

    print(f"\n{'='*70}")
    print(f"D2 Trivialidad — eval set T14-T18 + T23")
    print(f"lean_project: {lean_project_dir}")
    print(f"{'='*70}\n")

    for case in TEST_CASES:
        tid = case["id"]
        desc = case["desc"]
        stmt = case["lean_statement"]
        expected = case["expected_trivial"]
        notas = case["notas"]

        print(f"[{tid}] {desc}")
        print(f"      stmt: {stmt[:72]}{'...' if len(stmt) > 72 else ''}")

        t_start = time.monotonic()
        result = check_triviality(stmt, lean_project_dir=lean_project_dir)
        t_total = time.monotonic() - t_start

        status = "TRIVIAL" if result.trivial else "NO TRIVIAL"
        winning = f"← {result.tactica} ({result.tiempo_segundos:.1f}s)" if result.trivial else ""
        print(f"      → {status} {winning}  [total {t_total:.1f}s]")

        if verbose:
            print(_fmt_attempts(result.all_attempts))

        # Verificar expectativa (solo para casos con booleano esperado)
        if isinstance(expected, bool):
            if result.trivial == expected:
                print(f"      ✓ CORRECTO (esperado: {'trivial' if expected else 'no trivial'})")
                passed += 1
            else:
                label = "FALSO POSITIVO" if result.trivial else "FALSO NEGATIVO"
                print(f"      ✗ {label} (esperado: {'trivial' if expected else 'no trivial'})")
                unexpected.append((tid, label, result))
        else:
            # T23 y otros donde expected es string (caso especial)
            print(f"      ℹ Caso especial: {notas}")
            if result.trivial:
                print(f"        → aesop cerró el enunciado (falso positivo registrado)")
            else:
                print(f"        → D2 correcto: no marcó como trivial")

        print()

    print(f"{'='*70}")
    print(f"Resultado: {passed}/{total - 1} casos con expectativa booleana correctos")
    if unexpected:
        print(f"Inesperados: {', '.join(t for t, _, _ in unexpected)}")
    print(f"{'='*70}\n")

    if unexpected:
        print("Detalle de casos inesperados:")
        for tid, label, result in unexpected:
            print(f"\n  [{tid}] {label}")
            print("  all_attempts:")
            for tactic, success, elapsed, out in result.all_attempts:
                mark = "✓" if success else "✗"
                short = (out or "")[:120].replace("\n", " ")
                print(f"    {mark} {tactic:<12} {elapsed:.1f}s  {short}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Test D2 (trivialidad) sobre T14-T18 y T23 del eval set."
    )
    parser.add_argument(
        "--lean-project",
        type=Path,
        default=Path.home() / "avid-journal" / "lean_project",
        help="Ruta al lean_project/ con Mathlib pre-compilado. "
             "Por defecto: ~/avid-journal/lean_project",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostrar todos los intentos de tácticas, no solo el ganador.",
    )
    args = parser.parse_args()

    if not args.lean_project.exists():
        print(f"ERROR: lean_project no encontrado en {args.lean_project}")
        print("Especificá --lean-project /ruta/al/lean_project con Mathlib compilado.")
        sys.exit(1)

    run_tests(args.lean_project, verbose=args.verbose)


if __name__ == "__main__":
    main()
