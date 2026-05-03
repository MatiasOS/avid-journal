-- AViD block stub
-- label: def:cubrimiento-abierto
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- An open cover (cubrimiento abierto) of a topological space `(X, T)` is a family
    of open sets `F ⊆ tau` whose union equals the whole space X. -/
structure def_cubrimiento_abierto (X : Type*) (T : def_topologia X) where
  /-- The family of open sets forming the cover. -/
  F : Set (Set X)
  /-- Every member of the family is open. -/
  sub_tau : forall U, F U -> T.tau U
  /-- The union of the family covers X. -/
  covers : Set.sUnion F = Set.univ
