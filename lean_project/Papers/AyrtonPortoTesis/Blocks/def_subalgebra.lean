-- AViD block stub
-- label: def:subalgebra
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- B is a subalgebra of A over language L (written B <= A) when there exists
    an injective map from B's universe into A's universe that commutes with all
    operations: embed(f^B(b)) = f^A(embed o b). -/
structure def_subalgebra (L : def_lenguaje_algebraico) (A B : def_algebra L) where
  /-- The inclusion map from B into A witnessing B is a subset of A. -/
  embed : B.Universo -> A.Universo
  /-- The embedding is injective. -/
  embed_injective : Function.Injective embed
  /-- Operations agree: embed(f^B(b)) = f^A(embed o b) for all f in L. -/
  ops_compat : forall (f : L.Simbolos) (b : Fin (L.ar f) -> B.Universo),
    embed (B.ops f b) = A.ops f (fun i => embed (b i))
