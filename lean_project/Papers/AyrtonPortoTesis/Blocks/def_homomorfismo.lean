-- AViD block stub
-- label: def:homomorfismo
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- A homomorphism of algebras alpha : A -> B over language L is a function between
    universes that commutes with every operation: alpha(f^A(a)) = f^B(alpha . a). -/
structure def_homomorfismo (L : def_lenguaje_algebraico) (A B : def_algebra L) where
  toFun : A.Universo -> B.Universo
  hom_compat : forall (f : L.Simbolos) (a : Fin (L.ar f) -> A.Universo),
    toFun (A.ops f a) = B.ops f (fun i => toFun (a i))

/-- The identity homomorphism on an algebra A. -/
def def_homomorfismo.id (L : def_lenguaje_algebraico) (A : def_algebra L) :
    def_homomorfismo L A A where
  toFun := fun x => x
  hom_compat := fun _ _ => rfl

/-- A monomorphism is an injective homomorphism. -/
def def_homomorfismo.IsMonomorphism (L : def_lenguaje_algebraico) (A B : def_algebra L)
    (alpha : def_homomorfismo L A B) : Prop :=
  Function.Injective alpha.toFun

/-- An epimorphism is a surjective homomorphism. -/
def def_homomorfismo.IsEpimorphism (L : def_lenguaje_algebraico) (A B : def_algebra L)
    (alpha : def_homomorfismo L A B) : Prop :=
  Function.Surjective alpha.toFun

/-- An isomorphism is a bijective homomorphism. -/
def def_homomorfismo.IsIsomorphism (L : def_lenguaje_algebraico) (A B : def_algebra L)
    (alpha : def_homomorfismo L A B) : Prop :=
  Function.Bijective alpha.toFun
