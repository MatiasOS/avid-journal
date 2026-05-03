-- AViD block stub
-- label: def:espacios-T
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Separation axioms for a topological space `(X, T)`.
    A space is T0 (Kolmogorov) if for any two distinct points there is an open set
    that contains one but not the other.
    A space is T1 (Frechet) if for any two distinct points x, y there exist open sets
    U, V with x in U, y not in U, and y in V, x not in V.
    A space is T2 (Hausdorff) if for any two distinct points there exist disjoint
    open neighborhoods. -/
structure def_espacios_T (X : Type*) (T : def_topologia X) where
  /-- T0 (Kolmogorov): for any x ≠ y in X there exists U open such that
      (x ∈ U ∧ y ∉ U) or (y ∈ U ∧ x ∉ U). -/
  isT0 : forall x y : X, x ≠ y ->
    exists U : Set X, T.tau U /\ ((U x /\ ¬ U y) \/ (U y /\ ¬ U x))
  /-- T1 (Frechet): for any x ≠ y in X there exist open sets U, V with
      x ∈ U, y ∉ U, y ∈ V, x ∉ V. -/
  isT1 : forall x y : X, x ≠ y ->
    exists U V : Set X, T.tau U /\ T.tau V /\ U x /\ ¬ U y /\ V y /\ ¬ V x
  /-- T2 (Hausdorff): for any x ≠ y in X there exist open sets U, V with
      x ∈ U, y ∈ V, and U ∩ V = ∅. -/
  isT2 : forall x y : X, x ≠ y ->
    exists U V : Set X, T.tau U /\ T.tau V /\ U x /\ V y /\
      Set.inter U V = (∅ : Set X)
