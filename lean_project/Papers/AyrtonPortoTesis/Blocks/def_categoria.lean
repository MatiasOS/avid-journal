-- AViD block stub
-- label: def:categoria
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

universe u v

/-- Una categoria C (estilo grafo) consta de una coleccion de objetos Ob,
    una coleccion de morfismos Fle, aplicaciones de dominio Dom y codominio Cod,
    una composicion parcial comp (definida cuando Cod f = Dom g) y morfismos
    identidad id, sujetos a las leyes de asociatividad y unitariedad. -/
structure Categoria : Type (max u v + 1) where
  Ob       : Type u
  Fle      : Type v
  Dom      : Fle -> Ob
  Cod      : Fle -> Ob
  comp     : (f g : Fle) -> Cod f = Dom g -> Fle
  id       : Ob -> Fle
  id_dom   : (x : Ob) -> Dom (id x) = x
  id_cod   : (x : Ob) -> Cod (id x) = x
  comp_dom : (f g : Fle) -> (h : Cod f = Dom g) -> Dom (comp f g h) = Dom f
  comp_cod : (f g : Fle) -> (h : Cod f = Dom g) -> Cod (comp f g h) = Cod g
  assoc    : (f g h : Fle) -> (hfg : Cod f = Dom g) -> (hgh : Cod g = Dom h) ->
               comp (comp f g hfg) h ((comp_cod f g hfg).trans hgh) =
               comp f (comp g h hgh) (hfg.trans (comp_dom g h hgh).symm)
  id_left  : (f : Fle) -> comp (id (Dom f)) f (id_cod (Dom f)) = f
  id_right : (f : Fle) -> comp f (id (Cod f)) ((id_dom (Cod f)).symm) = f
