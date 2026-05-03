import Papers.TinyEvensPaperReal.Paper

/-- A natural number `n` is even if there exists a natural number `k` such that `n = 2 * k`. -/
def def_even (n : Nat) : Prop := Exists (fun k : Nat => n = 2 * k)
