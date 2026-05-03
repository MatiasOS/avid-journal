-- AViD block stub
-- label: def:clausura-interior
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Given a topological space (X, T) and a subset A of X:
    clausura (closure) Cl(A) = intersection of all closed supersets of A,
    interior Int(A) = union of all open subsets of A.
    A set V is closed when its complement belongs to tau. -/
def def_clausura_interior (X : Type*) (T : def_topologia X) (A : Set X) :
    Prod (Set X) (Set X) :=
  Prod.mk
    (Set.sInter {V : Set X | Set.Subset A V /\ T.tau (Set.compl V)})
    (Set.sUnion {O : Set X | T.tau O /\ Set.Subset O A})
