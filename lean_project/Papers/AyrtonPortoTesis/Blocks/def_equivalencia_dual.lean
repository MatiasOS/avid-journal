-- AViD block stub
-- label: def:equivalencia-dual
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Dos categorias C y D son dualmente equivalentes si existe una equivalencia
    de categorias entre C y D^op (la categoria opuesta de D).
    En este caso se dice que C y D son categorias duales. -/
def def_equivalencia_dual (C D : Categoria) : Prop :=
  Nonempty (block_24 C (block_19 D))
