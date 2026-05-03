-- AViD block stub
-- label: def:lenguaje-algebraico
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- Un lenguaje algebraico (o tipo algebraico) es un par `(L, ar)`, donde `L` es un tipo de
símbolos y `ar : L → ℕ` es la función de aridad, que asigna a cada símbolo su número de
argumentos. Aquí `ℕ` incluye el cero. -/
structure def_lenguaje_algebraico where
  /-- El tipo de símbolos del lenguaje. -/
  Simbolos : Type*
  /-- La función de aridad: asigna a cada símbolo `f` su número de argumentos `ar(f) ∈ ℕ`. -/
  ar : Simbolos -> Nat
