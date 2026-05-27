-- AViD block stub
-- label: def: funtor
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

universe u1 v1 u2 v2

/-- Un funtor covariante F : C -> D entre categorias es un mapeo que asigna
    a cada objeto x de C un objeto F(x) de D, y a cada morfismo f : x -> y de C
    un morfismo F(f) : F(x) -> F(y) de D, preservando identidades y composicion:
    F(Id_x) = Id_{F(x)} y F(g ∘ f) = F(g) ∘ F(f).
    Un funtor contravariante F : C -> D invierte la direccion de los morfismos,
    de modo que f : x -> y produce F(f) : F(y) -> F(x); equivalentemente,
    es un funtor covariante C^op -> D. -/
structure def_funtor (C : Categoria.{u1, v1}) (D : Categoria.{u2, v2}) where
  /-- Accion sobre objetos -/
  mapObj : C.Ob -> D.Ob
  /-- Accion sobre morfismos -/
  mapFle : C.Fle -> D.Fle
  /-- Preservacion del dominio -/
  dom_map : forall f : C.Fle, D.Dom (mapFle f) = mapObj (C.Dom f)
  /-- Preservacion del codominio -/
  cod_map : forall f : C.Fle, D.Cod (mapFle f) = mapObj (C.Cod f)
  /-- Preservacion de identidades: F(Id_x) = Id_{F(x)} -/
  map_id : forall x : C.Ob, mapFle (C.id x) = D.id (mapObj x)
  /-- Preservacion de la composicion: F(g ∘ f) = F(g) ∘ F(f) -/
  map_comp : forall (f g : C.Fle) (h : C.Cod f = C.Dom g),
               mapFle (C.comp f g h) =
               D.comp (mapFle f) (mapFle g)
                 ((cod_map f).trans ((congrArg mapObj h).trans (dom_map g).symm))

/-- Un funtor contravariante C -> D es un funtor covariante C^op -> D. -/
abbrev FuntorContra (C : Categoria.{u1, v1}) (D : Categoria.{u2, v2}) :=
  def_funtor (block_19 C) D
