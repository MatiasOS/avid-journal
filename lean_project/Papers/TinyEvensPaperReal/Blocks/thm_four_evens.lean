import Papers.TinyEvensPaperReal.Paper

theorem thm_four_evens (a b c d : Nat) (ha : def_even a) (hb : def_even b) (hc : def_even c) (hd : def_even d) : def_even (a + b + c + d) := by
  have hab : def_even (a + b) := lem_even_sum a b ha hb
  have hcd : def_even (c + d) := lem_even_sum c d hc hd
  have h := lem_even_sum (a + b) (c + d) hab hcd
  unfold def_even at *
  cases h with
  | intro k hk => exact Exists.intro k (by omega)
