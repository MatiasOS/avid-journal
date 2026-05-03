-- Test "delgado": no importa Mathlib, solo lo basico de Lean core.
-- Sirve como linea base para ver cuanto pesa el toolchain solo.

def isEvenNarrow (n : Nat) : Prop := ∃ k, n = 2 * k

theorem two_is_even_narrow : isEvenNarrow 2 := by
  refine ⟨1, ?_⟩
  rfl
