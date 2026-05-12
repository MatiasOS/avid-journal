# AGENT_NOTES — Quick-reference card for Claude Code in this repo

Companion to [CLAUDE.md](CLAUDE.md). CLAUDE.md is the *narrative* (architecture, the "why"). This file is the *lookup table* — paste-ready CLI commands, exact data shapes, enum values, helper-script index, and the list of design decisions you should not relitigate.

If a fact here disagrees with the source code, the **source code wins**. Update this file in the same PR.

---

## §1 Data shapes

### Parsed block dict — [src/parser/latex_parser.py:430-437](../src/parser/latex_parser.py#L430-L437)

```python
{
    "type":           str,            # 'definition' | 'theorem' | 'lemma' | 'proposition' | 'corollary' | normalized variant
    "label":          str | None,     # \label{...} value; None if the block had none
    "title":          str | None,     # \begin{theorem}[Title] — None when no bracketed title
    "content_latex":  str,            # always populated (blocks with <3 chars of content are dropped)
    "proof_latex":    str | None,     # None for definitions; None for theorems whose proof was not in the source
    "references":     list[str] | None,  # \ref targets from content+proof, deduped. None (not []) when empty.
}
```

Return type annotation in the parser is `List[Dict[str, Optional[str]]]`, but `references` is actually `list[str] | None` — the type hint there is loose.

### `Mode` enum — [src/formalization/complexity.py:15-21](../src/formalization/complexity.py#L15-L21)

| Mode | `.value` | Prompt file | `max_rounds_for` |
|---|---|---|---|
| `Mode.SIMPLE` | `"simple"` | `prompts/prompt_avid.txt` | 5 |
| `Mode.MEDIUM` | `"medium"` | `prompts/prompt_medium_mode_avid.txt` | 15 |
| `Mode.HARD` | `"hard"` | `prompts/prompt_hard_mode_avid.txt` | 30 |
| `Mode.EXTERNAL` | `"external"` | **none** — orchestrator routes through `_handle_external` (Mathlib lookup → axiom) | n/a |

Calling `prompt_file_for(Mode.EXTERNAL)` raises `KeyError` — it has no prompt by design.

### Classifier inputs

`classify(block)` reads only `block["type"]`, `block["content_latex"]`, `block["proof_latex"]`. The complexity thresholds: proof length ≥ 800 chars → HARD, ≥ 3 step markers → HARD, ≥ 400 chars + complexity signals (case/induction/WLOG/contradiction/contrapositive/inline lemma) → HARD, else MEDIUM. `proof_latex` empty/None → EXTERNAL.

### `NoveltyLabel` — [src/novelty/novelty_checker.py:25-30](../src/novelty/novelty_checker.py#L25-L30)

`NOVEL` · `NOVEL_METHOD` · `GENERALIZATION` · `NOT_NOVEL` · `IN_MATHLIB`

Paper-level `recommendation` returned by `check_paper`: `REDUNDANT` (all NOT_NOVEL, or only IN_MATHLIB+NOT_NOVEL) · `NEEDS REVIEW` (any NOT_NOVEL or IN_MATHLIB mixed with novel) · `PUBLISHABLE` (otherwise).

### `PAPER_INDEX.md` row format — [src/formalization/lean_project.py:674-683](../src/formalization/lean_project.py#L674-L683)

```markdown
## {label} — {title}
Type: {definition|theorem|lemma|proposition|corollary}
Status: ✅ verified | ⚠️ axiom | ❌ failed
File: Paper.lean:{lean_line}
Depends on: {label1, label2 | —}
Source: {citation}        ← only present for axioms
Statement: {first 200 chars of statement, newlines collapsed}

---
```

