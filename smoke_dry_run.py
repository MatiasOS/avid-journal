"""Smoke test: dry-run con blocks_range tras los fixes."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
sys.path.insert(0, ".")

from src.formalization.orchestrator import formalize_paper

res = formalize_paper(
    "examples/thesis_ayrton_porto/paper.tex",
    paper_title="Ayrton Porto Tesis",
    blocks_range="14-30",
    dry_run=True,
)
print()
print(f"Total: {res['total_blocks']}")
print(f"Counts: {res['counts']}")
