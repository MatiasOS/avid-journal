# Revisión de literatura: medición de novedad matemática

**Investigación exhaustiva para la sección de Related Work del preprint de AViD Journal**

Esta revisión cubre siete ramas: (1) el baseline ingenuo que AViD supera, (2) la motivación pública del problema, (3) novedad bibliométrica, (4) premise selection, (5) estructura de pruebas y grafos de dependencia, (6) autoformalización y su fragilidad, (7) nociones teóricas de novedad. Al final, la síntesis del hueco que ocupa AViD.

---

## Rama 1 — El baseline que AViD supera: "novedad = ausencia del corpus"

**Kasaura et al. — *Discovering New Theorems via LLMs with In-Context Proof Learning in Lean*** (arXiv:2509.14274, sept 2025).
Generan teoremas nuevos con un Conjecturing-Proving Loop. Definen novedad como: *"la conjetura no está ya en Mathlib4, ni en la librería generada, ni en la lista del conjeturador"*. Es decir, **novedad = no-presencia**, sin filtro de trivialidad ni distancia estructural. Es el competidor más directo de AViD y el baseline que se supera.

**Synthetic Theorem Generation in Lean** (OpenReview EeDSMy5Ruj).
Generación sintética de teoremas por forward-reasoning desde estados de prueba existentes.

**Mining Math Conjectures from LLMs: A Pruning Approach** (arXiv:2412.16177).
Reportan el problema inverso: redundancia en conjeturas generadas, *"GPT-4 usualmente produce el mismo tipo de lemas 'genéricos' cada vez"*. Atacan con pruning heurístico, no con métrica formal.

## Rama 2 — El problema reconocido como ABIERTO (motivación del paper)

**Abouzaid et al. — First Proof** (arXiv:2602.05192, febrero 2026).
Once matemáticos de primer nivel (incluido un Fields Medal) lanzaron un examen de matemática para AI con problemas no publicados. Punto clave: *"los LLMs tienen tendencia a encontrar pruebas existentes y olvidadas en lo profundo de la literatura matemática y presentarlas como originales; una de las pruebas recientes de Axiom Math, por ejemplo, resultó ser un resultado de búsqueda en la literatura tergiversado"*. First Proof testea sus preguntas en LLMs para asegurar que ninguna respuesta exista en datos de entrenamiento.

**Cita motivante (SecZine sobre First Proof):** *"hemos construido modelos que pueden parsear papers y extraer lemas; lo que nos falta es una manera sistemática de evaluar si esos lemas pueden ensamblarse en una prueba novedosa"*. Es casi la definición de AViD.

## Rama 3 — Novedad bibliométrica (campo adyacente que no alcanza)

**Uzzi, Mukherjee, Stringer, Jones — *Atypical Combinations and Scientific Impact*** (Science, 2013).
17.9 millones de artículos analizados. Encuentran que la ciencia de mayor impacto se basa en combinaciones excepcionalmente convencionales de trabajo previo pero con intrusión de combinaciones inusuales. Miden novedad como combinaciones atípicas de revistas citadas.

**Wang, Veugelers, Stephan (2017).** Novedad como primera aparición de una combinación de conocimientos en Web of Science.

**Boyack & Klavans (2014).** Crítica: los indicadores de Uzzi están confundidos por efectos disciplinarios (física vs. multidisciplinario, etc.).

**Measuring novelty in science with word embedding** (PLOS ONE, corrección 2026).
Validación de medidas bibliométricas de novedad con embeddings de título/abstract/keyword.

**Por qué no alcanza para AViD:** toda esta rama mide novedad *externamente* (citaciones, co-ocurrencia de revistas) y **nunca mira el contenido deductivo de la prueba**. Un paper puede citar fuentes atípicas y probar algo trivial, o citar fuentes convencionales y dar una prueba nueva. Bibliometría no distingue.

## Rama 4 — Premise selection (fundamento técnico del eje 2)

**Sledgehammer** (Paulson y Blanchette, línea Isabelle). Mecanismo clásico.

**MePo (Meng-Paulson)** y **MaSh** (Machine learning for Sledgehammer). Heurísticas y ML temprano.

**DeepMath** (Google, 2016). Primer uso serio de deep learning para premise selection.

**Mikuła, Jiang, Wenda Li et al. — Magnushammer** (ICLR 2024).
*"Premise selection con entrenamiento contrastivo y transformers que supera a Sledgehammer, logrando 59.5% contra 38.3% en PISA y 34.0% contra 20.9% en miniF2F"*. Wenda Li es coautor — citarlo bien es hablar su idioma.

**Piotrowski et al. — Machine-Learned Premise Selection for Lean** (arXiv:2304.00994).
Crítico para implementación de AViD. Muestra cómo *"tomar una prueba en Lean como string y listar las premisas que aparecen ahí"* e introduce un math filter que *"preserva solo lemas de naturaleza claramente matemática, descartando los básicos y técnicos, usando los nombres de teoremas y definiciones de mathlib como whitelist"*.

**Piotrowski & Urban — Stateful premise selection.** Iteración sobre el estado de prueba.

**ReProver / LeanDojo (Yang et al.).** Retrieval-augmented theorem proving en Lean.

