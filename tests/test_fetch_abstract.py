"""Tests for paper_extractor.fetch_abstract.

Live tests (hitting the real ArXiv metadata API) are marked @pytest.mark.live
and can be excluded with `pytest -m "not live"`.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.novelty.paper_extractor import (
    _normalize_arxiv_id,
    _parse_abstract_from_atom,
    fetch_abstract,
)


# ---------------------------------------------------------------------------
# _normalize_arxiv_id — unit
# ---------------------------------------------------------------------------

def test_normalize_strips_prefix():
    assert _normalize_arxiv_id("arXiv:2605.02064") == "2605.02064"
    assert _normalize_arxiv_id("arxiv:2605.02064") == "2605.02064"


def test_normalize_strips_version():
    assert _normalize_arxiv_id("2404.13480v2") == "2404.13480"
    assert _normalize_arxiv_id("2605.02064v1") == "2605.02064"


def test_normalize_strips_path():
    assert _normalize_arxiv_id("abs/2605.02064") == "2605.02064"


def test_normalize_strips_whitespace():
    assert _normalize_arxiv_id("  2605.02064  ") == "2605.02064"


def test_normalize_clean_id_unchanged():
    assert _normalize_arxiv_id("2605.02064") == "2605.02064"


# ---------------------------------------------------------------------------
# _parse_abstract_from_atom — unit (no network)
# ---------------------------------------------------------------------------

_SAMPLE_ATOM = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2605.02064v1</id>
    <title>A test paper title</title>
    <summary>
      This paper proves something interesting about Sidon sets.
      We use combinatorial methods to obtain the result.
    </summary>
  </entry>
</feed>
"""

_ATOM_NO_ENTRY = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
</feed>
"""

_ATOM_NO_SUMMARY = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2605.02064v1</id>
    <title>A test paper title</title>
  </entry>
</feed>
"""

_ATOM_EXCESS_WHITESPACE = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <summary>  Line one.   Line two.    Line three.  </summary>
  </entry>