Resume-mode skip logic — [src/formalization/lean_project.py:434-446](../src/formalization/lean_project.py#L434-L446): the parser normalizes the on-disk emoji-status to a plain token (`verified`, `axiom`, `failed`, `other`). The orchestrator skips blocks whose normalized status is `verified` or `axiom`. `failed` is **not** skipped — it gets re-tried. Use `--no-resume` to ignore the index entirely.

---

## §2 Per-paper on-disk layout

```
lean_project/Papers/<Slug>/
├── Paper.lean              ← orchestrator-owned; NEVER edit from a Claude session
├── PAPER_INDEX.md          ← orchestrator-owned (theorem DB consulted first)
├── REVIEW.md               ← orchestrator-owned (axioms / failures / notes)
├── Blocks/<lean_name>.lean ← ★ THE ONLY FILE the Claude session edits
├── TASK.md                 ← orchestrator-written per block (current task context)
└── docs/prompts/           ← agent prompts copied for the session
```

- Lean module name: `Papers.<Slug>.Paper`.
- Each `Blocks/<lean_name>.lean` must keep `import Papers.<Slug>.Paper` so prior verified blocks are in scope.
- After every verified block the orchestrator runs `lake build Papers.<Slug>.Paper` to cache the olean — keep `_lake_build_paper_module` in sync if you change how Paper.lean is written.
- The orchestrator extracts the declaration from `Blocks/<lean_name>.lean` with `_extract_declarations` (strips imports/banners) and appends to `Paper.lean`. `_has_real_declaration` rejects sessions that only left an `import` line.

---

## §3 Orchestrator CLI — paste-ready

Always invoke with `python -X utf8` (the orchestrator emits unicode; Windows consoles fall over otherwise).

```bash
python -X utf8 -m src.formalization.orchestrator <paper.tex> \
  --title "<Paper Title>" \
  [--blocks-range "1-13" | "5,7-9" | "10"] \
  [--no-resume] \
  [--standalone] \
  [--parent-project lean_project] \
  [--base-dir lean_papers] \
  [--setup-mathlib] \
  [--dry-run] \
  [--json]
```

Defaults — [src/formalization/orchestrator.py:949-971](../src/formalization/orchestrator.py#L949-L971):

- `--parent-project` defaults to `./lean_project` if it exists (sentinel `"<default>"` resolution at line 738). Use `--standalone` to opt out and create an isolated project under `--base-dir` (legacy, slower to maintain).
- Resume is **on by default**. Blocks already `verified` or `axiom` in `PAPER_INDEX.md` are skipped.
- `--blocks-range` indexes the **formalizable** blocks 1-based, not the parser's raw block list.

### Test entry points

| Command | What it does |
|---|---|
| `pytest tests/` | Full test suite. |
| `pytest -m "not live"` | Skip tests that hit Leandex / Semantic Scholar / ArXiv / Anthropic. |
| `python tests/test_orchestrator.py` | Orchestrator dry-run only (no Claude CLI). |
| `python tests/test_orchestrator.py --real` | Full e2e — needs Claude CLI + cached Mathlib. |
| `python src/parser/parse_tex.py <file.tex> --stats` | Parser CLI. |

### Subprocess sentinels

- `run_claude` exit code `99` → Anthropic rate-limit / quota exhausted. Orchestrator surfaces this as `RATE_LIMITED` ([orchestrator.py:345](../src/formalization/orchestrator.py#L345)).
- Session-end markers Claude must emit: `END_REASON:COMPLETE` (success) or `END_REASON:LIMIT`.

---

## §4 Helper CLIs — [scripts/formalization/](../scripts/formalization/)

Reach for these before writing a one-off. All resolve repo root automatically; run from the repo root with `python scripts/formalization/<name>.py`.

| Script | Purpose |
|---|---|
| `diagnose_thesis.py` | Parser-only `.tex` diagnostic (no Claude). |
| `list_thesis_blocks.py` | List formalizable blocks with context. |
| `audit_refs.py` / `audit_refs2.py` | `\ref` vs label audit. |
| `rebuild_state.py` | Rebuild `Paper.lean` + `PAPER_INDEX.md` from existing `Blocks/`. |
| `cleanup_failed.py` | Remove `failed` entries from index + markers from `Paper.lean`. |
| `promote_block.py` / `promote_block_v2.py` | Mark a block verified without calling Claude. |
| `smoke_dry_run.py` | Dry-run smoke test with `--blocks-range`. |
| `manual_resume_full.py` / `manual_resume_range.py` | Resume-mode manual checks (not pytest). |
| `debug_check_lean.py` / `debug_check_parallel.py` / `debug_encoding.py` | Subprocess + `lake env lean` debugging. |
| `bench_claude_overhead.py` | Micro-benchmark of the Claude CLI; pairs with [`scripts/formalization/bench_minimal.lean`](../scripts/formalization/bench_minimal.lean). |

---

## §5 Design decisions to NOT relitigate

Each item is a temptation followed by the rejection reason.

- **Adding a SQLite / Postgres layer "to track formalization state"** → No. `PAPER_INDEX.md` + `REVIEW.md` + `Paper.lean` *are* the design: per-paper, human-readable, the agent reads them as context. (CONTEXT.md, ARCHITECTURE.md)
- **Splitting Sketch into a separate proof agent (Numina-style)** → No. AViD deliberately diverges: one agent formalizes statement + proof together using `proof_latex` as the guide.
- **Refactoring scripts under `src/formalization/scripts/`** → Those are vendored from `vendor/numina-lean-agent` (git submodule). Treat them as upstream — prefer not to fork. Reserved sentinels and exit codes live there.
- **Relaxing the "no `sorry` in `Paper.lean`" rule** → No. `axiom` is the escape hatch, and only with a `-- source: ...` comment for results not findable in Mathlib.
- **Using `ℕ` / `ℤ` / `⟨ ⟩` in Lean identifiers** → No. Use ASCII (`Nat`, `Int`). `lean-lsp-mcp`'s diagnostic parser computes column offsets that break on multi-byte unicode in source.
- **Adding a `proof_agent` or `pre_analysis_llm` module** → Deferred. The Sketch Agent handles statement+proof together; if the parser misses inline auxiliary lemmas, the right answer is to request a structured paper, not a new agent. Don't add speculative scaffolding.
- **Removing the "unused" params on `NoveltyChecker.__init__`** (`lean_project_path`, `threshold_type_tree`) → They are reserved for Stages 4–5 and kept for forward-compat. Leave them.
- **Letting the Claude session edit `Paper.lean` or `PAPER_INDEX.md` directly** → No. The orchestrator owns those files. The session edits its `Blocks/<lean_name>.lean` only. The agent silently dropping work into the wrong file was a real past failure mode this rule guards against.
- **Auto-formatting / mass-rewriting prompts under `prompts/`** → The mandatory search-order encoded in those prompts (`PAPER_INDEX.md` → `lean_local_search` → `lean_leandex` → `lean_loogle`) is load-bearing. Preserve it when editing.
