-- AViD block stub
-- label: def:compacidad
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- A topological space `(X, T)` is **compact** if every open cover has a finite subcover:
    for every open cover `C` of `X`, there exists a finite subfamily `F'` of `C.F`
    that still covers `X`. -/
def def_compacidad (X : Type*) (T : def_topologia X) : Prop :=
  forall (C : def_cubrimiento_abierto X T),
    exists (F' : Finset (Set X)),
      (forall U, (F' : Set (Set X)) U -> C.F U) /\
      Set.sUnion (F' : Set (Set X)) = Set.univ
