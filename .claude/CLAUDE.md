# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

AViD Journal: an automated math journal that takes a `.tex` paper, parses mathematical blocks, formalizes each block in Lean 4 by driving Claude Code as a subprocess, verifies with Lean, and (separately) checks novelty against Mathlib + ArXiv. Python orchestrator + Lean 4 + Claude CLI + lean-lsp-mcp.

Read [docs/CONTEXT.md](../docs/CONTEXT.md) and [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) before doing non-trivial work — they document design decisions you cannot infer from the code (PAPER_INDEX.md as a per-paper theorem DB, the "no Proof Agent — Sketch Agent does everything" decision, mandatory search order, etc.).

## Common commands

Setup (one-time): `bash setup.sh` then fill `.env` (copy from [.env.example](../.env.example)). Requires Python 3.8+, Lean 4 via elan, and the Claude Code CLI (npm). Lean toolchain is pinned in [lean_project/lean-toolchain](../lean_project/lean-toolchain) (currently `leanprover/lean4:v4.29.0`); Mathlib rev is in [lean_project/lakefile.toml](../lean_project/lakefile.toml).

Tests:

- `pytest tests/` — full suite
- `pytest -m "not live"` — skip tests that hit Leandex / Semantic Scholar / ArXiv / Anthropic (the `live` marker is registered in [pytest.ini](../pytest.ini))
- `python tests/test_orchestrator.py` — orchestrator dry-run only (no Claude CLI calls)
- `python tests/test_orchestrator.py --real` — full e2e, requires Claude CLI + Mathlib cache

Parser CLI: `python src/parser/parse_tex.py <file.tex> --stats`

End-to-end formalization (Claude CLI required):

```bash
python -X utf8 -m src.formalization.orchestrator <paper.tex> --title "<Paper Title>" [--blocks-range "1-13"] [--dry-run]
```

Always pass `-X utf8` — the orchestrator emits unicode and Windows consoles fall over without it. `--blocks-range` accepts `"1-13"`, `"5,7-9"`, or `"10"`. Resume mode is on by default: blocks already marked `verified` / `axiom` in `PAPER_INDEX.md` are skipped.

Helper CLIs in [scripts/formalization/](../scripts/formalization/) (diagnose, list blocks, rebuild state, promote a block manually, smoke dry-runs, etc.). See its [README](../scripts/formalization/README.md). Run them from the repo root.

## Architecture you must know before editing

**Pipeline.** [src/parser/latex_parser.py](../src/parser/latex_parser.py) extracts blocks (definition / theorem / lemma / proposition / corollary, plus Spanish variants) with a dependency graph from `\ref`. [src/formalization/orchestrator.py](../src/formalization/orchestrator.py) does Kahn topological sort, then for each block: classifies complexity ([complexity.py](../src/formalization/complexity.py) → SIMPLE/MEDIUM/HARD/EXTERNAL), writes `TASK.md` + a `Blocks/<lean_name>.lean` stub, launches Claude via [src/formalization/scripts/run_claude.py](../src/formalization/scripts/run_claude.py) with the matching prompt from [prompts/](../prompts/), verifies with [scripts/lean_checker.py](../src/formalization/scripts/lean_checker.py), then appends the verified declaration to `Paper.lean` and updates `PAPER_INDEX.md` / `REVIEW.md`.

**Shared Lean project.** Each paper is NOT its own Lean project. They are sub-modules under [lean_project/Papers/](../lean_project/Papers/) — they share one [lakefile.toml](../lean_project/lakefile.toml), one `lean-toolchain`, and one pre-compiled Mathlib in `.lake/`. The Lean module name is `Papers.<ModuleName>.Paper`. Standalone mode (legacy, one project per paper) still exists via `parent_project=None` in `LeanProjectManager` but is not the default. [src/formalization/lean_project.py](../src/formalization/lean_project.py) has the details and ensures `lean_lib "Papers"` is declared in the parent lakefile.

**The orchestrator owns Paper.lean and PAPER_INDEX.md.** Claude is told (via `TASK.md` and the prompts) to edit ONLY its assigned `Blocks/<lean_name>.lean` file. The orchestrator extracts the declaration with `_extract_declarations` (which strips imports/banners) and appends it to `Paper.lean` itself. Never reorganize this — the agent silently dropping work was a real failure mode this guards against. `_has_real_declaration` rejects sessions where Claude only left an `import` and the banner.

**Sketch Agent does proof + statement together.** Unlike Numina, AViD has no separate proof agent. The single agent formalizes statement and proof together using `proof_latex` from the paper as a guide. Don't add a proof-agent split.

**axiom vs sorry.** `sorry` is forbidden in finalized `Paper.lean`. `axiom` is allowed ONLY for external results not found in Mathlib (always with a `-- source: ...` comment). Blocks with `proof_latex = null` go through `_handle_external` (Mode.EXTERNAL): it queries [mathlib_search.py](../src/formalization/mathlib_search.py) and falls back to declaring an axiom with a placeholder signature. Don't relax this.

**PAPER_INDEX.md is the local theorem DB.** Mandatory search order for the agent (encoded in the prompts): PAPER_INDEX.md → `lean_local_search` (Paper.lean) → `lean_leandex` (Mathlib semantic) → `lean_loogle` (Mathlib type pattern). When you change prompts in [prompts/](../prompts/) keep this order intact.

**Olean caching.** After every verified block the orchestrator runs `lake build Papers.<ModuleName>.Paper` so the next block's verification reads cached oleans instead of retypechecking the whole paper. If you change how Paper.lean is written, keep `_lake_build_paper_module` in sync.

