# `paper/` — investigación y preparación del preprint de AViD Journal

Esta carpeta vive dentro de `D:\Mis documentos\Documentos\AViD Journal\` y centraliza todo el trabajo de investigación, diseño de la métrica, evaluación, redacción del preprint y outreach asociado al proyecto.

El código del pipeline AViD vive afuera, en la carpeta raíz del proyecto. **Acá solo viven los documentos.**

---

## Archivos en la raíz de `paper/`

### Documentos de diseño (la base de todo)

- **`metric_spec.md`** — Especificación formal de la métrica de novedad. Tres dimensiones, árbol de decisión, limitaciones declaradas. Es el documento de referencia para implementación y para la sección de metodología del preprint.

- **`eval_set.csv`** — Conjunto de evaluación con 26 teoremas firmes + 9 slots TBD que se llenan durante la implementación. Cada fila incluye enunciado informal, categoría, rama del árbol que testea, y etiqueta esperada.

### Material para el preprint

- **`related_work.md`** — Revisión de literatura organizada en siete ramas, con la síntesis del hueco que ocupa AViD. Es la base de la sección "Related Work" del paper.

- **`limitations.md`** — Lista declarada de limitaciones del framework y de la implementación v1. Se va llenando durante el sprint.

- **`future_work.md`** — Direcciones futuras (refinamientos de métrica, extensiones de alcance, investigación teórica). Material para la sección de Future Work y para la propuesta de PhD.

### Bitácoras del sprint

- **`decisions.md`** — Registro de cada decisión de diseño no trivial (qué, alternativas, por qué). Cuando alguien pregunte "por qué hiciste X", la respuesta está acá.

- **`results_log.md`** — Log día por día del sprint de 15 días. Qué se hizo cada día, qué quedó pendiente, qué resultados se obtuvieron.

### Outreach

- **`outreach.md`** — Estado de cada contacto profesional (supervisores de PhD, Heath/Metalogic, Axiom Math, comunidad Lean). Próximos pasos concretos para cada uno.

---

## Subcarpetas

### `preprint/`
- **`draft.md`** — Esqueleto del preprint con todas las secciones. Se va llenando desde el Día 13.
- **`abstract.md`** — Borradores e iteraciones del abstract.
- **`figures/`** — Carpeta para figuras del paper (diagramas, tablas, plots).

### `demo/`
- **`notes.md`** — Decisiones de diseño y pendientes del demo web Gradio (Días 10-12).

---

## Cómo trabajar con esta estructura

**Durante implementación (Días 3-12):** las dos bitácoras (`decisions.md` y `results_log.md`) se actualizan al final de cada día. No más de 5 minutos por día. Si no se actualizan, al Día 13 se pierde la mitad del contenido del paper.

**Durante redacción (Días 13-15):** se trabaja casi exclusivamente en `preprint/draft.md`, importando contenido de los documentos de la raíz.

**Después del sprint:** los `.md` se mantienen como documentación viva del proyecto. El `draft.md` se exporta a PDF para subir a arXiv u otro canal.

---

## Convenciones

- **Idioma:** los documentos internos pueden estar en español; el `preprint/draft.md` y los emails de outreach van en inglés.
- **Términos técnicos:** mantener en inglés (proof irrelevance, premise selection, autoformalization, etc.) aunque el documento esté en español.
- **Referencias bibliográficas:** formato consistente — autor + año + arXiv-id cuando aplica.
- **Compromisos con fecha:** las decisiones que tengan deadline van en `results_log.md` o `outreach.md`, no acá.

---

## Estado actual del sprint

*(Actualizar diariamente.)*

- **Día 1:** ✓ `metric_spec.md` completo.
- **Día 2:** ✓ `eval_set.csv` con 26 filas firmes + 9 TBD.
- **Día 3 en adelante:** pendiente.

---

## Contacto

**Autor principal:** Ayrton Porto — ayrporto@gmail.com — ayrtonporto.github.io
