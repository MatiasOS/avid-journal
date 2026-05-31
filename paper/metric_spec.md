# Especificación de la métrica de novedad de AViD Journal

**Documento de diseño v1 — base para implementación y para la sección de metodología del paper**

---

## 1. Propósito y alcance

Este documento define, de manera precisa y operacional, qué significa que AViD clasifique un teorema como "novedoso". El objetivo es doble: (a) que sea implementable sin ambigüedad en los próximos días, y (b) que cada decisión de diseño sea defendible frente a la literatura previa y frente a la comunidad de teoría de tipos.

La unidad de análisis es el **teorema individual formalizado**. La novedad de un *artículo* completo se define, en una capa superior, como una agregación sobre la novedad de sus teoremas (fuera del alcance de v1; se menciona en trabajo futuro).

## 2. Notación y objetos básicos

Un **teorema formalizado** es un par `t = (τ, π)` donde `τ` es su *tipo* (el enunciado, en el sentido de Curry-Howard) y `π` es su *término de prueba* (o, equivalentemente para nuestros fines, el script de tácticas que lo genera).

El **corpus** contra el que se evalúa la novedad es `C = C_F ∪ C_I`, con dos capas de naturaleza distinta:

- `C_F` (corpus formal): teoremas ya formalizados, esencialmente mathlib.
- `C_I` (corpus informal): enunciados en lenguaje natural presentes en la literatura, accedidos vía arXiv y Semantic Scholar.

Esta dualidad es la diferencia central de AViD frente al baseline dominante (Kasaura et al., arXiv:2509.14274), que chequea novedad **solo contra el corpus formal** — definiendo novedad como "no está en mathlib ni en la lista generada". Chequear también `C_I` es lo que permite a AViD atrapar el modo de falla documentado por First Proof (Abouzaid et al., arXiv:2602.05192): un resultado ausente de mathlib pero ya existente en la literatura informal, presentado como original.

## 3. El problema central: ausencia del corpus ≠ novedad

La intuición ingenua "si no está en el corpus, es nuevo" falla por dos razones independientes, y la métrica entera está construida para corregir ambas.

**Falla por trivialidad.** Un teorema puede estar ausente de mathlib no por ser nuevo, sino por ser tan trivial que nadie se molestó en formalizarlo. Caso testigo: "la suma de cuatro números pares es par". No está en mathlib, pero la táctica `omega` lo cierra en milisegundos. La ausencia refleja trivialidad, no novedad.

**Falla por existencia informal.** Un teorema puede estar ausente de mathlib pero ya demostrado en un paper de arXiv. No es una contribución matemática nueva, aunque su formalización sí podría ser un aporte de ingeniería de formalización. Distinguir estos dos sentidos es parte del aporte de AViD.

## 4. Las tres dimensiones de la novedad

AViD descompone la novedad en tres dimensiones independientes. Cada una responde una pregunta distinta y se mide con un mecanismo distinto.

### 4.1 Dimensión 1 — No-existencia previa (¿ya existe este enunciado?)

Responde: ¿existe en el corpus un teorema con el mismo enunciado que `τ`? Esta dimensión incluye el **eje 1 (comparación de tipos)** y opera sobre las dos capas del corpus.

**Sobre `C_F` (formal):** se busca si existe `(τ', π') ∈ C_F` tal que `τ` y `τ'` son equivalentes. La equivalencia de tipos se define por niveles, y v1 adopta el más conservador implementable:

- *Nivel 0 (v1):* igualdad sintáctica tras normalización (`whnf` / formas normales de Lean).
- *Nivel 1 (deseable):* igualdad definicional vía `isDefEq` del kernel de Lean.
- *Reconocimiento honesto:* la equivalencia lógica plena (probar que `τ ↔ τ'`) es indecidible en general; v1 no la intenta y reporta sus falsos negativos (enunciados lógicamente equivalentes pero sintácticamente distintos, p. ej. currying o definiciones desplegadas de forma diferente).

**Sobre `C_I` (informal):** pipeline de dos etapas, barato-luego-caro.

