-- AViD block stub
-- label: def:producto-algebras
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- The product algebra of a family of algebras indexed by I over language L.
    The universe is Pi (i : I), (A i).Universo, and operations are defined
    coordinate-wise: f^(prod A_i)(a1,...,an)(i) = f^(A_i)(a1(i),...,an(i)). -/
def def_producto_algebras (L : def_lenguaje_algebraico) (I : Type*)
    (A : I -> def_algebra L) : def_algebra L where
  Universo := (i : I) -> (A i).Universo
  nonempty  := Nonempty.intro (fun i => (A i).nonempty.some)
  ops       := fun f args i => (A i).ops f (fun k => args k i)

/-- The projection pi_j : prod A_i -> A_j onto coordinate j is a homomorphism. -/
def def_producto_algebras_projection (L : def_lenguaje_algebraico) (I : Type*)
    (A : I -> def_algebra L) (j : I) :
    def_homomorfismo L (def_producto_algebras L I A) (A j) where
  toFun      := fun a => a j
  hom_compat := fun _f _args => rfl
