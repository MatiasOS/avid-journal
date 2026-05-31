# Bitácora de decisiones de diseño

**Propósito:** registrar cada decisión de diseño no trivial del proyecto AViD Journal, con fecha, alternativas consideradas, y el porqué de la elección. Cuando un reviewer (o Wenda Li, o un supervisor de PhD) pregunte "¿por qué decidiste X?", la respuesta está acá.

**Formato sugerido por entrada:**
- **Fecha** (YYYY-MM-DD)
- **Decisión** (qué se decidió, en una oración)
- **Alternativas consideradas** (qué otras opciones había)
- **Razonamiento** (por qué se eligió esta)
- **Reversibilidad** (qué tan caro sería cambiar después)

---

## Decisiones tomadas durante el diseño del sprint (pre-Día 3)

### 2026-05-XX — Métrica de novedad como conjunción de tres dimensiones independientes

**Decisión:** definir novedad como conjunción de (D1) no-existencia previa, (D2) no-trivialidad, (D3) distancia estructural de pruebas.

**Alternativas consideradas:**
- Solo D1 (el baseline de Kasaura et al.): rechazado porque marca "suma de 4 pares" como novedoso.
- D1 + D2 sin D3: rechazado porque no captura "misma afirmación, prueba nueva".
- Métrica única continua en lugar de tres binarias: rechazado por dificultad de interpretación y calibración.

**Razonamiento:** las tres dimensiones miden cosas conceptualmente independientes y los modos de falla son distintos. Combinarlas en un escalar único oculta información diagnóstica útil para el paper.

**Reversibilidad:** alta. Se puede agregar D4 más adelante o reformular D3 sin tocar las otras.

### 2026-05-XX — Distancia de Jaccard sobre conjuntos de premisas para D3

**Decisión:** medir distancia entre pruebas como `1 - |P(π₁) ∩ P(π₂)| / |P(π₁) ∪ P(π₂)|`.

**Alternativas consideradas:**
- Distancia coseno sobre vectores TF-IDF de premisas: más sofisticada pero introduce un parámetro extra (IDF requiere corpus de referencia).
- Distancia sobre grafos de dependencia completos (no solo conjuntos): más fina pero mucho más cara de calcular.
- Edit distance sobre términos de prueba como árboles de sintaxis: frágil, ruido de formalización.
- Homotopía entre términos: rechazado por proof irrelevance en `Prop` (los términos colapsan).

**Razonamiento:** Jaccard es simple, sin parámetros libres adicionales, geométricamente interpretable, y la literatura cercana (Axiom-Based Atlas de Yoo) la usa. Las mejoras (IDF, grafos) son trabajo futuro declarado.

**Reversibilidad:** media. La función de distancia es modular; cambiarla no toca el resto del pipeline.

### 2026-05-XX — Filtro de trivialidad vía tácticas estándar (no por presencia en mathlib)

**Decisión:** D2 corre tácticas `T_auto = {decide, omega, simp, norm_num, aesop, tauto}` sobre el enunciado. Si alguna lo cierra → trivial.

**Alternativas consideradas:**
- "Trivial = no está en mathlib": rechazado porque colapsa trivialidad con ausencia (mathlib contiene teoremas profundísimos).
- "Trivial = prueba corta (pocas líneas)": rechazado porque la longitud no refleja dificultad matemática.

**Razonamiento:** las tácticas estándar son el proxy honesto de "cerrable sin idea". Sobre-aproxima (a veces `aesop` cierra cosas no triviales), pero el sesgo va hacia "no novedoso", que es el error seguro.

**Reversibilidad:** alta. Agregar o quitar tácticas de `T_auto` es trivial.

### 2026-05-XX — AViD autoformaliza el par teorema-demostración, no solo el enunciado

**Decisión:** el sistema autoformaliza tanto `τ` como `π`. La evaluación se hace end-to-end.

**Alternativas consideradas:**
- Formalizar a mano los teoremas del eval set: rechazado porque oculta el eslabón más frágil del sistema (la traducción).
- Autoformalizar solo el enunciado y dejar la prueba a un prover externo: rechazado por complejidad de coordinación en v1.

**Razonamiento:** evaluar lo que el sistema *realmente* va a hacer, no una versión idealizada. La fragilidad de la traducción se reporta como Capa 1 separada de la Capa 2 (clasificación), para no confundir errores de traducción con errores de métrica.

**Reversibilidad:** alta. Si en v2 conviene separar las etapas, se hace.

### 2026-05-XX — Eval set con 26 teoremas firmes + 9 slots TBD

**Decisión:** las categorías 2 (clásicos no en mathlib), 5 (literatura no formalizada) y 6 (teoremas muy nuevos) se llenan durante implementación, no a ciegas.

**Razonamiento:** poblar esas categorías exige verificar mathlib y arXiv en vivo. Inventar a ciegas contaminaría el ground truth.

**Reversibilidad:** trivial.

---

## Decisiones pendientes para resolver durante el sprint

- Valor inicial del umbral `θ` para D3. Empezar con 0.5 y calibrar contra T07/T08/T09.
- Implementación de `isDefEq` (D1 nivel 1) o quedarse con D1 nivel 0 sintáctico para v1.
- Si los tres pares estrella (T07/T08/T09) entran todos o si T09 queda en reserva.
- Stack de la web demo: Gradio (más simple) vs. Streamlit vs. Next.js (más profesional).

---

## Decisiones tomadas durante implementación

### 2026-05-31 — Preservar "generalization" y "specialization" del juez LLM como Caso 5 ("zona gris")

**Decisión:** los veredictos `generalization` y `specialization` que emite `llm_judge.judge_theorem_pair()` de `src/novelty/` no se descartan en `src/novelty_v2/`. Se mapean al Caso 5 de la matriz taxonómica de la spec ("tipos relacionados pero no iguales — zona gris que requiere revisión humana") y se exponen en el campo `revision_humana=True` del veredicto de salida.

**Alternativas consideradas:**
- Colapsar ambos en `NOVEDAD_ENUNCIADO`: rechazado — una generalización no es una afirmación nueva independiente; confunde el mensaje al usuario.
- Ignorarlos y relanzar la búsqueda: rechazado — descarta información valiosa del juez.

**Razonamiento:** la spec ya prevé este caso ("zona gris") y recomienda explícitamente no forzar etiqueta. El juez LLM ya distingue estos casos con alta precisión. Preservarlos respeta el diseño de la spec y enriquece la salida del demo (el usuario ve "este enunciado es una generalización de X — revisión humana sugerida").

**Reversibilidad:** alta. El campo `revision_humana` es aditivo; colapsarlo a otro veredicto en v2 es un cambio local en `types.py`.
