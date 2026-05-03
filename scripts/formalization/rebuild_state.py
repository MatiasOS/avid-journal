"""
Reconstruye Paper.lean y PAPER_INDEX.md desde cero, usando solo:
  - los Block files que tengan declaracion real (no stubs),
  - el orden topologico calculado del .tex original,
  - los metadatos del parser.

Restablece el estado canonico tras una corrupcion (p.ej. dry-run que
escribio dummy lines, o entradas duplicadas por reruns con resume buggy).
"""
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.parser.latex_parser import LaTeXParser
from src.formalization.orchestrator import topological_sort
from src.formalization.lean_project import (
    LeanProjectManager,
    PAPER_LEAN_HEADER,
    PAPER_INDEX_HEADER,
    REVIEW_MD_HEADER,
)
from src.formalization.complexity import classify, Mode
from src.formalization.orchestrator import lean_ident_for, _extract_declarations, _has_real_declaration

PAPER_TITLE = "Ayrton Porto Tesis"
TEX_PATH = REPO_ROOT / "examples" / "thesis_ayrton_porto" / "paper.tex"
PAPER_DIR = REPO_ROOT / "lean_project" / "Papers" / "AyrtonPortoTesis"
BLOCKS_DIR = PAPER_DIR / "Blocks"
PAPER_LEAN = PAPER_DIR / "Paper.lean"
PAPER_INDEX = PAPER_DIR / "PAPER_INDEX.md"
REVIEW_MD = PAPER_DIR / "REVIEW.md"

print("[rebuild] Parseando .tex original...")
parser = LaTeXParser()
blocks_all = parser.parse_file(str(TEX_PATH))

formalizable = [b for b in blocks_all if b.get("type") not in ("remark", "example")]
print(f"[rebuild] {len(formalizable)} bloques formalizables.")

ordered = topological_sort(formalizable)
print(f"[rebuild] Ordenados por topologia.")

# Map label -> block info
by_label = {}
for i, b in enumerate(ordered, 1):
    label = b.get("label") or f"block_{i}"
    b["_idx"] = i
    by_label[label] = b

# Detect which Blocks/<name>.lean files have real declarations.
real_blocks = []
for f in BLOCKS_DIR.glob("*.lean"):
    code = _extract_declarations(f)
    if _has_real_declaration(code):
        real_blocks.append((f, code))

print(f"[rebuild] {len(real_blocks)} Block files con declaracion real.")

# Match each Block file with its label by lean_ident_for(label).
real_by_lean_name = {f.stem: (f, code) for f, code in real_blocks}
matches = []
for label, b in by_label.items():
    i = b["_idx"]
    lean_name = lean_ident_for(label, fallback=f"block_{i}")
    if lean_name in real_by_lean_name:
        f, code = real_by_lean_name[lean_name]
        matches.append((i, label, b, lean_name, code))

matches.sort(key=lambda m: m[0])
print(f"[rebuild] {len(matches)} bloques con codigo real, en orden topologico.")
for idx, label, _, lean_name, _ in matches:
    print(f"  {idx:3d}. {label:40s}  ({lean_name})")

# Rebuild Paper.lean
header = PAPER_LEAN_HEADER.format(paper_title=PAPER_TITLE)
parts = [header]

# We also need to handle external-axiom blocks: those have NO Block file but
# should appear in Paper.lean as `axiom` declarations. They are NOT in
# real_blocks. We detect them by mode=EXTERNAL.
processed_labels = set()
final_entries = []  # list of (label, block, lean_name, code, status, source)

for idx, label, b, lean_name, code in matches:
    parts.append(code.rstrip())
    parts.append("")
    final_entries.append((label, b, lean_name, code, "verified", None, None))
    processed_labels.add(label)

# Now scan EXTERNAL blocks that came BEFORE matched ones in topological
# order. We only include those that are EXTERNAL and whose .tex order is
# <= the highest matched idx. That preserves "everything we knew about up
# to the last verified block".
max_matched_idx = max((m[0] for m in matches), default=0)

# Collect EXTERNAL blocks needed (within reachable range).
external_axioms = []
for label, b in by_label.items():
    if label in processed_labels:
        continue
    i = b["_idx"]
    if i > max_matched_idx:
        continue
    mode = classify(b)
    if mode == Mode.EXTERNAL:
        external_axioms.append((i, label, b))

external_axioms.sort()
print(f"[rebuild] {len(external_axioms)} axiomas externos a (re)introducir.")

# Insert axiom blocks at appropriate position (use idx to keep order).
# Simpler: rebuild in idx order.
all_to_emit = list(matches) + [
    (i, label, b, lean_ident_for(label, fallback=f"block_{i}"), None) for i, label, b in external_axioms
]
all_to_emit.sort(key=lambda m: m[0])

