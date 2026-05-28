-- AViD block stub
-- label: def:even
-- type:  definition
-- title: Even number
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.TinyEvensExample.Paper

def def_even (n : Nat) : Prop := Exists (fun k : Nat => n = 2 * k)
