# Scripts de formalización (AViD)

Utilidades de línea de comandos relacionadas con el pipeline LaTeX → Lean (`src/formalization/`). Todas resuelven la raíz del repositorio automáticamente; ejecútalas **desde la raíz del repo** (recomendado: `python scripts/formalization/<script>.py`).

| Script | Propósito |
|--------|-----------|
| `diagnose_thesis.py` | Diagnóstico del `.tex` de la tesis (parser, sin Claude). |
| `list_thesis_blocks.py` | Lista bloques formalizables con contexto. |
| `audit_refs.py`, `audit_refs2.py` | Auditoría de `\ref` / labels vs parser. |
| `detect_encoding.py` | Prueba encodings del `.tex` de la tesis. |
| `rebuild_state.py` | Reconstruye `Paper.lean` / `PAPER_INDEX.md` desde bloques existentes. |
| `cleanup_failed.py` | Limpia entradas `failed` en índice y marcadores en `Paper.lean`. |
| `promote_block.py`, `promote_block_v2.py` | Marca un bloque como verificado sin llamar a Claude. |
| `smoke_dry_run.py` | Smoke test dry-run con `blocks_range`. |
| `manual_resume_full.py`, `manual_resume_range.py` | Comprobaciones manuales de resume / rangos (no son tests pytest). |
| `debug_check_lean.py`, `debug_check_parallel.py`, `debug_encoding.py` | Depuración de `lake env lean` y subprocess. |
| `bench_claude_overhead.py` | Micro-benchmark de la CLI de Claude (genera `bench_minimal.lean` junto al script). |

Archivos auxiliares versionados aquí: `bench_minimal.lean`. Fixture Lean trivial: `tests/fixtures/mathlib_smoke.lean`.
