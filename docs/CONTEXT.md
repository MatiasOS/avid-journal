# AViD Journal — Context

## What

AViD Journal (Automated Verification in Demonstrations) is an automated mathematics journal. It accepts a `.tex` paper, parses out the mathematical blocks (definitions, theorems, lemmas, propositions, corollaries), formalizes each block in Lean 4 by driving Claude Code as a subprocess, verifies the result with Lean + Mathlib, and (in a separate pass) checks novelty against Mathlib and ArXiv.

The pipeline is: **Parser → Orchestrator → per-block Claude Code session → `lean_checker` → `Paper.lean` + `PAPER_INDEX.md` → optional Novelty Check**.

## Why

When AIs start discovering theorems autonomously, peer review at human speed becomes the bottleneck. AViD is a bet on the infrastructure side of that problem: automated verification (does the proof actually type-check?) and automated review (is the result new, or already in Mathlib / on ArXiv?). The journal is the wrapper that ties those two checks to a publish/reject decision.

A few non-obvious design choices that shape the rest of the codebase:

- **No separate proof agent.** Unlike Numina-Lean-Agent, AViD uses one agent (the Sketch Agent) that formalizes statement and proof together, guided by the informal `proof_latex` from the source paper.
- **`PAPER_INDEX.md` is the local theorem DB.** Each paper accumulates a markdown index of verified blocks, and the agent consults it *before* searching Mathlib. There is no SQL layer — markdown is the design, not a placeholder.
- **`sorry` is forbidden; `axiom` is the escape hatch.** Results not findable in Mathlib are declared as `axiom` with a `-- source: ...` comment. The orchestrator owns this fallback, not the agent.
- **One shared Lean project, one Mathlib build.** Each paper is a sub-module under `lean_project/Papers/<Slug>/`, not its own Lean project — they share oleans.

## Where to go from here

| If you want… | Read |
| --- | --- |
| The module-level architecture and data flow | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Setup, install, and how to actually run the orchestrator | [QUICKSTART.md](QUICKSTART.md) → [GUIA_INSTALACION_Y_USO.md](GUIA_INSTALACION_Y_USO.md) |
| Status of each component (done / in progress / planned) | [PROGRESS.md](PROGRESS.md) |
| Worked LaTeX → Lean examples | [examples/README.md](../examples/README.md) |
| Helper CLI scripts | [scripts/formalization/README.md](../scripts/formalization/README.md) |

Repo: <https://github.com/ayrtonporto/avid-journal>
