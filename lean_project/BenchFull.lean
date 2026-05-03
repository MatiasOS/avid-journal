import Mathlib

-- Test "gordo": importa todo Mathlib.
-- Lo usamos para medir el costo real de cargar el environment completo.

def isEvenFull (n : Nat) : Prop := ∃ k, n = 2 * k

theorem two_is_even_full : isEvenFull 2 := by
  refine ⟨1, ?_⟩
  rfl
