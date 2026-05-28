-- ============================================================
-- AViD Journal — Paper: Tiny Evens Example
-- Formalización automática generada por AViD
-- ============================================================

import Mathlib

def def_even (n : Nat) : Prop := Exists (fun k : Nat => n = 2 * k)

lemma lem_even_sum (a b : Nat) (ha : def_even a) (hb : def_even b) : def_even (a + b) := by
  unfold def_even at *
  cases ha with
  | intro k hk =>
    cases hb with
    | intro m hm =>
      exact Exists.intro (k + m) (by omega)

theorem thm_four_evens (a b c d : Nat)
    (ha : def_even a) (hb : def_even b) (hc : def_even c) (hd : def_even d) :
    def_even (a + b + c + d) := by
  have hab : def_even (a + b) := lem_even_sum a b ha hb
  have habc : def_even (a + b + c) := lem_even_sum (a + b) c hab hc
  exact lem_even_sum (a + b + c) d habc hd

