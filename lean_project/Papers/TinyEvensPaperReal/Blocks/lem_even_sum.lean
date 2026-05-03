-- AViD block stub
-- label: lem:even_sum
-- type:  lemma
-- title: Sum of two evens
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.TinyEvensPaperReal.Paper

lemma lem_even_sum (a b : Nat) (ha : def_even a) (hb : def_even b) : def_even (a + b) := by
  unfold def_even at *
  cases ha with
  | intro k hk =>
    cases hb with
    | intro m hm =>
      exact Exists.intro (k + m) (by omega)