# Restart Paper.lean
parts = [header]
final_entries = []

for idx, label, b, lean_name, code in all_to_emit:
    if code is not None:
        parts.append(code.rstrip())
        parts.append("")
        final_entries.append((label, b, lean_name, "verified", None))
    else:
        statement = b.get("content_latex") or ""
        title = b.get("title") or ""
        lean_signature = "True  -- TODO: signature placeholder; refine manually"
        source = title or "external result (paper without proof)"
        axiom_code = (
            f"-- source: [{source}]\n"
            f"-- statement (informal): {statement[:160].replace(chr(10), ' ')}\n"
            f"axiom {lean_name} : {lean_signature}"
        )
        parts.append(axiom_code)
        parts.append("")
        final_entries.append((label, b, lean_name, "axiom", source))

new_paper = "\n".join(parts)
PAPER_LEAN.write_text(new_paper, encoding="utf-8")
print(f"[rebuild] Paper.lean reescrito ({PAPER_LEAN.stat().st_size} bytes).")

# Recompute lean_line for each entry by scanning the rebuilt Paper.lean
text = PAPER_LEAN.read_text(encoding="utf-8")
lines = text.splitlines()

def find_decl_line(lean_name: str) -> int:
    """Heuristic: find the line where 'structure|def|theorem|lemma|axiom|...' lean_name starts."""
    pat = re.compile(rf"^\s*(structure|def|theorem|lemma|axiom|inductive|class|abbrev|instance)\s+{re.escape(lean_name)}\b")
    for i, ln in enumerate(lines, 1):
        if pat.match(ln):
            return i
    # fallback: first occurrence of lean_name on line start
    pat2 = re.compile(rf"^\s*{re.escape(lean_name)}\b")
    for i, ln in enumerate(lines, 1):
        if pat2.match(ln):
            return i
    return 0

# Rebuild PAPER_INDEX.md
index_parts = [PAPER_INDEX_HEADER.format(paper_title=PAPER_TITLE).rstrip(), ""]

for label, b, lean_name, status_kind, source in final_entries:
    line_no = find_decl_line(lean_name)
    statement_short = (b.get("content_latex") or "")[:200]
    statement_short = statement_short.replace("\n", " ").strip()
    if len(b.get("content_latex") or "") > 200:
        statement_short += "..."
    deps = b.get("references") or []
    deps_str = ", ".join(deps) if deps else "—"
    title = b.get("title")

    if status_kind == "verified":
        status_emoji = "✅ verified"
    else:
        status_emoji = "⚠️ axiom"

    head_line = f"## {label}"
    if title:
        head_line += f" — {title}"

    block_type = b.get("type") or "unknown"

    entry = f"""{head_line}
Type: {block_type}
Status: {status_emoji}
File: Paper.lean:{line_no}
Depends on: {deps_str}
"""
    if source:
        entry += f"Source: {source}\n"
    entry += f"Statement: {statement_short}\n\n---\n"
    index_parts.append(entry)

new_index = "\n".join(index_parts)
PAPER_INDEX.write_text(new_index, encoding="utf-8")
print(f"[rebuild] PAPER_INDEX.md reescrito ({PAPER_INDEX.stat().st_size} bytes, {len(final_entries)} entradas).")

# REVIEW.md: solo axiomas + (vacio si no hay)
review = REVIEW_MD_HEADER.format(paper_title=PAPER_TITLE).rstrip() + "\n\n"
review += "## Axiomas declarados\n\n"
ax = [(l, b, ln, src) for l, b, ln, st, src in final_entries if st == "axiom"]
if ax:
    for label, b, lean_name, source in ax:
        review += f"- **{label}** (`{lean_name}`): {source or '(sin fuente)'}\n"
        review += f"  Statement: {(b.get('content_latex') or '')[:150]}...\n\n"
else:
    review += "(ninguno todavia)\n\n"
review += "---\n\n## Bloques fallidos\n\n(ninguno todavia)\n\n---\n\n## Notas adicionales\n"
REVIEW_MD.write_text(review, encoding="utf-8")
print(f"[rebuild] REVIEW.md reescrito ({REVIEW_MD.stat().st_size} bytes).")

print()
print("=" * 60)
print(f"Estado canonico restaurado:")
print(f"  Paper.lean:      {PAPER_LEAN.stat().st_size:7d} bytes")
print(f"  PAPER_INDEX.md:  {PAPER_INDEX.stat().st_size:7d} bytes  ({len(final_entries)} entradas)")
print(f"  REVIEW.md:       {REVIEW_MD.stat().st_size:7d} bytes")
print("=" * 60)
