-- AViD block stub
-- label: def:reticulo_distributivo
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Un retículo `α` es distributivo si para todo `a b c : α` se cumple
    `a ⊓ (b ⊔ c) = (a ⊓ b) ⊔ (a ⊓ c)`.
    Esta condición es equivalente a su dual: `a ⊔ (b ⊓ c) = (a ⊔ b) ⊓ (a ⊔ c)`. -/
def def_reticulo_distributivo (α : Type*) [Lattice α] : Prop :=
  ∀ a b c : α, a ⊓ (b ⊔ c) = (a ⊓ b) ⊔ (a ⊓ c)
