# Guía de instalación y uso — AViD Journal (formalización Lean)

Esta guía está pensada para que **cualquiera en otro equipo** pueda clonar el repo, instalar dependencias y ejecutar el pipeline de formalización (LaTeX → bloques → Claude Code → Lean + Mathlib).

---

## 1. Qué necesitas instalar (resumen)

| Componente | Para qué sirve |
|------------|----------------|
| **Git** | Clonar y versionar el proyecto |
| **Python 3.10+** (recomendado 3.11+) | Orquestador, parser LaTeX, scripts |
| **elan + Lean 4** | Compilador Lean (misma versión que `lean_project/lean-toolchain`) |
| **Lake** | Viene con Lean; descarga y construye **Mathlib** |
| **Claude Code CLI** (`claude` en el PATH) | El agente que escribe/edita los `.lean` por bloque |

No hace falta instalar Mathlib “a mano”: **Lake** lo trae como dependencia del proyecto `lean_project/` (`lakefile.toml`).

---

## 2. Instalación paso a paso

### 2.1 Git y Python

- **Git**: [https://git-scm.com/downloads](https://git-scm.com/downloads)
- **Python**: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
  En Windows, marca la opción **“Add Python to PATH”**.

### 2.2 Entorno virtual Python (recomendado)

Desde la raíz del repositorio (`AViD Journal`):

```bash
python -m venv .venv
```

Activación:

- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
- **macOS / Linux:** `source .venv/bin/activate`

Instalar dependencias:

```bash
pip install -r requirements.txt
```

### 2.3 Lean 4 con elan

La forma estándar es instalar **elan** y dejar que el proyecto fije la versión de Lean mediante `lean_project/lean-toolchain`.

- Instrucciones oficiales: [https://leanprover-community.github.io/get_started.html](https://leanprover-community.github.io/get_started.html)

Comprueba que Lean responde:

```bash
lean --version
```

La línea debe coincidir (o ser compatible) con la versión indicada en:

`lean_project/lean-toolchain`

### 2.4 Mathlib y primer build del proyecto compartido

El código asume un proyecto Lean compartido en:

`lean_project/`

Desde ahí:

```bash
cd lean_project
lake update
lake build
```

- La **primera vez** puede tardar mucho (descarga + compilación de Mathlib y dependencias).
- Los artefactos van a `lean_project/.lake/` (pesados; **no suelen subirse a GitHub**, ver sección 6).

Tras un build exitoso, puedes verificar un paper ya existente, por ejemplo:

```bash
lake build Papers.AyrtonPortoTesis.Paper
```

(si ese directorio existe en tu copia del repo).

### 2.5 Claude Code CLI

El orquestador invoca el ejecutable **`claude`** (subprocess). En Windows suele instalarse vía **npm** y aparecer como `claude.cmd`.

1. Instala **Node.js LTS**: [https://nodejs.org/](https://nodejs.org/)
2. Sigue la documentación actual de Anthropic para **Claude Code** (CLI) y autenticación (cuenta / suscripción / login).

Comprueba:

```bash
claude --version
```

Si el comando no se encuentra, revisa el PATH o usa la ruta completa al wrapper (`.cmd` en Windows).

**Notas:**

- La cuota de uso de Claude es externa al repo; si se agota, el runner detecta mensajes tipo “You've hit your limit” y el orquestador puede abortar el run (comportamiento esperado tras los últimos arreglos).
- No necesitas poner una API key “en el código Python” si ya iniciaste sesión con la CLI según el flujo oficial de Claude Code.

---

## 3. Cómo ejecutarlo

Trabaja siempre desde la **raíz del repo** (donde está `src/` y `requirements.txt`).

### 3.1 Codificación en Windows

Para evitar errores de Unicode en consola:

```powershell
$env:PYTHONIOENCODING="utf-8"
```

### 3.2 Dry-run (sin Claude, sin gasto)

Útil para validar parser + orden de bloques:

```bash
python -X utf8 -m src.formalization.orchestrator ruta/al/paper.tex --dry-run
```

### 3.3 Run real con proyecto Lean compartido (recomendado)

Por defecto se usa `lean_project/` como `--parent-project` si existe (ver `src/formalization/lean_project.py`).

```bash
python -X utf8 -m src.formalization.orchestrator ruta/al/paper.tex --title "Titulo del paper"
```

Opciones útiles:

| Opción | Significado |
|--------|-------------|
| `--title "..."` | Nombre legible del paper (slug del directorio bajo `lean_project/Papers/`) |
| `--blocks-range "1-13"` | Solo esos índices (1-based) entre los bloques **formalizables** |
| `--no-resume` | Ignora entradas ya `verified`/`axiom` en `PAPER_INDEX.md` |
| `--standalone` | Crea proyecto Lean aislado en `--base-dir` (legacy; más lento de mantener) |
| `--parent-project RUTA` | Otro proyecto Lean raíz en lugar de `./lean_project` |
| `--json` | Resumen final en JSON |

Ejemplo con rango y título:

```bash
python -X utf8 -m src.formalization.orchestrator "tests\mi_articulo.tex" --title "Mi articulo" --blocks-range "1-20"
```

### 3.4 Dónde queda la salida

Para un paper titulado `"Mi articulo"`, el slug típico es `MiArticulo` y la ruta:

```
lean_project/Papers/<Slug>/
├── Paper.lean           # acumulativo: todo lo ya verificado
├── PAPER_INDEX.md       # índice por bloque (estado, línea en Paper.lean, deps)
├── REVIEW.md            # axiomas / fallos / notas
├── Blocks/              # un .lean por bloque (lo que edita Claude)
│   └── ...
├── TASK.md              # generado por bloque (contexto de la tarea)
└── docs/prompts/        # copia de docs para el agente
```

Para **pair review**, lo más cómodo suele ser:

1. Leer `PAPER_INDEX.md` (mapa).
2. Abrir cada `Blocks/*.lean` (contenido por bloque).
3. Abrir `Paper.lean` para ver el módulo completo como lo verá Lean.

---

## 4. Estructura del repositorio (alto nivel)

```
├── prompts/                      # Prompts AViD para Claude Code
│   ├── prompt_avid.txt           # modo SIMPLE (definiciones, bloques cortos)
│   ├── prompt_medium_mode_avid.txt
│   ├── prompt_hard_mode_avid.txt
│   └── docs/prompts/             # avid_common.md, sketch agent, etc.
├── lean_project/                 # Proyecto Lean 4 compartido + Mathlib
│   ├── lakefile.toml
│   ├── lean-toolchain
│   └── Papers/<Slug>/...         # Un subdirectorio por paper formalizado
├── src/
│   ├── parser/                   # LaTeX → bloques + refs
│   └── formalization/
│       ├── orchestrator.py       # Pipeline principal + CLI
│       ├── lean_project.py       # creación idempotente de papers bajo Papers/
│       ├── complexity.py         # SIMPLE / MEDIUM / HARD / EXTERNAL
│       └── scripts/              # runner, run_claude, lean_checker, ...
├── tests/                        # .tex de prueba, tests pytest
├── requirements.txt
└── docs/
    └── GUIA_INSTALACION_Y_USO.md # este archivo
```

---

## 5. Qué puedes modificar en los prompts

Los archivos principales están en `prompts/`:

| Archivo | Cuándo se usa |
|---------|----------------|
| `prompt_avid.txt` | Modo **SIMPLE** (casi todas las definiciones; bloques sin prueba larga) |
| `prompt_medium_mode_avid.txt` | Modo **MEDIUM** |
| `prompt_hard_mode_avid.txt` | Modo **HARD** |

La selección la hace `src/formalization/complexity.py` (`classify`, `prompt_file_for`).

### Reglas que conviene no romper (contrato con el orquestador)

1. **Solo editar el archivo objetivo** indicado en `TASK.md` (típicamente `Blocks/<nombre>.lean`).
2. **No editar** `Paper.lean` ni `PAPER_INDEX.md` a mano desde Claude: el orquestador los actualiza al verificar cada bloque.
3. Mantener la línea `import Papers.<Slug>.Paper` en el bloque (visibilidad de definiciones previas).
4. Objetivo de verificación: código **sin errores de compilación**; `sorry` no está permitido por defecto (`allow_sorry=False` en las tareas).

### Qué sí suele ser seguro ajustar

- Tono, checklist de búsqueda en Mathlib, consejos de estilo Lean.
- Recordatorios de sintaxis ASCII (`forall`, `->`) si hay problemas de encoding en Windows.
- Límites de “cuánto buscar antes de declarar axioma” para resultados externos.

Tras cambiar prompts, un `--dry-run` + un bloque pequeño con `--blocks-range` valida que nada se rompió en el wiring.

---

## 6. Subir el proyecto a GitHub

### 6.1 Qué **no** subir (recomendado)

- **`lean_project/.lake/`**: caché y artefactos de build (muy pesados). Ya está ignorado en `lean_project/.gitignore`.
- **`.venv/`**: entorno virtual local.
- **`__pycache__/`**, `*.pyc`
- **Secretos**: `.env` con API keys (si en el futuro usas variables de entorno).

En la raíz del repo hay un `.gitignore` para Python y archivos comunes.

### 6.2 Qué **sí** suele subirse

- Código fuente (`src/`, `prompts/`, `tests/`).
- **Esqueleto** de `lean_project/` (`lakefile.toml`, `lean-toolchain`, fuentes `.lean` que quieras compartir).
- Opcional: papers formalizados en `lean_project/Papers/...` si quieres que otros **revieren el mismo Lean** sin rerun de Claude (trade-off: más tamaño de repo, pero reproducibilidad de lectura).

Si incluyes papers grandes, documenta en el README que el primer `lake build` puede ser largo.

### 6.3 Pasos típicos (primera vez)

En la raíz del proyecto:

```bash
git init
git branch -M main
git add .
git status   # revisar que .lake y .venv NO aparecen
git commit -m "Initial commit: AViD Journal formalization pipeline"
```

Crea un repo vacío en GitHub (sin README si ya tienes uno local, o haz merge).

```bash
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

### 6.4 Para colaboradores

En el README o en Issues, enlaza esta guía:

`docs/GUIA_INSTALACION_Y_USO.md`

y recuerda:

1. `pip install -r requirements.txt`
2. `cd lean_project && lake build`
3. `claude` instalado y autenticado
4. Ejecutar el orquestador con `PYTHONIOENCODING=utf-8` en Windows

---

## 7. Scripts útiles del repo (opcional)

Además del orquestador, en sesiones de trabajo se han usado scripts auxiliares en la raíz (si existen en tu copia), por ejemplo:

- Análisis del `.tex` sin Claude
- Limpieza de entradas `failed` tras rate limit
- Rebuild de índice desde `Blocks/`

Si los compartes en GitHub, documenta cada uno con una línea en el README.

---

## 8. Solución de problemas breve

| Síntoma | Qué revisar |
|---------|-------------|
| `claude` no encontrado (WinError 2) | PATH / instalar CLI / usar `claude.cmd` |
| Línea de comandos demasiado larga | Ya mitigado: prompt por stdin en `runner.py` |
| `Paper.olean` no existe al verificar un `Block` | Ejecutar `lake build Papers.<Slug>.Paper` desde `lean_project/` |
| Cuota Claude agotada | Esperar reset; usar `--blocks-range` + modo resume (por defecto) |

---

## 9. Ejemplos LaTeX + Lean en el repo

Hay dos conjuntos documentados (fuentes `.tex` y salida en `lean_project/Papers/`):

- Índice legible: **[`examples/README.md`](../examples/README.md)**

Resumen:

| Ejemplo | LaTeX | Lean generado |
|---------|-------|----------------|
| Artículo mínimo (pares) | `examples/tiny_even_numbers/paper.tex` | `lean_project/Papers/TinyEvensPaperReal/` |
| Tesis (corrida parcial) | `examples/thesis_ayrton_porto/paper.tex` | `lean_project/Papers/AyrtonPortoTesis/` |

Los scripts `diagnose_thesis.py`, `list_thesis_blocks.py`, etc., apuntan al `.tex` de `examples/thesis_ayrton_porto/paper.tex`.

---

Para una explicación **desde cero** (Git vs GitHub, primer push, por qué Mathlib no se sube, y cómo enlazar Numina con un submódulo), ver **[GIT_Y_GITHUB_DESDE_CERO.md](GIT_Y_GITHUB_DESDE_CERO.md)**.

---