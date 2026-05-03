-- AViD block stub
-- label: def:continuidad-homeomorfismo
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

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
