-- AViD block stub
-- label:
-- type:  definition
-- title: Categoria opuesta C^op
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- La categoria opuesta C^op de una categoria C tiene los mismos objetos y morfismos
    que C, pero con las direcciones invertidas: Dom_op f = Cod f, Cod_op f = Dom f,
    y la composicion f^op ∘ g^op = (g ∘ f)^op.
    Formalmente: C^op(x,y) = C(y,x). -/
def block_19 (C : Categoria.{u, v}) : Categoria.{u, v} where
  Ob       := C.Ob
  Fle      := C.Fle
  Dom      := C.Cod
  Cod      := C.Dom
  comp f g h := C.comp g f h.symm
  id       := C.id
  id_dom   := C.id_cod
  id_cod   := C.id_dom
  comp_dom f g h := C.comp_cod g f h.symm
  comp_cod f g h := C.comp_dom g f h.symm
  assoc f g h hfg hgh := (C.assoc h g f hgh.symm hfg.symm).symm
  id_left f := C.id_right f
  id_right f := C.id_left f
