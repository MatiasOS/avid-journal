-- AViD block stub
-- label:
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

-- Composicion de funtores: dada F : C -> D y G : D -> E, produce G circ F : C -> E
private def funtor_comp {C D E : Categoria} (F : def_funtor C D) (G : def_funtor D E) :
    def_funtor C E where
  mapObj x := G.mapObj (F.mapObj x)
  mapFle f := G.mapFle (F.mapFle f)
  dom_map f := (G.dom_map (F.mapFle f)).trans (congrArg G.mapObj (F.dom_map f))
  cod_map f := (G.cod_map (F.mapFle f)).trans (congrArg G.mapObj (F.cod_map f))
  map_id x := by rw [F.map_id, G.map_id]
  map_comp f g h := by
    rw [F.map_comp f g h, G.map_comp]

-- Predicado: el morfismo f en la categoria C es un isomorfismo
private def esIsomorfismo {C : Categoria} (f : C.Fle) : Prop :=
  Exists fun g : C.Fle =>
  Exists fun h1 : C.Cod f = C.Dom g =>
  Exists fun h2 : C.Cod g = C.Dom f =>
    And (C.comp f g h1 = C.id (C.Dom f)) (C.comp g f h2 = C.id (C.Dom g))

/-- Una equivalencia de categorias entre C y D consiste en funtores covariantes
    F : C -> D y G : D -> C, junto con transformaciones naturales
    theta : I_C => G circ F y phi : I_D => F circ G,
    tales que todas las componentes son isomorfismos.
    En este caso se dice que C y D son equivalentes. -/
structure block_24 (C D : Categoria) where
  /-- Funtor covariante de C a D -/
  F : def_funtor C D
  /-- Funtor covariante de D a C -/
  G : def_funtor D C
  /-- Transformacion natural theta : I_C => G circ F -/
  theta : def_transf_nat (block_22 C) (funtor_comp F G)
  /-- Transformacion natural phi : I_D => F circ G -/
  phi : def_transf_nat (block_22 D) (funtor_comp G F)
  /-- Cada componente theta_X es un isomorfismo en C -/
  theta_iso : forall X : C.Ob, esIsomorfismo (theta.component X)
  /-- Cada componente phi_Y es un isomorfismo en D -/
  phi_iso : forall Y : D.Ob, esIsomorfismo (phi.component Y)
