# AViD Journal — Progress

## 🎯 Project goal

Build the first fully automated mathematics journal that:

1. Accepts `.tex` papers
2. Formalizes proofs in Lean 4
3. Verifies correctness
4. Checks novelty (Mathlib + ArXiv)
5. Auto-publishes if valid

---

## ✅ Done

### Parser

- LaTeX parser ([src/parser/latex_parser.py](../src/parser/latex_parser.py)) that extracts theorems, lemmas, definitions, propositions, corollaries with their dependency graph (`\ref` resolution) and handles custom environments + Spanish variants (`teorema`, `lema`, …)
- CLI ([src/parser/parse_tex.py](../src/parser/parse_tex.py))

### Formalization pipeline

- Block complexity classifier ([src/formalization/complexity.py](../src/formalization/complexity.py)) — SIMPLE / MEDIUM / HARD / EXTERNAL, drives which prompt to use
- Three prompt modes in [prompts/](../prompts/) (`prompt_avid.txt`, `prompt_medium_mode_avid.txt`, `prompt_hard_mode_avid.txt`) plus coordinator / blueprint / sketch / common docs under [prompts/docs/prompts/](../prompts/docs/prompts/)
- Lean project manager ([src/formalization/lean_project.py](../src/formalization/lean_project.py)) — shared Lean project with Mathlib pre-built; each paper lives at `lean_project/Papers/<ModuleName>/`
- Orchestrator ([src/formalization/orchestrator.py](../src/formalization/orchestrator.py)) — Kahn topological sort, per-block TASK.md + Blocks/ stub, Claude subprocess via [scripts/run_claude.py](../src/formalization/scripts/run_claude.py), verification via [scripts/lean_checker.py](../src/formalization/scripts/lean_checker.py), append-to-Paper.lean with declaration extraction, PAPER_INDEX.md / REVIEW.md updates, resume mode, olean caching with `lake build` after each block, Mathlib axiom fallback via [src/formalization/mathlib_search.py](../src/formalization/mathlib_search.py)
- Two worked examples checked in: [lean_project/Papers/TinyEvensPaperReal/](../lean_project/Papers/TinyEvensPaperReal/), [lean_project/Papers/AyrtonPortoTesis/](../lean_project/Papers/AyrtonPortoTesis/)
- Helper CLIs in [scripts/formalization/](../scripts/formalization/) (diagnose, rebuild, smoke, promote, audit refs, benchmarks)

### Novelty pipeline (Stages 0–3)

- Stage 0 — Mathlib check via Leandex ([src/novelty/mathlib_checker.py](../src/novelty/mathlib_checker.py))
- Stage 1 — ArXiv search via Semantic Scholar + ArXiv ([src/novelty/arxiv_search.py](../src/novelty/arxiv_search.py)), with dedupe + threshold
- Stage 2 — PDF download + text extraction ([src/novelty/paper_extractor.py](../src/novelty/paper_extractor.py))
- Stage 3 — block ↔ candidate comparison with Claude judge ([src/novelty/block_comparator.py](../src/novelty/block_comparator.py), [src/novelty/llm_judge.py](../src/novelty/llm_judge.py))
- Orchestrator ([src/novelty/novelty_checker.py](../src/novelty/novelty_checker.py)) emits a `NoveltyLabel` per block
- Disk cache for external API calls ([src/novelty/_cache.py](../src/novelty/_cache.py))

---

## ⏳ In progress / 🔜 Planned

- Novelty Stages 4–5 — formalize the candidate match and compare the tree of dependent types against the paper's block. Parameter slots already kept in `NoveltyChecker.__init__` for forward compatibility.
- Polish the hard-mode pipeline — coordinator + blueprint + sketch handoff on real papers.
- More end-to-end golden papers beyond the current two examples.
- Web interface for paper submission.
- Quality assessment module (citation prediction, impact scoring).

---

## 💡 Decisions made

### Technology stack

- **Parser**: custom Python (regex + heuristics).
- **Novelty**: Semantic Scholar + Claude LLM judge.
- **Formalization**: Claude Code CLI driven by AViD prompts (inspired by Numina-Lean-Agent's coordinator / blueprint / sketch pattern; Numina-derived runtime utilities vendored under `src/formalization/scripts/`).
- **Web**: FastAPI + React (planned).

### Scope

- **NOT implementing** custom Lean tactics.
- **NOT implementing** training custom models.
- **NOT implementing** full ArXiv indexing (too expensive — Semantic Scholar instead).
- **Focus**: integration of existing tools into a coherent system.

### Single Sketch Agent

Unlike Numina, AViD has no separate "proof agent". The Sketch Agent formalizes statement and proof together, using the paper's `proof_latex` as a guide. This keeps the agent loop simpler and shares context between statement and proof.

### sorry / axiom policy

- `sorry` is forbidden in `Paper.lean`.
- `axiom` is allowed **only** for external results (`proof_latex = null`) that are not found in Mathlib, and always with a `-- source: ...` comment so a human can review them in `REVIEW.md`.

---

## 🐛 Known issues

1. **LeanDex API** — not publicly accessible.
   - Workaround: keep results cached on disk.
2. **Semantic Scholar API** — rate limits.
   - Solution: caching + backoff already implemented in [_cache.py](../src/novelty/_cache.py).
3. **Numina setup** — complex dependencies.
   - Solution: vendored as a git submodule under `vendor/numina-lean-agent`; AViD copies the relevant runtime scripts into `src/formalization/scripts/`.
