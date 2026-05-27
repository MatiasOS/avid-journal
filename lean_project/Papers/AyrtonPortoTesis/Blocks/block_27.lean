-- AViD block stub
-- label:
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Un reticulo es un algebra L = (L, inf, sup) de tipo (2,2) con dos operaciones binarias
    que satisfacen: asociatividad, conmutatividad, idempotencia y absorcion. -/
structure block_27 (L : Type*) where
  /-- Operacion de infimo (meet) -/
  inf : L -> L -> L
  /-- Operacion de supremo (join) -/
  sup : L -> L -> L
  /-- Asociatividad de inf -/
  inf_assoc : forall a b c : L, inf a (inf b c) = inf (inf a b) c
  /-- Asociatividad de sup -/
  sup_assoc : forall a b c : L, sup a (sup b c) = sup (sup a b) c
  /-- Conmutatividad de inf -/
  inf_comm : forall a b : L, inf a b = inf b a
  /-- Conmutatividad de sup -/
  sup_comm : forall a b : L, sup a b = sup b a
  /-- Idempotencia de inf -/
  inf_idem : forall a : L, inf a a = a
  /-- Idempotencia de sup -/
  sup_idem : forall a : L, sup a a = a
  /-- Ley de absorcion: a inf (b sup a) = a -/
  absorption_inf : forall a b : L, inf a (sup b a) = a
  /-- Ley de absorcion: a sup (b inf a) = a -/
  absorption_sup : forall a b : L, sup a (inf b a) = a
