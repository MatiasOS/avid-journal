# AViD Journal — Context for AI Agent

## What is AViD Journal

AViD Journal (Automated Verification in Demonstrations) is an automated mathematics journal that:
1. Accepts `.tex` papers
2. Formalizes proofs in Lean 4
3. Verifies correctness
4. Checks novelty against Mathlib and ArXiv
5. Auto-publishes if valid

The motivation: when AIs discover theorems autonomously, they need automated verification and review infrastructure.

---

## Current State

### What is implemented
- `src/parser/latex_parser.py` — LaTeX parser that extracts mathematical blocks (theorems, lemmas, definitions, propositions, corollaries) with dependency graph
- `src/parser/parse_tex.py` — CLI for the parser
- `src/formalization/lean_project.py` — creates the Lean 4 project structure per paper, manages Paper.lean and PAPER_INDEX.md

### What is NOT implemented yet
- `src/formalization/orchestrator.py` — main orchestration loop
- `src/novelty/` — ArXiv novelty check (future)
- `src/database/db.py` — persistence (future)
- `src/web/` — web interface (future)

---

## Architecture

```
paper.tex
    │
    ▼
[Parser] ← DONE
    │  extracts blocks: theorems, lemmas, definitions
    │  with dependency graph (topological order)
    ▼
[lean_project.py] ← DONE
    │  creates Lean project per paper
    │  initializes Paper.lean and PAPER_INDEX.md
    ▼
[Orchestrator] ← TO BUILD
    │  for each block in topological order:
    │  selects prompt mode based on complexity
    │  launches Claude Code via subprocess
    │  Claude Code formalizes block into Paper.lean
    │  updates PAPER_INDEX.md after each block
    ▼
[Paper.lean] — accumulates all verified blocks
[PAPER_INDEX.md] — local database of proven results
```

---

## Key Design Decisions

### Sequential and accumulative formalization
Blocks are processed in topological order (dependencies first). Each proven block is immediately available for subsequent blocks via PAPER_INDEX.md and lean_local_search.

### Block types and treatment
| Type | Has proof | Treatment |
|------|-----------|-----------|
| `definition` | No | Direct Lean translation, verify compiles |
| `theorem` / `lemma` / `proposition` / `corollary` | Yes | Formalize statement + proof together using proof_latex as guide |
| Any block with `proof_latex = null` | No | Search Mathlib → if not found, declare as `axiom` with source comment |

### No Proof Agent — Sketch Agent does everything
Unlike Numina (which separates sketch and proof agents), in AViD the agent formalizes statement AND proof together, guided by the informal proof from the paper.

### sorry policy
- `sorry` → FORBIDDEN in final Paper.lean
- `axiom` → ONLY for external results not found in Mathlib (always with source comment)

### External results (no proof in paper)
1. Search Mathlib with lean_leandex
2. If found → import and name explicitly
3. If not found → declare as axiom with bibliographic reference

### Nested auxiliary lemmas
If a proof contains inline auxiliary lemmas, the parser may not capture them. In that case, we request structured paper format. Pre-analysis LLM is deferred.

---

## PAPER_INDEX.md — Local theorem database

This is the key innovation. Each paper has a PAPER_INDEX.md that accumulates proven results. The agent MUST consult this before searching Mathlib.

Format:
```markdown
## label:name — Title
Type: definition | theorem | lemma | proposition | corollary
Status: ✅ verified | ⚠️ axiom | ❌ failed
File: Paper.lean:N
Depends on: label1, label2 | —
Source: [Author, Year]  (only for axiom)
Statement: Brief informal statement...

---
```

### Mandatory search order for the agent
1. PAPER_INDEX.md → results already proven in THIS paper
2. lean_local_search → find block by name in Paper.lean
3. lean_leandex → semantic search in Mathlib
4. lean_loogle → type pattern search in Mathlib

---

## Prompt Strategy (based on Numina-Lean-Agent)

The formalization uses Claude Code CLI as subprocess, exactly like Numina. Three prompt modes:

| Mode | When to use |
|------|-------------|
| `prompt_avid.txt` | Simple blocks: short definitions, direct corollaries |
| `prompt_medium_mode_avid.txt` | Theorems with proof present but complex |
| `prompt_hard_mode_avid.txt` | Very hard theorems, activates Coordinator + subagents |

The orchestrator selects the mode based on block complexity.

Files in `prompts/`:
- `prompt_avid.txt` ← done
- `prompt_medium_mode_avid.txt` ← done
- `prompt_hard_mode_avid.txt` ← TO DO
- `docs/prompts/avid_coordinator.md` ← TO DO (adapted from Numina's coordinator.md)
- `docs/prompts/avid_blueprint_agent.md` ← TO DO (adapted from Numina's blueprint_agent.md)

---

## Numina-Lean-Agent Integration

AViD uses Numina's execution infrastructure without modification:
- `scripts/run_claude.py` — CLI that launches Claude Code on a target
- `scripts/runner.py` — execution engine, handles rounds and END_REASON
- `scripts/task.py` — TaskMetadata and TaskResult definitions
- `scripts/lean_checker.py` — verifies .lean files
- `scripts/statement_tracker.py` — detects if agent modified theorem statements
- `scripts/extract_sublemmas.py` — Lean code parser

These scripts are copied from Numina unchanged into `src/formalization/scripts/`.

---

## Local Environment (Windows)

- Claude Code CLI: installed via npm
- Lean 4: v4.29.0 via elan
- lean-lsp-mcp: installed at `D:\Mis documentos\Documentos\tools\lean-lsp-mcp`
  - run_server.py wrapper at that location
  - registered with `--scope user` in Claude Code
- Lean project with Mathlib: `lean_project/` inside AViD Journal repo (for testing)
- uv: installed via winget

### Windows encoding note
Use `Nat` instead of `ℕ` in Lean code — Unicode causes column offset issues in lean-lsp-mcp diagnostic parser.

---

## What to build next

1. `prompt_hard_mode_avid.txt` — adapted from Numina's hard mode
2. `prompts/docs/avid_coordinator.md` — coordinator prompt adapted for AViD
3. `prompts/docs/avid_blueprint_agent.md` — blueprint agent adapted for AViD
4. `src/formalization/orchestrator.py` — main pipeline loop
5. End-to-end test with a sample paper

---

## Repo
github.com/ayrtonporto/avid-journal
