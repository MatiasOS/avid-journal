# Direcciones futuras de AViD Journal

**Propósito:** registrar todas las ideas, refinamientos y extensiones que NO entran en v1 pero que se mencionan en el preprint y/o son material para el PhD posterior. Cada entrada incluye breve descripción + por qué importa + nivel de dificultad estimado.

---

## Refinamientos de la métrica

### F1 — Premisas ponderadas por rareza (IDF)
**Idea:** en lugar de Jaccard puro, pesar cada premisa por su inverso de frecuencia en mathlib. Una premisa que aparece en 10 teoremas pesa mucho; una que aparece en 10.000 pesa poco.
**Por qué importa:** captura mejor la noción matemática de "premisa central vs. técnica".
**Dificultad:** baja-media. Requiere contar ocurrencias en mathlib (LeanDojo lo facilita).

### F2 — Distancia sobre grafos de dependencia
**Idea:** pasar de conjunto de premisas a grafo dirigido de dependencias. Comparar grafos con métricas más finas (cf. Metrics for Graph Comparison, PLOS One).
**Por qué importa:** dos pruebas pueden usar las mismas premisas pero combinarlas en órdenes muy distintos.
**Dificultad:** alta. Requiere extracción de estructura jerárquica de la prueba.

### F3 — Equivalencia de tipos definicional (D1 nivel 1)
**Idea:** usar `isDefEq` del kernel de Lean para detectar enunciados equivalentes hasta definitional unfolding.
**Por qué importa:** elimina la mayoría de falsos negativos sintácticos de v1.
**Dificultad:** media. Requiere interactuar con el kernel desde el pipeline Python.

### F4 — Equivalencia lógica más fuerte
**Idea:** intentar probar automáticamente `τ ↔ τ'` con tácticas. Más caro pero más fino que `isDefEq`.
**Por qué importa:** caso T22 del eval set (n + 0 = n vs. n = n) se resolvería.
**Dificultad:** media-alta. Indecidible en general; se debe acotar con presupuesto.

## Extensiones del alcance

### F5 — Novedad a nivel de artículo, no solo de teorema
**Idea:** agregar las decisiones teorema-a-teorema en un veredicto por paper. Métricas posibles: porcentaje de teoremas novedosos, novedad ponderada por "centralidad" del teorema.
**Por qué importa:** un paper puede ser nuevo aunque sus lemas individuales sean conocidos.
**Dificultad:** media. Requiere definir centralidad/peso.

### F6 — Detector de problemas abiertos
**Idea (ya parcialmente desarrollado):** identificar conjeturas no probadas mencionadas en la literatura. Modo "qué problemas valdría la pena formalizar".
**Por qué importa:** complementa novedad — si un teorema ataca un problema abierto reconocido, eso es señal fuerte de novedad.
**Dificultad:** media. Ya hay infraestructura inicial.

### F7 — Múltiples modelos de autoformalización
**Idea:** integrar Numina, Axiom, Kimina, ProofFlow como modelos intercambiables en la capa de autoformalización. AViD se vuelve agnóstico al traductor.
**Por qué importa:** desacopla la métrica del estado del arte de traducción. Cuando mejore la traducción, AViD mejora gratis.
**Dificultad:** media. Es trabajo de integración, no de investigación.

### F8 — Extensión a HoTT / fragmento univalente
**Idea:** para teoremas en `Type` (con relevancia de pruebas), usar homotopía verdadera en lugar de premisas como medida de distancia.
**Por qué importa:** cierra el caso conceptual que el documento de diseño dejó abierto.
**Dificultad:** alta. Requiere trabajo serio de teoría de tipos.

## Evaluación a escala

### F9 — Corrida sobre mathlib completa
**Idea:** procesar las ~1.9M de líneas de mathlib para construir el corpus C_F sistemáticamente y medir auto-consistencia (¿cuántos teoremas de mathlib detectaríamos como redundantes entre sí?).
**Por qué importa:** valida la métrica a escala. Posiblemente revele patrones interesantes (clusters de pruebas similares).
**Dificultad:** alta (computacional).

### F10 — Benchmark sobre corpus arXiv (autoformalizado)
**Idea:** correr AViD sobre un set grande de papers recientes y publicar tasas de "novedad genuina", "redundancia oculta", "trivialidad". Reporte estilo bibliométrico pero a nivel de prueba.
**Por qué importa:** habilita estudios sobre la novedad real de la producción matemática moderna.
**Dificultad:** muy alta. Limitada por autoformalización.

## Investigación teórica

### F11 — Conexión con complejidad de Kolmogorov / zero-knowledge
**Idea (vía Somani):** formalizar "novedad = complejidad mínima para derivar de premisas existentes". Conectar con teoría de complejidad.
**Por qué importa:** marco teórico unificador para varias dimensiones de novedad.
**Dificultad:** muy alta. Trabajo de tesis de PhD por sí solo.

### F12 — Reverse mathematics como medida de "profundidad" de un teorema
**Idea:** medir qué axiomas se usaron efectivamente (no solo qué premisas) para caracterizar la fuerza lógica del teorema.
**Por qué importa:** dimensión ortogonal a novedad — "qué tan profundo es" complementa "qué tan nuevo es".
**Dificultad:** alta. Requiere familiaridad con reverse mathematics.

---

## Direcciones de producto (post-paper)

### P1 — Integración con sistemas de submission de papers
Como capa adicional de revisión automática para journals de matemática asistida por computadora.

### P2 — Plugin para Lean / mathlib
Aviso temprano cuando un contribuidor intenta probar algo ya presente.

### P3 — Servicio para grandes laboratorios de AI matemática
Filtro de novedad pre-publicación (¿esto que mi modelo "descubrió" es realmente nuevo?). Mercado obvio: Axiom Math, Harmonic, Morph Labs.

### P4 — Integración de LeanDojo-v2 al demo público post-sprint
AViD chequea novedad, LeanDojo-v2 provee capacidad de prueba sobre los resultados marcados como novedosos. Pieza diferenciadora del demo público frente a otros checkers. La infraestructura WSL2 instalada durante el sprint (Día 3) queda disponible para esta integración sin trabajo adicional de setup.
