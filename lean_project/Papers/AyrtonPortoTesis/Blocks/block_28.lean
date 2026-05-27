-- AViD block stub
-- label:
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Un retículo acotado es un retículo `L = (L, ∧, ∨)` que posee un primer elemento
    (elemento inferior) `bot` y un último elemento (elemento superior) `top`:
    - `bot ∧ a = bot` para todo `a` (elemento inferior);
    - `a ∨ top = top` para todo `a` (elemento superior).
    El retículo cumple adicionalmente las leyes de asociatividad, conmutatividad,
    idempotencia y absorción. -/
structure block_28 where
  /-- El universo del retículo. -/
  L : Type*
  /-- Operación meet (ínfimo): a ∧ b -/
  meet : L -> L -> L
  /-- Operación join (supremo): a ∨ b -/
  join : L -> L -> L
  /-- Asociatividad de meet -/
  meet_assoc : forall a b c : L, meet a (meet b c) = meet (meet a b) c
  /-- Asociatividad de join -/
  join_assoc : forall a b c : L, join a (join b c) = join (join a b) c
  /-- Conmutatividad de meet -/
  meet_comm : forall a b : L, meet a b = meet b a
  /-- Conmutatividad de join -/
  join_comm : forall a b : L, join a b = join b a
  /-- Idempotencia de meet -/
  meet_idem : forall a : L, meet a a = a
  /-- Idempotencia de join -/
  join_idem : forall a : L, join a a = a
  /-- Absorcion: a ∧ (b ∨ a) = a -/
  meet_absorb : forall a b : L, meet a (join b a) = a
  /-- Absorcion: a ∨ (b ∧ a) = a -/
  join_absorb : forall a b : L, join a (meet b a) = a
  /-- Primer elemento (elemento inferior): 0 ∧ a = 0 para todo a -/
  bot : L
  bot_meet : forall a : L, meet bot a = bot
  /-- Último elemento (elemento superior): a ∨ 1 = 1 para todo a -/
  top : L
  join_top : forall a : L, join a top = top
