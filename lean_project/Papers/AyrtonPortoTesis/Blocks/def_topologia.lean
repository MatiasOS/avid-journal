-- AViD block stub
-- label: def:topologia
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- A topology on a type `X` is a family `tau` of subsets of `X` satisfying:
    (1) the empty set and the whole space belong to `tau`;
    (2) arbitrary unions of members of `tau` belong to `tau`;
    (3) finite intersections of members of `tau` belong to `tau`.
    The pair `(X, tau)` is called a topological space. -/
structure def_topologia (X : Type*) where
  /-- The family of open sets (tau : Set (Set X) = (Set X) -> Prop). -/
  tau : Set (Set X)
  /-- The empty set is open. -/
  empty_mem : tau (fun (_ : X) => False)
  /-- The whole space is open. -/
  univ_mem : tau Set.univ
  /-- Arbitrary unions of open sets are open: if every member of F is in tau,
      then the union of F is in tau. -/
  union_mem : forall (F : Set (Set X)), (forall U, F U -> tau U) -> tau (Set.sUnion F)
  /-- Finite intersections of open sets are open. -/
  inter_mem : forall (s : Finset (Set X)), (forall U, (s : Set (Set X)) U -> tau U) ->
    tau (Set.sInter (s : Set (Set X)))
