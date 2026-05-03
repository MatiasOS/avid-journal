-- Test "intermedio": importa solo modulos especificos de Mathlib relevantes
-- para hablar de paridad / numeros naturales.
--
-- Esta es la estrategia "Numina-friendly": en vez de `import Mathlib`,
-- se importan modulos quirurgicos para mantener el environment chico.

import Mathlib.Data.Nat.Basic
import Mathlib.Algebra.Ring.Parity

def isEvenMid (n : Nat) : Prop := ∃ k, n = 2 * k

theorem two_is_even_mid : isEvenMid 2 := by
  refine ⟨1, ?_⟩
  rfl
