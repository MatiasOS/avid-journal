# Briefing para Claude Code — AViD Journal sprint, Día 4 en adelante

**Este es tu primer mensaje. Leelo entero antes de cualquier acción.**

Sos Claude Code retomando un sprint de investigación ya en marcha. La sesión anterior (Día 3) cerró con setup de infraestructura completo y una reorientación arquitectural importante. Tu trabajo es continuar desde Día 4 sin que Ayrton tenga que repetir contexto.

---

## 1. Qué es AViD Journal

AViD Journal es un sistema automatizado para chequear la **novedad matemática** de teoremas formalizados en Lean 4. Recibe un paper `.tex`, lo parsea en bloques (definiciones, teoremas, lemas, proposiciones, corolarios), autoformaliza cada bloque a Lean usando Claude Code como subprocess, verifica con Lean, y luego — la parte central del sprint — clasifica la novedad de cada teorema contra un corpus compuesto por mathlib (formal) y arXiv + Semantic Scholar (informal). Stack: Python orchestrator + Lean 4 + LeanDojo + SQLite + Gradio (este último a construir).

El proyecto vive en `D:\Mis documentos\Documentos\AViD Journal\` (Windows) con clon de trabajo dentro de WSL2 en `/home/ayrton/avid-journal/` (filesystem nativo de Linux). El autor es **Ayrton Porto** (UNICEN, matemático argentino, Lean 4 nivel intermedio, no programador experimentado).

---

## 2. Qué es el sprint de 15 días

Sprint para producir simultáneamente **cuatro artefactos**:

- **A — Demo web público funcional** (Gradio + Hugging Face Spaces) con URL estable.
- **B — Métrica de novedad implementada** con sus tres dimensiones (D1, D2, D3) según `paper/metric_spec.md`.
- **C — Evidencia preliminar**: corrida sobre el eval set de `paper/eval_set.csv` (29 teoremas firmes + 9 TBD) con tabla de aciertos por categoría.
- **D — Preprint v1 listo** (no publicado) en `paper/preprint/draft.md`.

Los tres entregables son la **"credential mínima"** que permite a Ayrton mandar emails a tres supervisores potenciales de PhD (Wenda Li / Edinburgh, Sean Welleck / CMU, Floris van Doorn / Bonn) y al contacto Heath Sanchez (Metalogic Labs).

---

## 3. Decisiones arquitecturales clave

Cada una está expandida en `paper/decisions.md` con alternativas consideradas y reversibilidad. Acá la lista corta:

1. **Métrica = conjunción de 3 dimensiones independientes**: D1 (no-existencia), D2 (no-trivialidad), D3 (distancia estructural de premisas vía Jaccard). El veredicto final es uno de cinco (NOVEDAD_ENUNCIADO / NOVEDAD_DEMOSTRACION / CONOCIDO_LITERATURA / NO_NOVEDOSO_redundante / NO_NOVEDOSO_trivial) más ZONA_GRIS (Caso 5 de la matriz taxonómica).

2. **Camino B — adaptar el código a la spec, no al revés.** `src/novelty/` (la implementación previa de stages 0–3) **se congela y no se toca**. Se importa como dependencia externa desde `src/novelty_v2/`, que es la implementación nueva alineada con `paper/metric_spec.md`.

3. **Mapeo `generalization`/`specialization` del juez LLM al Caso 5 (ZONA_GRIS)**, no se descartan. Ver `types.py`.

4. **LeanDojo v1 para D3, LeanDojo-v2 para futura segunda capa del demo (P4 en `future_work.md`).** Son herramientas distintas con propósitos distintos, no versiones de la misma cosa.

5. **D3 NO está en el pipeline automático del demo.** Hallazgo del Día 3: LeanDojo traza dependencias transitivas, no archivos sueltos. Procesar un teorema cualquiera implica trazar todos los imports, lo que en el caso de Mathlib son horas. Por eso:
   - **D1 y D2 corren automáticamente en tiempo real** sobre cada teorema.
   - **D3 se ofrece a pedido** vía cola SQLite. Ayrton procesa offline en su WSL.
   - Para la evidencia del paper, D3 se mide manualmente sobre los pares estrella (T07, T08, T09) en Día 7.

6. **Demo es Versión 2 asíncrona incompleta**: pipeline end-to-end con streaming visual del progreso (no galería de ejemplos precomputados). Input: paper `.tex` completo. Output: tabla de teoremas con veredicto + botón "solicitar análisis fino" para D3.

---

## 4. Estado del repo y entorno

### Repo

- Working tree limpio en commit **`a0cbd05`** (último al cierre del Día 3 antes del commit de cierre que Ayrton mismo va a hacer).
- Ramas: solo `main`. Sincronizado con `origin/main` en GitHub (`ayrtonporto/avid-journal`).
- Si en el chat actual ya hay un commit posterior con mensaje `docs: end of Day 3 — pivot to real-time D1+D2, D3 manual`, ese es el HEAD de partida.

### Estructura

```
src/
├── parser/             ← LaTeX → bloques (funciona, no tocar)
├── formalization/      ← Lean pipeline existente (funciona, no tocar)
├── novelty/            ← Stages 0-3 vieja implementación (CONGELADA, importar como dependencia)
└── novelty_v2/         ← scaffold del sprint
    ├── __init__.py
    ├── types.py        ← 5 veredictos + ZONA_GRIS, dataclasses D1/D2/D3
    ├── README.md       ← relación con src/novelty/
    └── dimensions/
        ├── d1_existence.py    ← stub, implementar Día 7
        ├── d2_triviality.py   ← stub, implementar Día 4
        └── d3_premises.py     ← stub, implementar Días 5-6 (manual con LeanDojo)
