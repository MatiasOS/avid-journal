-- AViD block stub
-- label: def:transf-nat
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Una transformacion natural theta : F => G entre funtores covariantes
    F, G : C -> D es una familia de morfismos theta_X : F(X) -> G(X) en D,
    indexada por los objetos X de C, de manera que para cada morfismo
    f : X -> Y en C el siguiente cuadrado conmuta:
       theta_X ; G(f) = F(f) ; theta_Y
    (escribiendo la composicion en orden diagramatico: primero la izquierda,
    luego la derecha). -/
structure def_transf_nat {C : Categoria.{u1, v1}} {D : Categoria.{u2, v2}}
    (F G : def_funtor C D) where
  /-- La componente en cada objeto X: un morfismo en D con Dom = F(X), Cod = G(X) -/
  component : C.Ob -> D.Fle
  /-- La componente theta_X tiene dominio F(X) -/
  dom_cond  : forall X : C.Ob, D.Dom (component X) = F.mapObj X
  /-- La componente theta_X tiene codominio G(X) -/
  cod_cond  : forall X : C.Ob, D.Cod (component X) = G.mapObj X
  /-- Condicion de naturalidad: theta_X ; G(f) = F(f) ; theta_Y
      Es decir, G(f) circ theta_X = theta_Y circ F(f) -/
  naturality : forall (f : C.Fle),
    D.comp (component (C.Dom f)) (G.mapFle f)
      ((cod_cond (C.Dom f)).trans (G.dom_map f).symm) =
    D.comp (F.mapFle f) (component (C.Cod f))
      ((F.cod_map f).trans (dom_cond (C.Cod f)).symm)
