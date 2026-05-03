-- ============================================================
-- AViD Journal — Paper: Ayrton Porto Tesis
-- Formalización automática generada por AViD
-- ============================================================

import Mathlib


/-- Un lenguaje algebraico (o tipo algebraico) es un par `(L, ar)`, donde `L` es un tipo de
símbolos y `ar : L → ℕ` es la función de aridad, que asigna a cada símbolo su número de
argumentos. Aquí `ℕ` incluye el cero. -/
structure def_lenguaje_algebraico where
  /-- El tipo de símbolos del lenguaje. -/
  Simbolos : Type*
  /-- La función de aridad: asigna a cada símbolo `f` su número de argumentos `ar(f) ∈ ℕ`. -/
  ar : Simbolos -> Nat

/-- Un álgebra `A` de tipo `L` es una estructura que consiste en un universo (conjunto no vacío)
y, para cada símbolo `f` de `L` con aridad `ar(f) = n`, una operación `f^A : A^n → A`.
Aquí `A^n` se representa como `Fin (L.ar f) → Universo`. -/
structure def_algebra (L : def_lenguaje_algebraico) where
  /-- El universo del álgebra: un tipo no vacío. -/
  Universo : Type*
  /-- El universo es no vacío. -/
  nonempty : Nonempty Universo
  /-- Las operaciones: para cada símbolo `f ∈ L` de aridad `n = ar(f)`,
      una función `Universo^n → Universo`. -/
  ops : (f : L.Simbolos) -> (Fin (L.ar f) -> Universo) -> Universo

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

/-- Given a topological space (X, T) and a subset A of X:
    clausura (closure) Cl(A) = intersection of all closed supersets of A,
    interior Int(A) = union of all open subsets of A.
    A set V is closed when its complement belongs to tau. -/
def def_clausura_interior (X : Type*) (T : def_topologia X) (A : Set X) :
    Prod (Set X) (Set X) :=
  Prod.mk
    (Set.sInter {V : Set X | Set.Subset A V /\ T.tau (Set.compl V)})
    (Set.sUnion {O : Set X | T.tau O /\ Set.Subset O A})

/-- A family `B` of subsets of `X` is a base (basis) for a topology on `X` if:
    (1) the union of all sets in `B` covers `X`;
    (2) for any `B1, B2 in B` and `x in B1 cap B2`, there exists `B3 in B`
        with `x in B3 subseteq B1 cap B2`.
    The topology generated by `B` is the family of all arbitrary unions of elements of `B`. -/
structure def_base_generadora (X : Type*) where
  /-- The base family: a collection of subsets of X. -/
  B : Set (Set X)
  /-- Condition 1: B covers X (the union of all sets in B equals X). -/
  covers : Set.sUnion B = Set.univ
  /-- Condition 2: for any B1, B2 in B and x in B1 cap B2, there exists B3 in B
      with x in B3 subseteq B1 cap B2. -/
  inter_refine : forall (B1 B2 : Set X), B B1 -> B B2 ->
    forall (x : X), B1 x /\ B2 x ->
    exists B3 : Set X, B B3 /\ B3 x /\ Set.Subset B3 (Set.inter B1 B2)

/-- The topology generated by a base: the family of all arbitrary unions
    of elements of the base. -/
def def_base_generadora.topologia_generada {X : Type*} (base : def_base_generadora X) :
    Set (Set X) :=
  fun U => exists F : Set (Set X), (forall V, F V -> base.B V) /\ U = Set.sUnion F

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

/-- A subbase for a topology on X is a family S of subsets of X such that
    the union of all members of S covers X (i.e. sUnion S = univ).
    The topology generated by S consists of all sets U such that for every
    x in U there exist finitely many S1, ..., Sn in S satisfying
    x in S1 inter ... inter Sn subseteq U. -/
structure def_subbase (X : Type*) where
  /-- The subbase family: a collection of subsets of X. -/
  S : Set (Set X)
  /-- Covering condition: the union of all members of S equals X. -/
  covers : Set.sUnion S = Set.univ

/-- The topology generated by a subbase sub: the family of all sets U such that
    for every x in U there exists a finite subfamily F of sub.S with
    x in sInter F subseteq U. -/
