-- AViD block stub
-- label: def:isomorfismo-categorias
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

universe u1 v1 u2 v2

/-- Dos categorias C y D son isomorfas (C ≅ D) si existen funtores covariantes
    F : C -> D y G : D -> C tales que se cumplen las igualdades estrictas
    F ∘ G = I_D y G ∘ F = I_C, es decir:
      - F.mapObj (G.mapObj y) = y  y  F.mapFle (G.mapFle f) = f  para todo y, f en D;
      - G.mapObj (F.mapObj x) = x  y  G.mapFle (F.mapFle g) = g  para todo x, g en C. -/
structure def_isomorfismo_categorias (C : Categoria.{u1, v1}) (D : Categoria.{u2, v2}) where
  /-- Funtor covariante de C a D -/
  F : def_funtor C D
  /-- Funtor covariante de D a C -/
  G : def_funtor D C
  /-- F ∘ G = I_D sobre objetos -/
  FG_obj : forall y : D.Ob, F.mapObj (G.mapObj y) = y
  /-- F ∘ G = I_D sobre morfismos -/
  FG_fle : forall f : D.Fle, F.mapFle (G.mapFle f) = f
  /-- G ∘ F = I_C sobre objetos -/
  GF_obj : forall x : C.Ob, G.mapObj (F.mapObj x) = x
  /-- G ∘ F = I_C sobre morfismos -/
  GF_fle : forall g : C.Fle, G.mapFle (F.mapFle g) = g
