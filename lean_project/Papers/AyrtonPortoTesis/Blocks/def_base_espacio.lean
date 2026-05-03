-- AViD block stub
-- label: def:base-espacio
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- A family `B` of subsets of `X` is a **base** of the topological space `(X, T)` if:
    (1) every member of `B` is open, i.e. `B ⊆ T.tau`;
    (2) for every open set `U ∈ T.tau` and every point `x ∈ U`, there exists `V ∈ B`
        with `x ∈ V ⊆ U`. -/
structure def_base_espacio (X : Type*) (T : def_topologia X) where
  /-- The base family: a collection of subsets of X. -/
  B : Set (Set X)
  /-- Condition 1: every element of B is open (B ⊆ tau). -/
  sub_tau : forall V : Set X, B V -> T.tau V
  /-- Condition 2: every open set is covered by elements of B — for every U in tau
      and every x in U, there exists V in B with x ∈ V ⊆ U. -/
  refine : forall U : Set X, T.tau U -> forall x : X, U x ->
    exists V : Set X, B V /\ V x /\ Set.Subset V U
