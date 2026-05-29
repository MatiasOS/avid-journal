"""Tests para paper_extractor.extract_blocks_from_file().

Verifica que un .tex local se parsea correctamente y produce bloques en el
mismo formato que consume NoveltyChecker (sin red, sin ArXiv).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.novelty.paper_extractor import extract_abstract_from_tex, extract_blocks_from_file

_TINY_TEX = _REPO_ROOT / "examples" / "tiny_even_numbers" / "paper.tex"
_WITH_ABSTRACT_TEX = _REPO_ROOT / "tests" / "fixtures" / "paper_with_abstract.tex"
_EMPTY_ABSTRACT_TEX = _REPO_ROOT / "tests" / "fixtures" / "paper_with_empty_abstract.tex"


# ---------------------------------------------------------------------------
# Casos felices
# ---------------------------------------------------------------------------

def test_extract_blocks_from_file_count():
    """tiny_even_numbers/paper.tex contiene exactamente 3 bloques."""
    blocks = extract_blocks_from_file(str(_TINY_TEX))
    assert len(blocks) == 3, f"Esperados 3 bloques, obtenidos {len(blocks)}"


def test_extract_blocks_from_file_types():
    """Los tipos de los 3 bloques son definition, lemma, theorem (en ese orden)."""
    blocks = extract_blocks_from_file(str(_TINY_TEX))
    types = [b["type"] for b in blocks]
    assert types == ["definition", "lemma", "theorem"], f"Tipos inesperados: {types}"


def test_extract_blocks_from_file_labels():
    """Los labels coinciden con los \\label{} definidos en el .tex."""
    blocks = extract_blocks_from_file(str(_TINY_TEX))
    labels = [b["label"] for b in blocks]
    assert labels == ["def:even", "lem:even_sum", "thm:four_evens"], (
        f"Labels inesperados: {labels}"
    )


def test_extract_blocks_from_file_required_keys():
    """Cada bloque tiene las keys que consume NoveltyChecker."""
    required = {"type", "label", "title", "content_latex", "proof_latex", "references"}
    blocks = extract_blocks_from_file(str(_TINY_TEX))
    for i, block in enumerate(blocks):
        missing = required - block.keys()
        assert not missing, f"Bloque {i} le faltan keys: {missing}"


def test_extract_blocks_from_file_content_nonempty():
    """Todos los bloques tienen content_latex no vacío."""
    blocks = extract_blocks_from_file(str(_TINY_TEX))
    for i, block in enumerate(blocks):
        content = block.get("content_latex") or ""
        assert content.strip(), f"Bloque {i} tiene content_latex vacío"


def test_extract_blocks_from_file_proof_in_theorem():
    """El theorem y el lemma tienen proof_latex; la definition no."""
    blocks = extract_blocks_from_file(str(_TINY_TEX))
    by_label = {b["label"]: b for b in blocks}

    assert not (by_label["def:even"].get("proof_latex") or "").strip(), (
        "def:even no debería tener proof_latex"
    )
    assert (by_label["lem:even_sum"].get("proof_latex") or "").strip(), (
        "lem:even_sum debería tener proof_latex"
    )
    assert (by_label["thm:four_evens"].get("proof_latex") or "").strip(), (
        "thm:four_evens debería tener proof_latex"
    )


# ---------------------------------------------------------------------------
# Casos de error
# ---------------------------------------------------------------------------

def test_extract_blocks_from_file_not_found():
    """FileNotFoundError si el archivo no existe."""
    with pytest.raises(FileNotFoundError):
        extract_blocks_from_file("no_existe_este_archivo.tex")


def test_extract_blocks_from_file_wrong_extension():
    """ValueError si la ruta no tiene extensión .tex."""
    with pytest.raises(ValueError, match=r"\.tex"):
        extract_blocks_from_file(str(_REPO_ROOT / "README.md"))


# ---------------------------------------------------------------------------
# extract_abstract_from_tex — casos felices
# ---------------------------------------------------------------------------

def test_extract_abstract_returns_text():
    """.tex con \\begin{abstract} devuelve el texto limpio."""
    result = extract_abstract_from_tex(str(_WITH_ABSTRACT_TEX))
    assert result is not None
    # El abstract contiene estas palabras clave del fixture
    assert "even" in result.lower()
    assert "sum" in result.lower()


def test_extract_abstract_is_clean_text():
    """El resultado no contiene comandos LaTeX residuales."""
    result = extract_abstract_from_tex(str(_WITH_ABSTRACT_TEX))
    assert result is not None
    assert "\\" not in result, f"Hay comandos LaTeX sin limpiar: {result!r}"
    assert "{" not in result and "}" not in result


def test_extract_abstract_no_section():
    """.tex sin sección abstract devuelve None (tiny_even_numbers no tiene abstract)."""
    result = extract_abstract_from_tex(str(_TINY_TEX))
    assert result is None


def test_extract_abstract_empty_section():
    """.tex con \\begin{abstract}\\end{abstract} vacío devuelve None."""
    result = extract_abstract_from_tex(str(_EMPTY_ABSTRACT_TEX))
    assert result is None


# ---------------------------------------------------------------------------
# extract_abstract_from_tex — casos de error
# ---------------------------------------------------------------------------

def test_extract_abstract_not_found():
    """FileNotFoundError si el archivo no existe."""
    with pytest.raises(FileNotFoundError):
        extract_abstract_from_tex("archivo_inexistente.tex")


def test_extract_abstract_wrong_extension():
    """ValueError si la ruta no tiene extensión .tex."""
    with pytest.raises(ValueError, match=r"\.tex"):
        extract_abstract_from_tex(str(_REPO_ROOT / "README.md"))
