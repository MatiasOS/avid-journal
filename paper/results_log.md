# Log de resultados del sprint AViD Journal

**Sprint de 15 días para entregar:** demo web funcional + métrica de novedad con filtro de trivialidad + evidencia preliminar + preprint v1.

**Formato por día:** qué se hizo, qué quedó andando, qué quedó pendiente, qué decisiones aparecieron.

---

## Día 1 — Especificación escrita de la métrica ✓

**Hecho:** documento `metric_spec.md` completo. Tres dimensiones definidas. Árbol de decisión. Limitaciones declaradas.

**Pendiente:** ninguno.

**Decisiones nuevas:** ninguna (todas las decisiones de diseño fueron tomadas y registradas en `decisions.md`).

## Día 2 — Conjunto de evaluación ✓

**Hecho:** `eval_set.csv` con 26 teoremas firmes + 9 slots TBD. Cuatro categorías cubiertas: clásicos en mathlib, pares con distinta prueba (T07 Euclides/Euler, T08 √2 paridad/raíz racional, T09 Gauss inducción/emparejamiento), triviales, casos de falla.

**Pendiente:** llenar los 9 slots TBD durante implementación (clásicos no en mathlib, conocidos en literatura, teoremas muy nuevos).

## Día 3 — Setup de infraestructura

**Objetivo:** repo limpio con estructura de carpetas, README inicial, entorno reproducible, **LeanDojo corriendo sobre un ejemplo mínimo de mathlib**.

**Hecho:**

**Pendiente:**

**Bloqueos:**

## Día 4 — Filtro de trivialidad (D2)

**Objetivo:** módulo `triviality_filter.py` que toma un enunciado en Lean e intenta cerrarlo con `T_auto = {decide, omega, simp, norm_num, aesop, tauto}` + `exact?`. Output: bandera + táctica que lo cerró.

**Hecho:**

**Pendiente:**

**Resultados sobre eval set (preliminar):**

## Día 5 — Extracción de premisas con LeanDojo (parte 1)

**Objetivo:** función `get_premises(theorem) -> set[str]` corriendo sobre teoremas básicos.

**Hecho:**

**Pendiente:**

## Día 6 — Extracción de premisas con LeanDojo (parte 2)

**Objetivo:** extracción funcionando sobre los pares T07, T08, T09 + math filter (whitelist mathlib).

**Hecho:**

**Pendiente:**

## Día 7 — Eje 1: comparación de tipos (D1)

**Objetivo:** `type_compare.py` que decide si dos enunciados Lean tienen el mismo tipo (nivel 0 sintáctico tras normalización).

**Hecho:**

**Pendiente:**

## Día 8 — Distancia de Jaccard + integración de la métrica

**Objetivo:** `novelty_score.py` que toma un teorema y devuelve el veredicto combinado (las tres dimensiones).

**Hecho:**

**Pendiente:**

## Día 9 — Corrida sobre eval set + tabla de resultados

**Objetivo:** procesar las 26 filas firmes del eval set. Tabla con etiqueta esperada vs. veredicto real. Cálculo de accuracy por categoría.

**Hecho:**

**Resultados:**

| Categoría | Aciertos | Total | % |
| --- | --- | --- | --- |
| Clásicos en mathlib | | 6 | |
| Pares distinta prueba | | 6 | |
| Enunciados cercanos | | 5 | |
| Triviales | | 5 | |
| Generados por IA | | 3 | |
| Casos de falla | | 4 | |
| **Total** | | **29** | |

**Hallazgos importantes (para Limitations y Future Work):**

## Día 10 — Demo web (Gradio) backend

**Objetivo:** interfaz Gradio que toma un enunciado en lenguaje natural, lo autoformaliza, corre la métrica, y muestra veredicto + las tres sub-puntuaciones.

**Hecho:**

**Pendiente:**

## Día 11 — Pulido del demo + página de landing

**Objetivo:** página explicando la idea (matriz de cuatro casos, caso Axiom, qué hace AViD distinto) + demo embebido con ejemplos pre-cargados.

**Hecho:**

**Pendiente:**

## Día 12 — Deploy del demo

**Objetivo:** URL pública estable (Hugging Face Spaces o equivalente).

**URL del demo:**

## Día 13 — Draft del preprint

**Objetivo:** draft completo siguiendo la estructura de `preprint/draft.md`.

**Hecho:**

**Pendiente:**

## Día 14 — Figuras + pulido del paper

**Objetivo:** diagrama del pipeline, tabla de resultados, matriz taxonómica. Pasada final buscando afirmaciones débiles.

**Hecho:**

**Pendiente:**

## Día 15 — Preprint listo (no publicado todavía)

**Objetivo:** versión final en PDF lista para subir. Decisión de dónde/cómo publicar queda para después del sprint.

**Hecho:**

**Entregables finales:**
- `preprint/draft.md` (versión final)
- `preprint/AViD_novelty_preprint_v1.pdf`
- URL del demo
- Repo limpio

## Post-mortem del sprint

*(se completa el Día 15 o 16)*

**Qué salió bien:**

**Qué salió mal:**

**Qué cambiaría si lo hiciera de nuevo:**

**Próximos pasos:**
