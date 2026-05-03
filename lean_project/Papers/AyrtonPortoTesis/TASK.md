# Current Block

- **Label**: def:filtro
- **Type**: definition
- **Title**: 
- **Lean name**: `def_filtro`
- **Target file (EDIT THIS, AND ONLY THIS)**: `Blocks/def_filtro.lean`
- **Paper module imported by the target**: `Papers.AyrtonPortoTesis.Paper`

## File editing rules (CRITICAL)

You MUST follow these rules. Violating them silently drops your work.

1. Edit ONLY `Blocks/def_filtro.lean`. This is YOUR file for this session.
2. NEVER edit `Paper.lean`. It is read-only context with the blocks
   already proven in this paper. The orchestrator will append your
   declaration to `Paper.lean` automatically AFTER this session.
3. NEVER edit `PAPER_INDEX.md`. The orchestrator updates it.
4. Keep the existing `import Papers.AyrtonPortoTesis.Paper` line at the top of the
   target file. That import gives you access to all dependencies
   listed below by their Lean names.
5. The body of `Blocks/def_filtro.lean` should be ONE main declaration
   (`def_filtro`) plus optional helper lemmas above it.

## Dependencies you can call (already in `Paper.lean`)

(none)

## Informal statement

Sea \( \mathbb{L}=(L,\wedge,\vee) \) un retículo. 
Un subconjunto no vacío \( F \subseteq L \) se llama filtro si satisface:
\begin{enumerate}[\normalfont (1)]
 \item \( F \) es creciente con respecto al orden de \( \mathbb{L} \);
 \item si \( a,b \) pertenecen a \( F \), entonces \( a\wedge b \) también pertenece a \( F \)
 (es decir, \( F \) es cerrado bajo ínfimos).
\end{enumerate}
Un filtro \( F \) se dira propio si $F \neq L$, es decir, está propiamente contenido en \( L \).

## Informal proof

(no proof provided in paper)

## Workflow

1. (HARD mode only) Read `docs/prompts/avid_common.md` and `docs/prompts/avid_sketch_agent.md`.
2. Open `Blocks/def_filtro.lean` and add your declaration(s).
3. Verify with `lean_diagnostic_messages(file_path="Blocks/def_filtro.lean")`.
4. Iterate until there are no severity-1 errors and no `sorry`.
5. End your response with `END_REASON:COMPLETE` (success) or `END_REASON:LIMIT`.