```

### Entorno

- **WSL2 + Ubuntu 22.04** instalado en `D:\WSL\Ubuntu2204\`.
- **Usuario WSL:** `ayrton` con `systemd=true` en `/etc/wsl.conf`.
- **Repo clonado en:** `/home/ayrton/avid-journal/` (NO trabajar desde `/mnt/d/...` — performance de I/O es mala para Lean).
- **Venv:** `/home/ayrton/avid-journal/.venv/` (Python 3.10.12, pesa ~5.5 GB con torch+CUDA libs traídos por `sentence-transformers`).
- **Paquetes ya instalados en el venv:** todo `requirements.txt` (anthropic, arxiv, sentence-transformers, faiss-cpu, PyMuPDF, pytest…) + **lean-dojo 4.20.0** (pausado para uso manual del Día 7).
- **Lean:** elan 4.2.2 + toolchain `leanprover/lean4:v4.29.0` (único toolchain instalado).
- **SSH a GitHub:** key ed25519 en `~/.ssh/id_ed25519`, registrada en la cuenta `ayrtonporto`.

---

## 5. Plan reorganizado de los días 4 al 15

**Día 4 — D2 (filtro de trivialidad).**
Entregable: `src/novelty_v2/dimensions/d2_triviality.py` con función `is_trivial(theorem_lean_source, statement) → D2Result`. Genera `example : τ := by T` para cada táctica de `T_auto = {decide, omega, simp, norm_num, aesop, tauto}` + `exact?`, ejecuta `lean` con presupuesto de tiempo `b`, devuelve qué táctica cerró (si alguna). Probar sobre T14-T18 (triviales del eval set) + T23 (caso de falla esperado).

**Día 5 — Esquema D3 + LeanDojo offline setup.**
Entregable: script `scripts/d3/trace_mathlib_v4_29.py` que orquesta una corrida única (probablemente nocturna) de tracing de mathlib `v4.29.0` con LeanDojo, persistiendo el resultado a disco. NO lo ejecuta en este día — solo deja el script listo y verificado. Avisar a Ayrton antes de cualquier ejecución larga.

**Día 6 — Implementación D3 (sobre output de LeanDojo).**
Entregable: `src/novelty_v2/dimensions/d3_premises.py` con `compute_premise_distance(theorem_a, theorem_b) → D3Result`. Math filter (whitelist mathlib) + Jaccard. Sin LeanDojo embebido en el pipeline: lee resultados pre-trazados.

**Día 7 — D1 + corrida manual de D3 sobre pares estrella.**
Entregable A: `src/novelty_v2/dimensions/d1_existence.py` reusando `mathlib_checker.check_in_mathlib` (de v1) para C_F y `arxiv_search` + `block_comparator` + `llm_judge` para C_I. Mapeo de `generalization`/`specialization` a ZONA_GRIS.
Entregable B: ejecutar LeanDojo offline UNA VEZ sobre el `lean_project/` para extraer las premisas de T07/T08/T09 (Euclides vs Euler, paridad vs raíz racional, Gauss inducción vs Gauss emparejamiento). Calibrar umbral θ inicial = 0.5.

**Día 8 — Orquestador + árbol de decisión combinado.**
Entregable: `src/novelty_v2/orchestrator.py` con `evaluate(block) → NoveltyVerdict` siguiendo el árbol de la spec §6 (D2 → D1 sobre C_F → D1 sobre C_I → D3 sólo si match).

**Día 9 — Corrida sobre eval set + tabla.**
Entregable: script que procesa las 26 filas firmes (excluye 9 TBD), produce tabla aciertos/total por categoría. Llenar tabla en `paper/results_log.md`.

**Día 10 — Gradio backend + cola SQLite para D3.**
Entregable: app Gradio con input textarea (paper `.tex`) + streaming de progreso + tabla de salida. Endpoint asincrónico que encola pedidos de D3 en SQLite para procesar offline. Botón "solicitar análisis fino" por teorema.

**Día 11 — Landing + pulido visual.**
Entregable: bloques narrativos del demo (header, problema, demo interactivo, cómo funciona, footer) según `paper/demo/notes.md`. Ejemplos pre-cargados.

**Día 12 — Deploy.**
Entregable: URL pública estable (Hugging Face Spaces). Verificada con un par de inputs.

**Día 13 — Draft del preprint.**
Entregable: `paper/preprint/draft.md` lleno siguiendo el esqueleto. Importar de `metric_spec.md`, `related_work.md`, `limitations.md`.

**Día 14 — Figuras + pasada final.**
Entregable: diagrama pipeline, tabla resultados, matriz taxonómica. Caza de afirmaciones débiles.

**Día 15 — Preprint listo (no publicado).**
Entregable: PDF final en `paper/preprint/AViD_novelty_preprint_v1.pdf`.

---

## 6. Reglas de trabajo con Ayrton

1. **Antes de cualquier cambio importante, explicar qué vas a hacer y por qué.** No improvisar.
2. **Después de cada implementación, correr el código sobre el caso concreto y mostrar output real.** No "debería funcionar" — mostrar que funcionó.
3. **Si tenés dudas conceptuales (matemática o métrica), preguntar — no inventar.**
4. **Implementar SOLO lo pedido.** No agregar features, logging avanzado, tests exhaustivos ni reescrituras "para que quede más limpio" salvo pedido explícito. La spec define exactamente qué hace v1.
5. **Commits frecuentes con mensajes Conventional Commits.** Cada pieza que funciona, un commit.
6. **Marcar siempre hecho documentado vs. inferencia.** Esta regla es no-negociable: si decís algo basado en lo que leíste en una doc/archivo, citá la fuente. Si es inferencia tuya, decilo explícito ("inferencia mía"). Mezclar los dos sin marcar = pérdida de confianza.
7. **No corras procesos de larga duración (>1 min) sin avisar primero.** Estimar tiempo → avisar → esperar OK → ejecutar. LeanDojo en particular puede colgar la máquina (mathlib trace = horas). Sin excepciones.
8. **No uses `run_in_background` salvo que Ayrton lo pida explícitamente.** Procesos en background corrompieron el venv en Día 3.
9. **Actualizar `paper/results_log.md` al final de cada día** con 2-3 oraciones sobre qué se hizo, qué quedó, qué cambió.
10. **Registrar decisiones de diseño no triviales en `paper/decisions.md`** con el formato existente (fecha, decisión, alternativas, razonamiento, reversibilidad).
11. **Si aparece una limitación nueva durante implementación, agregarla a `paper/limitations.md`** con el formato existente (status, caso del eval set que lo documenta, impacto).
12. **No AI attribution en commits, PRs ni código generado.** Sin `Co-Authored-By: Claude`, sin "Generated with Claude Code". El código se lee como escrito por Ayrton.

---

## 7. Archivos clave en `paper/` — orden de lectura recomendado

1. `paper/metric_spec.md` — la spec formal de la métrica. **Fuente de verdad para implementación.** Cualquier cosa que la implementación haga distinto a esto requiere decisión registrada en `decisions.md`.
2. `paper/eval_set.csv` — 26 teoremas firmes + 9 TBD con etiqueta esperada por categoría.
3. `paper/decisions.md` — historial cronológico de decisiones de diseño. **Leer entero antes de proponer cambios arquitecturales.**
4. `paper/results_log.md` — log día por día. Estado actual al cierre del Día 3.
5. `paper/limitations.md` — qué reconocemos como limitación de v1.
6. `paper/related_work.md` — siete ramas de literatura + síntesis del hueco de AViD.
7. `paper/future_work.md` — F1-F12, P1-P4. Lo que NO entra en v1.
8. `paper/demo/notes.md` — diseño del demo Gradio (Días 10-12).
9. `paper/preprint/draft.md` — esqueleto del paper para los Días 13-15.

Adicional: `.claude/CLAUDE.md` del repo tiene instrucciones generales del proyecto (formato de commits, convenciones de unicode/Windows, módulos que no tocar, etc.). Leerlo también.

---

## 8. Eval set y pipeline existente

### Eval set (`paper/eval_set.csv`)

29 teoremas firmes ya escritos + 9 slots TBD que se llenan durante implementación. Categorías cubiertas:

- **clasico_en_mathlib** (T01-T06): √2 irracional, infinitos primos, TFC, Fermat pequeño, Pitágoras, suma de Gauss. Esperado: `NO_NOVEDOSO_redundante`.
- **par_distinta_prueba** (T07a/b Euclides/Euler, T08a/b paridad/raíz racional, T09a/b Gauss inducción/emparejamiento): **los pares estrella**. Esperado: `NOVEDAD_DEMOSTRACION`.
- **enunciados_cercanos_distintos** (T10-T13, T26): zona gris. Esperado: `NOVEDAD_ENUNCIADO` o revisión.
- **trivial** (T14-T17 + T18 como trampa de control). Esperado: `NO_NOVEDOSO_trivial`.
- **generado_IA** (T19-T21): casos motivantes. Etiqueta depende del caso.
- **caso_falla** (T22-T25): documentan falsos negativos esperados de D1 nivel sintáctico, falsos positivos de D2 con aesop, etc.

### Módulos existentes (NO modificar)

`src/novelty/` implementa stages 0-3 del pipeline viejo. Está en producción y se usa como dependencia desde `novelty_v2`. Tabla de reutilización en `src/novelty_v2/README.md`:

| Función importada | Uso en v2 |
|---|---|
| `mathlib_checker.check_in_mathlib()` | D1 sobre C_F |
| `arxiv_search.search_semantic_scholar/arxiv()` | D1 sobre C_I etapa A |
| `block_comparator` (MiniLM) | D1 sobre C_I etapa A |
| `llm_judge.judge_theorem_pair()` | D1 sobre C_I etapa B |
| `_cache.cache_or_fetch()` | caching compartido |

`src/parser/` y `src/formalization/` también funcionan y se usan upstream del pipeline de novedad. Tampoco tocar.

---

## 9. Cosas que NO hay que hacer

- **NO reescribir `paper/metric_spec.md` sin pedir.** Es el contrato del sprint con la realidad. Si encontrás algo que no cierra, traer a Ayrton, no editar la spec por tu cuenta.
- **NO tocar `src/novelty/`.** Se congeló por decisión. Se importa, no se modifica.
- **NO asumir que LeanDojo es parte del flujo automático del sprint.** Es offline-manual para D3 sobre pares estrella en Día 7. El demo público corre solo D1 + D2.
- **NO trabajar desde `/mnt/d/...` en WSL.** Performance de I/O es 5-10x peor que filesystem nativo. Todo en `~/avid-journal/`.
- **NO instalar paquetes en el venv con múltiples comandos `pip install` simultáneos en background.** Eso corrompió el venv en Día 3 (binarios `.so` truncados). Una operación por vez.
- **NO instalar PyPantograph, LeanDojo-v2, torch-CUDA explícitamente.** Lo que está, sirve. Lo que se agregue es decisión explícita.
- **NO agregar database layer (SQLite con esquema complejo, Postgres) más allá de la cola asincrónica simple para pedidos de D3.** El estado del proyecto vive en archivos markdown.
- **NO agregar attribution de Claude en commits ni en código.** Regla absoluta del proyecto.
- **NO usar `run_in_background` salvo pedido explícito de Ayrton.**

---

## 10. Cómo seguir — primer turno

En tu primer respuesta a Ayrton, hacé esto en orden:

1. Confirmá brevemente que leíste este briefing y los archivos clave (al menos `metric_spec.md`, `decisions.md`, `results_log.md`, y `src/novelty_v2/README.md` + `types.py`).
2. Resumí en **5-10 puntos** tu entendimiento del estado actual: objetivo, arquitectura, decisiones clave, qué hay implementado, qué viene en Día 4.
3. **Esperá aprobación de Ayrton antes de tocar código.** Aun si te parece que "el plan es claro", la regla 1 dice esperar.
4. Si encontrás contradicciones o cosas que no entendés, preguntá. No improvises.

Bienvenido al sprint.
