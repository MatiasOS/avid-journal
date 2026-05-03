-- AViD block stub
-- label: def:algebra
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Un álgebra `A` de tipo `L` es una estructura que consiste en un universo (conjunto no vacío)
y, para cada símbolo `f` de `L` con aridad `ar(f) = n`, una operación `f^A : A^n → A`.
Aquí `A^n` se representa como `Fin (L.ar f) → Universo`. -/
structure def_algebra (L : def_lenguaje_algebraico) where
  /-- El universo del álgebra: un tipo no vacío. -/
  Universo : Type*
  /-- El universo es no vacío. -/
  nonempty : Nonempty Universo
  /-- Las operaciones: para cada símbolo `f ∈ L` de aridad `n = ar(f)`,
      una función `Universo^n → Universo`. -/
  ops : (f : L.Simbolos) -> (Fin (L.ar f) -> Universo) -> Universo