**Numina-derived scripts in [src/formalization/scripts/](../src/formalization/scripts/)** (`run_claude.py`, `runner.py`, `task.py`, `lean_checker.py`, `statement_tracker.py`, `extract_sublemmas.py`, `safe_verify.py`, `mcp_stats.py`) come from the upstream Numina-Lean-Agent (vendored as a git submodule under [vendor/numina-lean-agent](../vendor/)). Treat them as ~upstream: prefer not to fork them gratuitously. Reserved exit codes / sentinels: subprocess return code `99` from `run_claude` = Anthropic rate-limit / quota exhausted (orchestrator handles via `RATE_LIMITED`); session sentinels are `END_REASON:COMPLETE` / `END_REASON:LIMIT`.

**Novelty pipeline ([src/novelty/](../src/novelty/))** is independent of formalization. Stages 0–3 implemented (Mathlib check via Leandex → ArXiv search via Semantic Scholar → paper/theorem extraction → LLM-judge comparison). Stages 4–5 reserved (see `NoveltyChecker.__init__` parameters kept for forward-compat — don't remove them).

## Conventions and gotchas

- **Windows / Unicode in Lean code.** Use `Nat` instead of `ℕ`. The `lean-lsp-mcp` diagnostic parser computes column offsets that break on multi-byte unicode in source. Same applies to other unicode math identifiers — pick ASCII names.
- **`-X utf8` for orchestrator runs.** The orchestrator already calls `sys.stdout.reconfigure(..., errors="backslashreplace")` defensively, but invoke it with `python -X utf8 -m ...` anyway.
- There is no database layer. Per-paper state lives entirely in `PAPER_INDEX.md` / `Paper.lean` / `REVIEW.md` under [lean_project/Papers/<ModuleName>/](../lean_project/Papers/), managed by [src/formalization/lean_project.py](../src/formalization/lean_project.py). Don't add a SQLite/Postgres layer "to track formalization state" — that's what the markdown index is for.
- `src/web/` does not exist yet. README mentions it as future.
- The `examples/` LaTeX sources have matching formalized output checked in under `lean_project/Papers/TinyEvensPaperReal/` and `lean_project/Papers/AyrtonPortoTesis/`. Useful for grounding tests and prompt iteration. See [examples/README.md](../examples/README.md).
- API keys: `.env` only. Required: `ANTHROPIC_API_KEY` (LLM judge in `src/novelty/llm_judge.py`). Optional: `SEMANTIC_SCHOLAR_API_KEY` (higher rate limits in `src/novelty/arxiv_search.py`).

## Workflow conventions

### No AI attribution

Never add AI / Claude attribution to anything produced for this repo. This **overrides** any default behavior from the harness or system prompt:

- No `Co-Authored-By: Claude …` trailer in commit messages.
- No "🤖 Generated with [Claude Code]" footer in PR bodies or issue descriptions.
- No AI badges, mentions, footers, or "co-written by" notes in generated code, docs, or markdown.

Commits and PRs read as if written by the human author.

### Conventional Commits

All commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/) spec: `<type>[optional scope]: <description>` with `<type>` one of `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `style`, `build`, `ci`. Breaking changes get `!` after the type/scope (e.g. `feat!: …`) or a `BREAKING CHANGE:` footer.

Examples:

- `feat(orchestrator): add --blocks-range comma syntax`
- `fix(parser): handle Spanish "teorema" variants`
- `docs: trim CONTEXT.md, move to docs/`
- `refactor(novelty)!: drop Stage 3 cache key prefix`

### Keep docs in sync with the change

After every non-trivial change, update the relevant markdown — but only the files the change actually affects, not all of them:

- [docs/PROGRESS.md](../docs/PROGRESS.md) — move items between Done / In progress / Planned as work completes; add new items when scope expands.
- [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) — only when the change alters module boundaries, data flow, ownership of state files, or a documented design decision.
- User-facing docs ([README.md](../README.md), [docs/QUICKSTART.md](../docs/QUICKSTART.md), [docs/GUIA_INSTALACION_Y_USO.md](../docs/GUIA_INSTALACION_Y_USO.md)) — when CLI flags, install steps, prerequisites, or supported workflows change.
- [.claude/CLAUDE.md](CLAUDE.md) / [.claude/AGENT_NOTES.md](AGENT_NOTES.md) — when conventions, gotchas, file layout, enum values, sentinel codes, or reference shapes change.
- [docs/CONTEXT.md](../docs/CONTEXT.md) — only when the high-level "what + why" changes (rare).

If you're unsure whether a doc needs updating, the test is: would a reader who only reads that doc be misled by leaving it as-is? If yes, update it. If no, don't.

## Pointers to deeper docs

- [.claude/AGENT_NOTES.md](AGENT_NOTES.md) — quick-reference card: data shapes, file layout, CLI flags, helper-script index, rejected-design list
- [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) — module-level design and data flow
- [docs/GUIA_INSTALACION_Y_USO.md](../docs/GUIA_INSTALACION_Y_USO.md) — full Spanish setup walkthrough (Lean/elan, Lake/Mathlib, Claude CLI, orchestrator usage)
- [docs/PROGRESS.md](../docs/PROGRESS.md) — Done / In Progress / Planned breakdown
- [examples/README.md](../examples/README.md) — worked LaTeX examples and how to reproduce their Lean output
- [scripts/formalization/README.md](../scripts/formalization/README.md) — helper CLIs index