- *Etapa A (filtro grueso, barato):* similitud semántica vía embeddings entre el enunciado candidato y los abstracts/teoremas del corpus informal. Solo decide a qué papers vale la pena aplicarles la etapa fina. Imprecisión tolerable acá.
- *Etapa B (verificación fina, cara):* para los papers que pasan el filtro, escaneo teorema-a-teorema; si hay similitud textual alta, se **autoformaliza** el teorema rival a un tipo Lean `τ'` y se compara con `τ` por el mismo criterio de equivalencia de tipos de arriba.

**Salida de D1:** dos banderas, `existe_en_C_F` y `existe_en_C_I`, cada una con su referencia. La etapa B es el punto frágil del sistema (la autoformalización es propensa a error; cf. ProofFlow arXiv:2510.15981, Aria arXiv:2510.04520) y AViD debe reportar explícitamente cuándo una clasificación depende de una traducción incierta.

### 4.2 Dimensión 2 — No-trivialidad (¿requiere alguna idea?)

Responde: ¿es `τ` matemáticamente trivial, en el sentido de cerrarse por automatización pura sin ideas? Esta dimensión es **independiente de D1** y es la que corrige la falla por trivialidad.

**Definición operacional:** `t` es **trivial** si existe una táctica `T` en el conjunto de automatización estándar `T_auto = {decide, omega, simp, norm_num, aesop, tauto}` que cierra `τ` (sin hipótesis adicionales) dentro de un presupuesto fijo de tiempo/recursos `b`. Se añade `exact?` como caso especial: si `exact?` cierra `τ` con un lema existente, eso detecta simultáneamente existencia en `C_F` (solapa con D1) y trivialidad de recuperación.

**Implementación:** generar un archivo `example : τ := by T` por cada táctica y verificar si compila dentro de `b`. No requiere metaprogramming; es el módulo más barato del sistema.

**Reconocimiento honesto:** "cerrable por `T_auto`" es una **sobre-aproximación** de trivialidad — `aesop` ocasionalmente cierra teoremas no triviales. Pero el sesgo va en la dirección correcta para novelty checking: si una táctica estándar lo liquida, no es una contribución que valga la pena reclamar como nueva, aun si no está en el corpus. El filtro es conservador hacia "no novedoso", que es el error seguro.

**Salida de D2:** bandera `trivial` + qué táctica lo cerró.

### 4.3 Dimensión 3 — Distancia estructural de pruebas (¿es la misma prueba o una nueva?)

Responde: dado que existe un teorema con el mismo enunciado (D1 encontró match de tipo), ¿la prueba candidata usa esencialmente las mismas ideas, o es una demostración alternativa? Esta dimensión solo se activa cuando D1 halla coincidencia de tipo. Es el **eje 2**.

**Por qué premisas y no homotopía:** en Lean 4 los teoremas viven en `Prop`, que es *proof-irrelevant*: dos términos cualesquiera del mismo `Prop` son definicionalmente iguales, de modo que cualquier noción de "homotopía entre términos" colapsa y no distingue nada. Por eso medimos la distancia entre los **conjuntos de premisas** que cada prueba invoca — qué lemas y definiciones previas usa. Esto se apoya en la línea de premise selection (Magnushammer, Mikuła–Jiang–Li et al., ICLR 2024; Machine-Learned Premise Selection for Lean, Piotrowski et al. arXiv:2304.00994), pero usada en **dirección inversa**: la premise selection elige premisas para *construir* pruebas; AViD extrae las premisas usadas como *huella* para *comparar* pruebas.

**Extracción de premisas:** `P(π) = ` conjunto de constantes de mathlib que aparecen en el término de prueba `π`, tras aplicar un **math filter** (whitelist de nombres de mathlib) que descarta lemas básicos/técnicos del core de Lean como `rfl`, `congr_arg`, `Eq.refl` — siguiendo exactamente la receta de Piotrowski et al. Herramienta de extracción: LeanDojo (traza pruebas y premisas de mathlib).

**Medida de distancia (v1):** índice de Jaccard.

```
d(π₁, π₂) = 1 − |P(π₁) ∩ P(π₂)| / |P(π₁) ∪ P(π₂)|
```

Con un umbral `θ`: si `d > θ`, las pruebas son **estructuralmente distantes** (demostración alternativa, novedad de prueba); si `d ≤ θ`, son la misma prueba (redundante).

