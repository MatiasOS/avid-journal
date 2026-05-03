-- AViD block stub
-- label:
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Una subcategoria D de una categoria C.
    ObD y FleD son predicados sobre Ob(C) y Fle(C) respectivamente,
    indicando que objetos y flechas pertenecen a D. -/
structure block_20 (C : Categoria.{u, v}) where
  /-- Predicado de pertenencia a los objetos de D -/
  ObD      : C.Ob -> Prop
  /-- Predicado de pertenencia a las flechas de D -/
  FleD     : C.Fle -> Prop
  /-- Los dominios de las flechas de D son objetos de D -/
  dom_mem  : forall f : C.Fle, FleD f -> ObD (C.Dom f)
  /-- Los codominios de las flechas de D son objetos de D -/
  cod_mem  : forall f : C.Fle, FleD f -> ObD (C.Cod f)
  /-- La identidad de cada objeto de D pertenece a FleD -/
  id_mem   : forall x : C.Ob, ObD x -> FleD (C.id x)
  /-- D es cerrada bajo composicion -/
  comp_mem : forall (f g : C.Fle) (h : C.Cod f = C.Dom g),
               FleD f -> FleD g -> FleD (C.comp f g h)

/-- D es una subcategoria plena de C si toda flecha de C con dominio y codominio
    en ObD pertenece a FleD. -/
def isPlena {C : Categoria.{u, v}} (D : block_20 C) : Prop :=
  forall (f : C.Fle), D.ObD (C.Dom f) -> D.ObD (C.Cod f) -> D.FleD f
