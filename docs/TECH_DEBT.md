# Deuda Técnica

## Limpieza de LaTeX y semántica matemática

### Issue: `\/` y otras macros de operadores en lógica algebraica

La función `strip_latex_for_query` elimina `\/` y otros comandos LaTeX
no-alfanuméricos. Esto es CORRECTO para queries a search engines
(Semantic Scholar, ArXiv search), que no entienden símbolos matemáticos
y operan sobre palabras.

Sin embargo, `\/` en papers de lógica algebraica, teoría de reticulados,
y dualidad usualmente representa join / supremo generalizado (∨), 
NO italic correction. Confirmado en arXiv:2404.13480 (álgebras condicionales).

### Implicancia para módulo de paráfrasis (futuro Stage 2 enhancement)

Cuando se implemente el módulo de paráfrasis (teorema LaTeX → 
lenguaje natural mediante LLM), será CRÍTICO preservar la semántica
matemática de estos operadores. La paráfrasis necesita "ver" la
estructura matemática, no texto limpiado.

Decisión: la paráfrasis NO debe usar `strip_latex_for_query`. Debe
operar sobre el LaTeX crudo, dejando que el LLM interprete los
operadores en contexto.

### Macros comunes a tener en cuenta

- `\/` → join / supremo (∨)
- `\wedge`, `\/\` → meet / ínfimo (∧)
- `\sqcup`, `\sqcap` → operaciones de reticulados
- Macros personalizadas con `\newcommand` definidas por autor