**Mejoras futuras (declaradas, no en v1):** pesar premisas por rareza estilo IDF (una premisa rara aporta más que una ubicua), por profundidad en el grafo de dependencias (cf. la distribución scale-free del AFP, Huch arXiv:2209.13305), o pasar de distancia entre conjuntos a distancia entre grafos de dependencia (cf. Metrics for Graph Comparison, PLOS ONE). El Axiom-Based Atlas (Yoo, arXiv:2504.00063) usa proof vectors sobre axiomas con coseno/Jaccard para *organizar* conocimiento; AViD usa premisas para *chequear novedad contra corpus* — mismo tipo de herramienta, propósito distinto.

**Salida de D3:** la distancia `d` y la clasificación cercana/distante.

## 5. La matriz taxonómica de novedad

Cruzando el eje 1 (¿mismo tipo?) con el eje 2 (¿premisas cercanas o distantes?) se obtienen cuatro casos:

|                    | Premisas cercanas                                         | Premisas distantes                                                    |
| ------------------ | --------------------------------------------------------- | --------------------------------------------------------------------- |
| **Mismo tipo**     | Misma prueba del mismo teorema → *nada nuevo*             | Misma afirmación, prueba nueva → *novedad de demostración*            |
| **Tipo distinto** | (no aplica eje 2) → *novedad de enunciado*                | (no aplica eje 2) → *novedad de enunciado*                            |

Un quinto caso, transversal, es el de **tipos relacionados pero no iguales** (generalizaciones, variaciones): zona gris que v1 marca como "requiere revisión humana" en vez de forzar una etiqueta.

## 6. Regla de decisión combinada

Las tres dimensiones se integran en un árbol de decisión. El orden está elegido por costo computacional creciente: primero los filtros baratos que pueden descartar, dejando la autoformalización cara para el final.

1. **Aplicar D2 (trivialidad).** Si `trivial` → clasificar **NO NOVEDOSO (trivial)** y terminar. *(Esto mata el caso "suma de 4 pares" de entrada.)*
2. **Aplicar D1 sobre `C_F` (búsqueda formal, barata).**
   - Si existe match de tipo en mathlib → ir al paso 4 con ese match.
3. **Aplicar D1 sobre `C_I` (informal: etapa A barata, luego etapa B cara solo si A dispara).**
   - Si no hay match en `C_F` ni en `C_I` → clasificar **NOVEDAD DE ENUNCIADO** y terminar.
   - Si hay match en `C_I` pero no en `C_F` → clasificar **CONOCIDO EN LITERATURA (no formalizado)**; la formalización podría ser aporte de ingeniería, pero no es contribución matemática nueva.
4. **Aplicar D3 (distancia de premisas) sobre el/los match(es) de tipo.**
   - Si premisas distantes (`d > θ`) → **NOVEDAD DE DEMOSTRACIÓN**.
   - Si premisas cercanas (`d ≤ θ`) → **NO NOVEDOSO (redundante)**.

## 7. Casos límite y cómo se manejan

- **Enunciados lógicamente equivalentes con sintaxis distinta:** v1 puede dar falso negativo en D1 (no detecta el match); se reporta como limitación conocida.
- **Teoremas no triviales que `aesop` cierra:** falso positivo de trivialidad en D2; sesgo conservador aceptado.
- **Autoformalización incorrecta del rival en D1 etapa B:** la clasificación se marca como "dependiente de traducción incierta" y se prioriza para revisión humana.
- **Tipos relacionados pero no idénticos:** no se fuerza etiqueta, se manda a revisión.

## 8. Limitaciones declaradas

La equivalencia de tipos de v1 es sintáctica, con falsos negativos esperables. El filtro de trivialidad sobre-aproxima. La distancia de Jaccard ignora el peso y la posición de cada premisa en el grafo. La autoformalización del corpus informal es el eslabón más frágil y acota la confiabilidad de toda la rama `C_I`. El conjunto de evaluación de v1 es pequeño y curado a mano. Ninguna de estas limita la validez del *framework*; acotan la precisión de la *implementación v1*.

## 9. Resumen en una frase (para el abstract)

AViD define la novedad de un teorema formalizado como la conjunción de tres condiciones independientes —no-existencia en un corpus formal e informal, no-trivialidad bajo automatización estándar, y distancia estructural de premisas respecto de pruebas existentes del mismo enunciado— corrigiendo así el criterio ingenuo de "ausencia del corpus" que confunde trivialidad y existencia informal con genuina novedad.
