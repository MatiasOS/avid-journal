-- AViD block stub
-- label:
-- type:  definition
-- title:
-- See ../TASK.md for the informal statement and proof.
--
-- Write the formalized Lean declaration(s) below this line.

import Papers.AyrtonPortoTesis.Paper

/-- El funtor identidad I_C : C -> C que envia cada objeto a si mismo
    y cada morfismo a si mismo. -/
def block_22 (C : Categoria) : def_funtor C C where
  mapObj x := x
  mapFle f := f
  dom_map _ := rfl
  cod_map _ := rfl
  map_id _ := rfl
  map_comp _ _ _ := rfl
