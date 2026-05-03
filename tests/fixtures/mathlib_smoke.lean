import Mathlib
theorem add_comm_test (a b : ℕ) : a + b = b + a := by
  exact Nat.add_comm a b
