"""Smoke test: dry-run con blocks_range tras los fixes."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.formalization.orchestrator import formalize_paper

res = formalize_paper(
    str(REPO_ROOT / "examples" / "thesis_ayrton_porto" / "paper.tex"),
    paper_title="Ayrton Porto Tesis",
    blocks_range="14-30",
    dry_run=True,
)
print()
print(f"Total: {res['total_blocks']}")
print(f"Counts: {res['counts']}")
