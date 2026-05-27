# lean_project

Shared Lean 4 project that hosts every paper AViD formalizes as a sub-module. Mathlib is built **once** here; each paper reuses the cached oleans instead of getting its own Mathlib.

## Layout

```
lean_project/
├── lakefile.toml          # toolchain + Mathlib + library declarations
├── lean-toolchain         # pinned Lean version
├── LeanProject.lean       # default library entry point
└── Papers/
    └── <ModuleName>/      # one sub-module per formalized paper
        ├── Paper.lean             # cumulative module (orchestrator-owned)
        ├── PAPER_INDEX.md         # per-block log (status, line, deps)
        ├── REVIEW.md              # axioms / failures / human-review notes
        ├── Blocks/<lean_name>.lean # per-block file (edited by Claude)
        ├── TASK.md                # current block context (orchestrator-written)
        └── docs/prompts/          # agent prompts copied for the session
```

The Lean module path for a paper is `Papers.<ModuleName>.Paper`.

## Setup

Install Lean via [elan](https://leanprover-community.github.io/get_started.html). The toolchain pinned in [lean-toolchain](lean-toolchain) takes precedence over any system Lean.

One-time Mathlib build (slow the first time, fast afterwards):

```bash
cd lean_project
lake update
lake build
```

`.lake/` (build artifacts, including Mathlib's `.olean` files) is gitignored.

## Working with a paper

A paper at `Papers/<ModuleName>/` is built like any other Lean library target:

```bash
lake build Papers.<ModuleName>.Paper
```

The orchestrator runs this automatically after every verified block so the next block's verification reads cached oleans.

## Pointers

- [docs/GUIA_INSTALACION_Y_USO.md](../docs/GUIA_INSTALACION_Y_USO.md) — full install + usage walkthrough (Spanish)
- [examples/README.md](../examples/README.md) — worked examples (TinyEvensPaperReal, AyrtonPortoTesis) with the LaTeX source and the formalized Lean checked in