def def_subbase.topologia_generada {X : Type*} (sub : def_subbase X) : Set (Set X) :=
  fun U => forall x : X, U x ->
    exists F : Finset (Set X),
      (forall V, (F : Set (Set X)) V -> sub.S V) /\
      Set.sInter (F : Set (Set X)) x /\
      Set.Subset (Set.sInter (F : Set (Set X))) U

/-- An open cover (cubrimiento abierto) of a topological space `(X, T)` is a family
    of open sets `F ⊆ tau` whose union equals the whole space X. -/
structure def_cubrimiento_abierto (X : Type*) (T : def_topologia X) where
  /-- The family of open sets forming the cover. -/
  F : Set (Set X)
  /-- Every member of the family is open. -/
  sub_tau : forall U, F U -> T.tau U
  /-- The union of the family covers X. -/
  covers : Set.sUnion F = Set.univ

/-- A topological space `(X, T)` is **compact** if every open cover has a finite subcover:
    for every open cover `C` of `X`, there exists a finite subfamily `F'` of `C.F`
    that still covers `X`. -/
def def_compacidad (X : Type*) (T : def_topologia X) : Prop :=
  forall (C : def_cubrimiento_abierto X T),
    exists (F' : Finset (Set X)),
      (forall U, (F' : Set (Set X)) U -> C.F U) /\
      Set.sUnion (F' : Set (Set X)) = Set.univ

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
-- source: [{\cite[Lema~26.1]
-- statement (informal): {Munkres}}]\label{lem:compacto-subespacio-Munkres} Sean $(X,\tau)$ un espacio topológico y $V \subseteq X$. Las siguientes afirmaciones son equivalentes: \begin
axiom block_14 : True  -- TODO: signature placeholder; refine manually

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

/-- A function `f : X → Y` between topological spaces `(X, T)` and `(Y, T')` is
    **continuous** if the preimage of every open set in `T'` is open in `T`. -/
def esContinua {X Y : Type*} (T : def_topologia X) (T' : def_topologia Y)
    (f : X → Y) : Prop :=
  forall U : Set Y, T'.tau U -> T.tau (Set.preimage f U)

/-- A function `f : X → Y` is a **homeomorphism** from `(X, T)` to `(Y, T')` if:
    - `f` is bijective;
    - `f` is continuous (preimages of `T'`-open sets are `T`-open);
    - the inverse of `f` is continuous (images of `T`-open sets are `T'`-open).
    In this case the spaces `(X, T)` and `(Y, T')` are called homeomorphic. -/
structure def_continuidad_homeomorfismo {X Y : Type*}
    (T : def_topologia X) (T' : def_topologia Y) where
  /-- The underlying function `f : X → Y`. -/
  f : X -> Y
  /-- `f` is bijective. -/
  bij : Function.Bijective f
  /-- `f` is continuous: preimages of `T'`-open sets are `T`-open. -/
  cont : esContinua T T' f
  /-- The inverse of `f` is continuous: images of `T`-open sets are `T'`-open. -/
  inv_cont : forall V : Set X, T.tau V -> T'.tau (Set.image f V)

universe u v

/-- Una categoria C (estilo grafo) consta de una coleccion de objetos Ob,
    una coleccion de morfismos Fle, aplicaciones de dominio Dom y codominio Cod,
    una composicion parcial comp (definida cuando Cod f = Dom g) y morfismos
    identidad id, sujetos a las leyes de asociatividad y unitariedad. -/
structure Categoria : Type (max u v + 1) where
  Ob       : Type u
  Fle      : Type v
  Dom      : Fle -> Ob
  Cod      : Fle -> Ob
  comp     : (f g : Fle) -> Cod f = Dom g -> Fle
  id       : Ob -> Fle
  id_dom   : (x : Ob) -> Dom (id x) = x
  id_cod   : (x : Ob) -> Cod (id x) = x
  comp_dom : (f g : Fle) -> (h : Cod f = Dom g) -> Dom (comp f g h) = Dom f
  comp_cod : (f g : Fle) -> (h : Cod f = Dom g) -> Cod (comp f g h) = Cod g
  assoc    : (f g h : Fle) -> (hfg : Cod f = Dom g) -> (hgh : Cod g = Dom h) ->
               comp (comp f g hfg) h ((comp_cod f g hfg).trans hgh) =
               comp f (comp g h hgh) (hfg.trans (comp_dom g h hgh).symm)
  id_left  : (f : Fle) -> comp (id (Dom f)) f (id_cod (Dom f)) = f
  id_right : (f : Fle) -> comp f (id (Cod f)) ((id_dom (Cod f)).symm) = f

/-- Un morfismo `f : x → y` en una categoria `C` es un isomorfismo si existe
    un morfismo `g : y → x` tal que g ∘ f = id_x y f ∘ g = id_y.
    Los objetos `x` e `y` se dicen isomorfos en `C`. -/
structure block_18 (C : Categoria) where
  /-- Dominio del isomorfismo -/
  x : C.Ob
  /-- Codominio del isomorfismo -/
  y : C.Ob
  /-- El morfismo que es isomorfismo -/
  f : C.Fle
  /-- El morfismo inverso -/
  g : C.Fle
  /-- f tiene dominio x -/
  dom_f : C.Dom f = x
  /-- f tiene codominio y -/
  cod_f : C.Cod f = y
  /-- g tiene dominio y -/
  dom_g : C.Dom g = y
  /-- g tiene codominio x -/
  cod_g : C.Cod g = x
  /-- g ∘ f = id_x (diagrammatic: first f, then g) -/
  left_inv : C.comp f g (cod_f.trans dom_g.symm) = C.id x
  /-- f ∘ g = id_y (diagrammatic: first g, then f) -/
  right_inv : C.comp g f (cod_g.trans dom_f.symm) = C.id y

/-- La categoria opuesta C^op de una categoria C tiene los mismos objetos y morfismos
    que C, pero con las direcciones invertidas: Dom_op f = Cod f, Cod_op f = Dom f,
    y la composicion f^op ∘ g^op = (g ∘ f)^op.
    Formalmente: C^op(x,y) = C(y,x). -/
def block_19 (C : Categoria.{u, v}) : Categoria.{u, v} where
  Ob       := C.Ob
  Fle      := C.Fle
  Dom      := C.Cod
  Cod      := C.Dom
  comp f g h := C.comp g f h.symm
  id       := C.id
  id_dom   := C.id_cod
  id_cod   := C.id_dom
  comp_dom f g h := C.comp_cod g f h.symm
  comp_cod f g h := C.comp_dom g f h.symm
  assoc f g h hfg hgh := (C.assoc h g f hgh.symm hfg.symm).symm
  id_left f := C.id_right f
  id_right f := C.id_left f

/-- Una subcategoria D de una categoria C.
    ObD y FleD son predicados sobre Ob(C) y Fle(C) respectivamente,
    indicando que objetos y flechas pertenecen a D. -/
structure block_20 (C : Categoria.{u, v}) where
  /-- Predicado de pertenencia a los objetos de D -/
  ObD      : C.Ob -> Prop
  /-- Predicado de pertenencia a las flechas de D -/
  FleD     : C.Fle -> Prop
  /-- Los dominios de las flechas de D son objetos de D -/
  dom_mem  : forall f : C.Fle, FleD f -> ObD (C.Dom f)
  /-- Los codominios de las flechas de D son objetos de D -/
  cod_mem  : forall f : C.Fle, FleD f -> ObD (C.Cod f)
  /-- La identidad de cada objeto de D pertenece a FleD -/
  id_mem   : forall x : C.Ob, ObD x -> FleD (C.id x)
  /-- D es cerrada bajo composicion -/
  comp_mem : forall (f g : C.Fle) (h : C.Cod f = C.Dom g),
               FleD f -> FleD g -> FleD (C.comp f g h)

/-- D es una subcategoria plena de C si toda flecha de C con dominio y codominio
    en ObD pertenece a FleD. -/
def isPlena {C : Categoria.{u, v}} (D : block_20 C) : Prop :=
  forall (f : C.Fle), D.ObD (C.Dom f) -> D.ObD (C.Cod f) -> D.FleD f
