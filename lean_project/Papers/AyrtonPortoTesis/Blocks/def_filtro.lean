-- AViD block stub
-- label: def:filtro
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Un subconjunto no vacío `F` de un retículo `L` es un **filtro** si:
1. `F` es creciente (upward-closed): si `a ∈ F` y `a ≤ b`, entonces `b ∈ F`;
2. `F` es cerrado bajo ínfimos: si `a, b ∈ F`, entonces `a ⊓ b ∈ F`.

Un filtro `F` es **propio** si `F ≠ L` (es decir, `F ≠ Set.univ`). -/
structure def_filtro {L : Type*} [Lattice L] (F : Set L) : Prop where
  /-- F is non-empty. -/
  nonempty : F.Nonempty
  /-- F is upward-closed: if a ∈ F and a ≤ b, then b ∈ F. -/
  upward_closed : ∀ a ∈ F, ∀ b : L, a ≤ b → b ∈ F
  /-- F is closed under binary meets: if a, b ∈ F then a ⊓ b ∈ F. -/
  meet_closed : ∀ a ∈ F, ∀ b ∈ F, a ⊓ b ∈ F

/-- Un filtro `F` en un retículo `L` es **propio** si `F ≠ L`. -/
def def_filtro_propio {L : Type*} [Lattice L] (F : Set L) : Prop :=
  def_filtro F ∧ F ≠ Set.univ
