-- AViD block stub
-- label: def:compacidad-subespacio
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- A subspace `V` of a topological space `(X, T)` is **compact** if every cover of `V`
    by open sets of `X` has a finite subcover: for every family `F` of open sets of `(X, T)`
    whose union contains `V`, there exists a finite subfamily `F'` of `F`
    whose union still contains `V`. -/
def def_compacidad_subespacio {X : Type*} (T : def_topologia X) (V : Set X) : Prop :=
  forall (F : Set (Set X)),
    (forall U, F U -> T.tau U) ->
    Set.Subset V (Set.sUnion F) ->
    exists (F' : Finset (Set X)),
      (forall U, (F' : Set (Set X)) U -> F U) /\
      Set.Subset V (Set.sUnion (F' : Set (Set X)))