**Cómo se diferencia AViD:** premise selection usa "qué premisas son relevantes" como *input para construir* una prueba. AViD usa "qué premisas usó una prueba ya hecha" como *huella para comparar* dos pruebas. Mismo objeto, dirección inversa, propósito nuevo.

## Rama 5 — Estructura de pruebas, grafos de dependencia y similitud

**Yoo — *The Axiom-Based Atlas*** (arXiv:2504.00063, abril 2025).
**Competidor más cercano a vigilar.** Representa teoremas como proof vectors sobre sistemas de axiomas fundacionales. Mapea dependencias lógicas a vectores indexados por axiomas. Define métricas de similitud cuantitativas como distancia coseno entre resultados matemáticos. Compara con similitud coseno, distancia euclidiana o índice de Jaccard.

**Diferencia con AViD:** el Atlas es para *visualizar y organizar* el conocimiento matemático por estructura lógica; AViD usa la estructura de premisas para *chequear novedad contra un corpus que incluye literatura informal vía autoformalización*. El propósito (novelty-checking activo) y el alcance (corpus formal + informal) son distintos, pero la herramienta es pariente. NO esconder: posicionarse respecto a él explícitamente.

**Aspinall et al. — Towards Formal Proof Metrics** (Springer).
Definir métricas de prueba por analogía con métricas de software, partiendo de métricas de diseño orientado a objetos (acoplamiento, cohesión, etc.).

**Huch — Structure in Theorem Proving** (TUM, arXiv:2209.13305).
Analiza el grafo de dependencias del Archive of Formal Proofs. Encuentra distribución scale-free del grado de entrada. Útil si AViD quiere pesar premisas por rareza.

**Dependency Graphs for Interactive Theorem Provers.** Visualización de dependencias.

**Supporting Maintenance of Formal Mathematics with Similarity Search** (Springer 2024).
Detección de clones en pruebas formales, refactoring.

**Metrics for Graph Comparison: A Practitioner's Guide** (PLOS One).
Menú de distancias entre grafos si se quiere ir más allá de Jaccard.

## Rama 6 — Autoformalización y su fragilidad (debilidad ya reconocida)

**Wu et al. — Autoformalization with Large Language Models** (NeurIPS 2022). Paper fundacional.

**ProofFlow** (Huawei AI4Math, arXiv:2510.15981).
Enfoque de grafo de dependencias con lemas intermedios para preservar la estructura lógica del argumento original. Introduce **PROOFSCORE**, métrica compuesta para evaluar corrección sintáctica, fidelidad semántica y fidelidad estructural.

**Aria** (arXiv:2510.04520).
Aborda que *"los LLMs generan código inválido con funciones inexistentes en Mathlib o incompatibles con toolchains que evolucionan rápido"*. Justo el riesgo del paso de traducción de AViD.

**Conjecturing: An Overlooked Step in Formal Mathematical Reasoning** (arXiv:2510.11986).
*"El desempeño de autoformalización está sustancialmente sobreestimado cuando se tiene en cuenta la conjetura"*. Tratar el conjeturar como tarea independiente.

**Patel — A New Approach Towards Autoformalization** (arXiv:2310.07957). LLMs para formalización con few-shot.

## Rama 7 — Nociones teóricas de novedad (para Future Work)

**Neel Somani — Reflexiones sobre autoformalización y novedad.**
Propone medir la **complejidad mínima requerida para expresar una prueba**: si una prueba solo reconfigura teoremas existentes con nuevos parámetros, carece de novedad; si necesita crear múltiples teoremas nuevos no triviales, probablemente representa un avance genuino. También: inspirarse en **zero-knowledge proofs**, definiendo el "conocimiento" matemático como la capacidad de reconstruir una prueba usando resultados existentes en tiempo polinomial. Identifica la ausencia de una **métrica de closeness** como gap clave.

**Reverse mathematics** (Friedman, Simpson). Medir la fuerza lógica de un teorema. Ángulo alternativo de novedad.

## Síntesis: el hueco que ocupa AViD

Cuando se junta todo, el mapa queda claro:

- La **bibliometría** mide novedad por metadatos de citación, nunca por contenido de prueba.
- El **premise selection** extrae premisas pero para construir pruebas, no para compararlas.
- El **Axiom-Based Atlas** compara estructura de pruebas pero para organizar/visualizar, no para chequear novedad contra un corpus.
- El **conjecturing con LLMs** chequea novedad solo por ausencia de mathlib — el baseline con el bug de trivialidad.
- La **autoformalización** traduce informal a formal pero no evalúa si lo traducido es nuevo.
- **First Proof** documenta que el problema existe y es urgente, pero es un benchmark con evaluación humana, no un sistema automático.

**Nadie integra las tres dimensiones que AViD propone:** chequeo de existencia sobre corpus formal *e informal* + filtro de trivialidad vía tácticas + distancia estructural de premisas. Ese es el aporte defendible.

---

## Nota de honestidad intelectual

El Axiom-Based Atlas (Yoo 2025) es lo bastante cercano como para que un reviewer pregunte específicamente por él. La respuesta defendible: AViD no es "el Atlas con otro nombre" porque (a) el propósito es novelty-checking activo, no organización, y (b) el alcance del corpus incluye literatura informal vía autoformalización, no solo el formal ya existente.
