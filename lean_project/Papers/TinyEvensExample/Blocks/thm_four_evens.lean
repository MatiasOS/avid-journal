import Papers.TinyEvensExample.Paper

theorem thm_four_evens (a b c d : Nat)
    (ha : def_even a) (hb : def_even b) (hc : def_even c) (hd : def_even d) :
    def_even (a + b + c + d) := by
  have hab : def_even (a + b) := lem_even_sum a b ha hb
  have habc : def_even (a + b + c) := lem_even_sum (a + b) c hab hc
  exact lem_even_sum (a + b + c) d habc hd
