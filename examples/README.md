# Ejemplos del repo (LaTeX + Lean ya formalizado)

Este directorio agrupa los **fuentes LaTeX** que sirven como referencia pública. Las traducciones a Lean generadas por AViD viven en:

`lean_project/Papers/<NombreDelPaper>/`

---

## 1. Artículo mínimo (números pares)

| Qué | Ruta |
|-----|------|
| **LaTeX** | [`tiny_even_numbers/paper.tex`](tiny_even_numbers/paper.tex) |
| **Lean verificado** | [`../lean_project/Papers/TinyEvensPaperReal/`](../lean_project/Papers/TinyEvensPaperReal/) |

El contenido del `.tex` es el mismo que el *fixture* de tests [`tests/fixtures/sample_paper.tex`](../tests/fixtures/sample_paper.tex) (tres bloques: definición de par, lema de suma, teorema de cuatro pares).

### Reproducir desde cero (requiere Claude Code CLI)

Desde la raíz del repositorio:

```bash
python -X utf8 -m src.formalization.orchestrator examples/tiny_even_numbers/paper.tex --title "Tiny Evens Paper Real"
```

(Otro `--title` crearía otro slug bajo `lean_project/Papers/`.)

### Solo revisar el Lean

Abre `lean_project/Papers/TinyEvensPaperReal/Paper.lean` y los archivos en `Blocks/`.

---

## 2. Tesis de licenciatura (fragmento formalizado)

| Qué | Ruta |
|-----|------|
| **LaTeX** | [`thesis_ayrton_porto/paper.tex`](thesis_ayrton_porto/paper.tex) |
| **Lean (estado al momento del último commit)** | [`../lean_project/Papers/AyrtonPortoTesis/`](../lean_project/Papers/AyrtonPortoTesis/) |

Es el manuscrito completo en un solo archivo `.tex` (~270 KB). El pipeline AViD procesa **bloques formalizables** (definiciones, teoremas, etc.) según el parser; no todo el preámbulo ni los capítulos narrativos cuentan como “bloques”.

### Comandos típicos

Diagnóstico sin Claude:

```bash
python scripts/formalization/diagnose_thesis.py
```

Formalización por rangos (ahorra cuota y permite *pair review* incremental):

```bash
python -X utf8 -m src.formalization.orchestrator examples/thesis_ayrton_porto/paper.tex --title "Ayrton Porto Tesis" --blocks-range "1-13"
```

El modo **resume** está activado por defecto: los bloques ya `verified` / `axiom` en `PAPER_INDEX.md` se saltan.

### Lectura recomendada para revisión

1. `lean_project/Papers/AyrtonPortoTesis/PAPER_INDEX.md`
2. `lean_project/Papers/AyrtonPortoTesis/Blocks/*.lean`
3. `lean_project/Papers/AyrtonPortoTesis/Paper.lean`

---

## Licencia del contenido de ejemplo

El código del proyecto AViD sigue la licencia del repositorio. El contenido matemático del PDF/LaTeX de la tesis conserva la autoría del tesista; se incluye aquí como **material de ejemplo** para reproducibilidad del pipeline.
