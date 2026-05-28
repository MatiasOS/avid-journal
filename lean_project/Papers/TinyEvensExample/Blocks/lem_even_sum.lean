import Papers.TinyEvensExample.Paper

lemma lem_even_sum (a b : Nat) (ha : def_even a) (hb : def_even b) : def_even (a + b) := by
  unfold def_even at *
  cases ha with
  | intro k hk =>
    cases hb with
    | intro m hm =>
      exact Exists.intro (k + m) (by omega)
