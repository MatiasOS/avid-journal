-- AViD block stub
-- label:
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Un morfismo `f : x → y` en una categoria `C` es un isomorfismo si existe
    un morfismo `g : y → x` tal que g ∘ f = id_x y f ∘ g = id_y.
    Los objetos `x` e `y` se dicen isomorfos en `C`. -/
structure block_18 (C : Categoria) where
  /-- Dominio del isomorfismo -/
  x : C.Ob
  /-- Codominio del isomorfismo -/
  y : C.Ob
  /-- El morfismo que es isomorfismo -/
  f : C.Fle
  /-- El morfismo inverso -/
  g : C.Fle
  /-- f tiene dominio x -/
  dom_f : C.Dom f = x
  /-- f tiene codominio y -/
  cod_f : C.Cod f = y
  /-- g tiene dominio y -/
  dom_g : C.Dom g = y
  /-- g tiene codominio x -/
  cod_g : C.Cod g = x
  /-- g ∘ f = id_x (diagrammatic: first f, then g) -/
  left_inv : C.comp f g (cod_f.trans dom_g.symm) = C.id x
  /-- f ∘ g = id_y (diagrammatic: first g, then f) -/
  right_inv : C.comp g f (cod_g.trans dom_f.symm) = C.id y