</feed>
"""


def test_parse_abstract_returns_text():
    abstract = _parse_abstract_from_atom(_SAMPLE_ATOM)
    assert "Sidon" in abstract
    assert "combinatorial" in abstract


def test_parse_abstract_strips_outer_whitespace():
    abstract = _parse_abstract_from_atom(_SAMPLE_ATOM)
    assert not abstract.startswith(" ")
    assert not abstract.endswith(" ")


def test_parse_abstract_collapses_inline_spaces():
    abstract = _parse_abstract_from_atom(_ATOM_EXCESS_WHITESPACE)
    assert "  " not in abstract  # no double spaces


def test_parse_abstract_no_entry_raises():
    with pytest.raises(ValueError, match="no <entry>"):
        _parse_abstract_from_atom(_ATOM_NO_ENTRY)


def test_parse_abstract_no_summary_returns_empty():
    result = _parse_abstract_from_atom(_ATOM_NO_SUMMARY)
    assert result == ""


def test_parse_abstract_invalid_xml_raises():
    with pytest.raises(ValueError, match="Invalid XML"):
        _parse_abstract_from_atom("this is not xml at all <<<")


# ---------------------------------------------------------------------------
# fetch_abstract — unit (mocked HTTP)
# ---------------------------------------------------------------------------

def _make_response(text: str, status_code: int = 200) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.raise_for_status = MagicMock()
    if status_code >= 400:
        import requests as _req
        resp.raise_for_status.side_effect = _req.HTTPError(
            response=resp
        )
    return resp


def test_fetch_abstract_returns_abstract_from_api(tmp_path, monkeypatch):
    """fetch_abstract parsea correctamente el XML Atom y devuelve el abstract."""
    # Redirigir cache a directorio temporal para no contaminar el cache real
    import src.novelty._cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_ROOT", tmp_path / "cache")

    with patch("requests.get", return_value=_make_response(_SAMPLE_ATOM)):
        result = fetch_abstract("2605.02064", use_cache=False)

    assert "Sidon" in result
    assert len(result) > 10


def test_fetch_abstract_normalizes_id(tmp_path, monkeypatch):
    """fetch_abstract acepta IDs con prefijo arXiv: y sin ellos."""
    import src.novelty._cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_ROOT", tmp_path / "cache")

    with patch("requests.get", return_value=_make_response(_SAMPLE_ATOM)) as mock_get:
        fetch_abstract("arXiv:2605.02064v1", use_cache=False)

    # La URL enviada debe tener el ID normalizado
    call_url = mock_get.call_args[0][0]
    assert "2605.02064" in call_url
    assert "arXiv:" not in call_url
    assert "v1" not in call_url


def test_fetch_abstract_raises_for_nonexistent_paper(tmp_path, monkeypatch):
    """fetch_abstract lanza ValueError si el paper no existe (no <entry>)."""
    import src.novelty._cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_ROOT", tmp_path / "cache")

    with patch("requests.get", return_value=_make_response(_ATOM_NO_ENTRY)):
        with pytest.raises(ValueError, match="no <entry>"):
            fetch_abstract("9999.99999", use_cache=False)


def test_fetch_abstract_retries_on_network_error(tmp_path, monkeypatch):
    """fetch_abstract reintenta 3 veces ante errores de red y falla al agotar."""
    import requests as _req
    import src.novelty._cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_ROOT", tmp_path / "cache")
    # Acelerar los sleeps para no ralentizar el test
    monkeypatch.setattr("src.novelty.paper_extractor._ABSTRACT_RETRY_DELAYS", (0, 0, 0))

    with patch("requests.get", side_effect=_req.ConnectionError("timeout")) as mock_get:
        with pytest.raises(_req.RequestException):
            fetch_abstract("2605.02064", use_cache=False)

    # 4 intentos = 3 delays + 1 final
    assert mock_get.call_count == 4


def test_fetch_abstract_no_retry_on_value_error(tmp_path, monkeypatch):
    """fetch_abstract NO reintenta si el error es semantico (paper no existe)."""
    import src.novelty._cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_ROOT", tmp_path / "cache")
    monkeypatch.setattr("src.novelty.paper_extractor._ABSTRACT_RETRY_DELAYS", (0, 0, 0))

    with patch("requests.get", return_value=_make_response(_ATOM_NO_ENTRY)) as mock_get:
        with pytest.raises(ValueError):
            fetch_abstract("9999.99999", use_cache=False)

    # Solo 1 intento — no hay retry ante ValueError
    assert mock_get.call_count == 1


def test_fetch_abstract_uses_cache(tmp_path, monkeypatch):
    """fetch_abstract devuelve el cache sin llamar a la red en el segundo llamado."""
    import src.novelty._cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_ROOT", tmp_path / "cache")

    with patch("requests.get", return_value=_make_response(_SAMPLE_ATOM)) as mock_get:
        first = fetch_abstract("2605.02064", use_cache=True)
        second = fetch_abstract("2605.02064", use_cache=True)

    assert first == second
    assert "Sidon" in first
    # Solo 1 llamada HTTP; la segunda viene del cache
    assert mock_get.call_count == 1


# ---------------------------------------------------------------------------
# fetch_abstract — live (hits real ArXiv API)
# ---------------------------------------------------------------------------

@pytest.mark.live
def test_fetch_abstract_live_2605_02064():
    """Live: obtiene el abstract real de arXiv:2605.02064 (paper de Sidon sets)."""
    result = fetch_abstract("2605.02064", use_cache=False)

    assert result, "Abstract no debe ser vacio"
    assert len(result) >= 100, f"Abstract demasiado corto: {len(result)} chars"
    assert "sidon" in result.lower(), f"Palabra 'Sidon' no encontrada en: {result[:200]}"
