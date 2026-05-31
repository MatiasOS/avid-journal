# Notas sobre el demo web

**Propósito:** centralizar decisiones, requisitos y pendientes del demo Gradio que se construye en los Días 10-12 del sprint.

---

## Objetivos del demo

El demo cumple **dos funciones simultáneamente** y eso debe estar claro en el diseño:

1. **Función técnica:** permitir que cualquiera ingrese un enunciado en lenguaje natural y vea cómo AViD lo clasifica, con desglose por dimensión. Esto sirve para Wenda Li, Welleck, van Doorn — quieren tocar el sistema, no leer sobre él.

2. **Función comunicativa:** explicar la idea a alguien que llega frío. Esto sirve para Heath, Axiom, audiencia general de Zulip/Twitter. La página tiene que contar la historia de por qué importa antes de mostrar la herramienta.

---

## Stack elegido

**Gradio** — razones:
- Setup mínimo (decorador Python, en minutos hay UI).
- Deploy gratuito a Hugging Face Spaces.
- Pensado para audiencia técnica que toca un input y ve un output.
- Cero configuración de servidor.

**Alternativas rechazadas:**
- **Streamlit:** equivalente a Gradio pero ligeramente más complejo para casos simples.
- **Next.js / React:** profesional pero mucho overhead de frontend; perdido tiempo de implementación.

**Hosting:** Hugging Face Spaces (gratis, integración Gradio nativa, URL estable).

---

## Estructura propuesta de la página

### Bloque 1 — Header narrativo
Una imagen o diagrama de la matriz de cuatro casos.
Título: "AViD Journal — checking the novelty of formal proofs"
Subtítulo de una oración: "When is a theorem genuinely new? Three independent dimensions, one verdict."

### Bloque 2 — El problema (con caso Axiom)
Dos párrafos cortos:
- Por qué correctness ≠ novelty.
- Caso Axiom-Fel como evidencia del modo de falla.

### Bloque 3 — Demo interactivo
Input: textarea grande para pegar un enunciado en lenguaje natural (matemático/LaTeX). Ejemplos pre-cargados como botones:
- "La suma de cuatro pares es par" (debería dar TRIVIAL).
- "La raíz cuadrada de 2 es irracional" (debería dar REDUNDANTE — está en mathlib).
- "Existen infinitos primos (prueba de Euler)" (mostrar la D3 vs. Euclides).
- Un caso de novedad genuina del eval set (slot TBD del Día 9).

Output: tarjeta con:
- **Veredicto principal** (uno de los cinco: TRIVIAL / REDUNDANTE / NOVEDAD DE ENUNCIADO / NOVEDAD DE DEMOSTRACIÓN / CONOCIDO EN LITERATURA).
- **Desglose por dimensión:**
  - D1 (¿existe?): Sí/No en C_F + Sí/No en C_I, con link si corresponde.
  - D2 (¿trivial?): Sí/No, con qué táctica lo cerró.
  - D3 (¿prueba nueva?): distancia de Jaccard + match más cercano.
- **Capa 1 status:** ¿la traducción a Lean fue fiel? (sí/no/dudoso/falló)
- **Tipo Lean producido:** mostrar el `τ` autoformalizado.

### Bloque 4 — Cómo funciona (resumen)
Diagrama del árbol de decisión. Tres líneas de explicación.

### Bloque 5 — Footer
- Link al preprint.
- Link al repo de GitHub.
- Link al `metric_spec.md`.
- Contacto.

---

## Requisitos técnicos del demo

- **Tiempo de respuesta target:** < 30 segundos por enunciado. Más que eso pierde a la audiencia.
- **Caching:** los ejemplos pre-cargados deben tener resultados cacheados; no se computan en vivo.
- **Manejo de errores:** si autoformalización falla, mostrar mensaje claro: "Translation failed — this is a known limitation of v1. See Section X of the preprint."
- **Sin login ni registro.** Demo público.

---

## Pendientes / decisiones a tomar durante implementación

- ¿Qué modelo usa AViD para autoformalizar? (¿Numina? ¿Claude/GPT con prompts cuidados?)
- ¿El demo corre LeanDojo en tiempo real o usa cache pre-computado?
- ¿Tema visual claro u oscuro? (Default Gradio está bien para v1.)
- ¿Idioma del UI: inglés solo, o bilingüe?
- ¿Algún tipo de analytics? (Mejor no — privacidad.)

---

## Cuándo se hace cada parte

- **Día 10:** backend Gradio funcionando sobre los ejemplos pre-cargados.
- **Día 11:** página de landing con bloques narrativos, pulido visual.
- **Día 12:** deploy a Hugging Face Spaces. URL pública estable y confirmada.

---

## Riesgos

**Riesgo principal:** LeanDojo es lento corriendo en tiempo real. Mitigación: pre-cachear los ejemplos del eval set y para inputs nuevos del usuario tener un mensaje "this may take a minute" + spinner.

**Riesgo secundario:** autoformalización del usuario falla mucho en input arbitrario. Mitigación: limitar inputs a vocabulario de mathlib, dar ejemplos buenos, y manejar fallos elegantemente.

**Riesgo terciario:** Hugging Face Spaces tiene límites de cómputo en el tier gratis. Mitigación: si llegamos al límite, contemplar tier pagado mínimo o backend en otro lado.

---

## Link al demo

**URL:** *(se completa el Día 12 cuando esté desplegado)*
