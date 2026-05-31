# Abstract — borradores e iteraciones

**Propósito:** versionar las distintas formulaciones del abstract antes de la versión final del Día 14. El abstract es lo primero que lee cualquier reviewer/supervisor; vale invertir tiempo.

**Restricción típica:** 150-250 palabras.

---

## Borrador v0 (de la spec, Día 1)

> AViD define la novedad de un teorema formalizado como la conjunción de tres condiciones independientes —no-existencia en un corpus formal e informal, no-trivialidad bajo automatización estándar, y distancia estructural de premisas respecto de pruebas existentes del mismo enunciado— corrigiendo así el criterio ingenuo de "ausencia del corpus" que confunde trivialidad y existencia informal con genuina novedad.

*Una oración. Sirve como tagline pero no como abstract completo.*

---

## Borrador v1 (esqueleto del preprint, Día 13)

> We introduce AViD Journal, a system for automatically assessing the novelty of mathematical theorems by decomposing it into three independent dimensions: non-existence in a corpus combining formal libraries and informal literature, non-triviality under standard proof automation, and structural distance from existing proofs measured via premise sets. We argue and show empirically that the naive criterion of "absence from the formal corpus", widely used by recent LLM-based theorem generators, conflates triviality and informal existence with genuine novelty — a failure mode publicly documented in industrial AI mathematics systems. AViD's three-dimensional decomposition corrects this conflation. We present a preliminary evaluation over 29 hand-curated theorems and release a functional web demo at [URL].

*Cinco oraciones. Cubre problema, contribución, validación, demo. Pendiente: agregar el número de aciertos cuando esté el Día 9.*

---

## Borrador v2 (Día 14, post-resultados)

*[A llenar el Día 14 con los números reales del eval set, mencionando explícitamente el caso Axiom como motivación, y refinando hasta que cada palabra cuente. La versión final debería poder responder en cinco oraciones: qué problema, por qué importa, qué hacemos, cómo lo validamos, dónde está el código.]*

---

## Versión TL;DR para Zulip (1 oración)

*[Para el post de anuncio en Lean Zulip. Diferente del abstract — más casual, menos formal.]*

Ejemplo posible: "AViD Journal: an automated novelty checker for Lean theorems that goes beyond 'is it in mathlib?' by combining triviality filtering and proof-structure comparison via premise sets. Demo: [URL]. Preprint: [URL]. Feedback welcome."

---

## Versión para emails a supervisores (1-2 oraciones, post-saludo)

*[Para Wenda Li, Welleck, van Doorn. Más técnica.]*

Ejemplo posible: "I've been building AViD Journal — an automated pipeline that combines Python orchestration, Lean 4, LeanDojo-based premise extraction, and Semantic Scholar to assess whether a proof is genuinely novel, by decomposing novelty into three independent dimensions: prior existence (formal + informal corpus), non-triviality (tactic automation), and structural distance from existing proofs (Jaccard on premise sets). The aim is to address a failure mode publicly identified in recent industrial AI systems where existing literature results were misrepresented as novel."

---

## Notas para la versión final

- Mencionar Axiom-Fel explícitamente solo si encaja sin desbalancear (es la motivación más concreta pero también podría leerse como ataque).
- El número de aciertos del eval set (Día 9) va en el abstract.
- La URL del demo va en el abstract — es lo que le da credibilidad operacional.
- El nombre "AViD Journal" — confirmar si se mantiene o se simplifica a "AViD" en el título del paper.
