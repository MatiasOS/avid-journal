"""Tests for exponential backoff in ArXiv search (_fetch_arxiv) and
eprint download (_download_eprint).

All tests use mocks — no real network calls.
Delay constants are monkeypatched to tiny values so tests run fast.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest
import requests

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import src.novelty.arxiv_search as arxiv_search
import src.novelty.paper_extractor as paper_extractor
from src.novelty.arxiv_search import _fetch_arxiv
from src.novelty.paper_extractor import _download_eprint

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Delays diminutos para tests rápidos (monkeypatch target)
_FAST_DELAYS = (0.01, 0.02, 0.04)

# Un resultado ficticio de _arxiv_fetch_once
_FAKE_RESULT = [{"paper_id": "http://arxiv.org/abs/1234.5678", "title": "A paper",
                 "abstract": "Abstract text", "arxiv_id": "1234.5678"}]


def _http_error(status: int):
    """Crea un arxiv.HTTPError con el status code dado."""
    import arxiv
    return arxiv.HTTPError("http://arxiv.org/search", retry=0, status=status)


def _make_response(status_code: int, content: bytes = b"data") -> MagicMock:
    """Mock de requests.Response con status_code y content."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.content = content
    return resp


# ---------------------------------------------------------------------------
# _fetch_arxiv — escenarios de backoff
# ---------------------------------------------------------------------------

class TestFetchArxivBackoff:

    def test_429_then_success(self, monkeypatch):
        """429 en primer intento → retry → éxito en segundo intento."""
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        side_effects = [_http_error(429), _FAKE_RESULT]
        with patch.object(arxiv_search, "_arxiv_fetch_once",
                          side_effect=side_effects) as mock_fetch:
            result = _fetch_arxiv("query", top_k=5)

        assert result == _FAKE_RESULT
        assert mock_fetch.call_count == 2

    def test_503_503_then_success(self, monkeypatch):
        """503 dos veces → éxito en el tercer intento."""
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        side_effects = [_http_error(503), _http_error(503), _FAKE_RESULT]
        with patch.object(arxiv_search, "_arxiv_fetch_once",
                          side_effect=side_effects) as mock_fetch:
            result = _fetch_arxiv("query", top_k=5)

        assert result == _FAKE_RESULT
        assert mock_fetch.call_count == 3

    def test_503_x4_exhausts_retries(self, monkeypatch):
        """503 cuatro veces: agota los 3 reintentos y devuelve lista vacía."""
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        side_effects = [_http_error(503)] * 4
        with patch.object(arxiv_search, "_arxiv_fetch_once",
                          side_effect=side_effects) as mock_fetch:
            result = _fetch_arxiv("query", top_k=5)

        assert result == []
        assert mock_fetch.call_count == 4  # intento inicial + 3 reintentos

    def test_404_no_retry(self, monkeypatch):
        """404 → no reintenta, devuelve lista vacía inmediatamente."""
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        side_effects = [_http_error(404)]
        with patch.object(arxiv_search, "_arxiv_fetch_once",
                          side_effect=side_effects) as mock_fetch:
            result = _fetch_arxiv("query", top_k=5)

        assert result == []
        assert mock_fetch.call_count == 1  # solo 1 intento, sin retry

    def test_400_no_retry(self, monkeypatch):
        """400 → no retryable, devuelve [] en el primer intento."""
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        with patch.object(arxiv_search, "_arxiv_fetch_once",
                          side_effect=[_http_error(400)]) as mock_fetch:
            result = _fetch_arxiv("query", top_k=5)

        assert result == []
        assert mock_fetch.call_count == 1

    def test_429_is_retryable_not_like_other_4xx(self, monkeypatch):
        """429 SÍ reintenta, a diferencia de 404/400."""
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        # 429 → éxito: si 429 no reintentara, call_count sería 1
        side_effects = [_http_error(429), _FAKE_RESULT]
        with patch.object(arxiv_search, "_arxiv_fetch_once",
                          side_effect=side_effects) as mock_fetch:
            result = _fetch_arxiv("query", top_k=5)

        assert result == _FAKE_RESULT
        assert mock_fetch.call_count == 2

    def test_network_error_retries(self, monkeypatch):
        """ConnectionError → retryable, sigue intentando."""
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        side_effects = [requests.ConnectionError("timeout"), _FAKE_RESULT]
        with patch.object(arxiv_search, "_arxiv_fetch_once",
                          side_effect=side_effects) as mock_fetch:
            result = _fetch_arxiv("query", top_k=5)

        assert result == _FAKE_RESULT
        assert mock_fetch.call_count == 2

    def test_network_error_exhausts_retries(self, monkeypatch):
        """Red falla 4 veces → lista vacía después de 3 reintentos."""
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        side_effects = [requests.ConnectionError("no route")] * 4
        with patch.object(arxiv_search, "_arxiv_fetch_once",
                          side_effect=side_effects) as mock_fetch:
            result = _fetch_arxiv("query", top_k=5)

        assert result == []
        assert mock_fetch.call_count == 4

    def test_sleep_delays_are_correct(self, monkeypatch):
        """Los delays de sleep corresponden a ARXIV_RETRY_DELAYS en orden."""
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        # 3 fallos → sleep × 3, luego éxito
        side_effects = [_http_error(503), _http_error(503), _http_error(503), _FAKE_RESULT]
        sleep_calls = []

        def spy_sleep(secs):
            sleep_calls.append(secs)

        with patch("src.novelty.arxiv_search.time.sleep", side_effect=spy_sleep):
            with patch.object(arxiv_search, "_arxiv_fetch_once",
                              side_effect=side_effects):
                _fetch_arxiv("query", top_k=5)

        assert sleep_calls == list(_FAST_DELAYS), (
            f"Sleep delays {sleep_calls} don't match ARXIV_RETRY_DELAYS {list(_FAST_DELAYS)}"
        )

    def test_returns_empty_list_not_exception_on_total_failure(self, monkeypatch):
        """Nunca debe lanzar excepción al agotarse los reintentos."""
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        with patch.object(arxiv_search, "_arxiv_fetch_once",
                          side_effect=[_http_error(503)] * 4):
            result = _fetch_arxiv("query", top_k=5)

        assert isinstance(result, list)
        assert result == []

    def test_logs_error_on_total_failure(self, monkeypatch, caplog):
        """Se loguea ERROR (no solo WARNING) al agotar todos los reintentos."""
        import logging
        monkeypatch.setattr(arxiv_search, "ARXIV_RETRY_DELAYS", _FAST_DELAYS)

        with patch.object(arxiv_search, "_arxiv_fetch_once",
                          side_effect=[_http_error(503)] * 4):
            with caplog.at_level(logging.ERROR, logger="src.novelty.arxiv_search"):
                _fetch_arxiv("query", top_k=5)

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert error_records, "Se esperaba al menos un registro ERROR al agotar reintentos"


# ---------------------------------------------------------------------------
# _download_eprint — escenarios de backoff
# ---------------------------------------------------------------------------

class TestDownloadEprintBackoff:

    def test_429_then_success(self, monkeypatch):
        """429 → retry → 200 con contenido."""
        monkeypatch.setattr(paper_extractor, "EPRINT_RETRY_DELAYS", _FAST_DELAYS)

        responses = [_make_response(429), _make_response(200, content=b"tarball")]
        with patch("requests.get", side_effect=responses) as mock_get:
            result = _download_eprint("2605.02064")

        assert result == b"tarball"
        assert mock_get.call_count == 2

    def test_503_503_then_success(self, monkeypatch):
        """503 dos veces → éxito en el tercer intento."""
        monkeypatch.setattr(paper_extractor, "EPRINT_RETRY_DELAYS", _FAST_DELAYS)

        responses = [_make_response(503), _make_response(503), _make_response(200, b"data")]
        with patch("requests.get", side_effect=responses) as mock_get:
            result = _download_eprint("2605.02064")

        assert result == b"data"
        assert mock_get.call_count == 3

    def test_503_x4_exhausts_retries(self, monkeypatch):
        """503 cuatro veces → devuelve None después de 3 reintentos."""
        monkeypatch.setattr(paper_extractor, "EPRINT_RETRY_DELAYS", _FAST_DELAYS)

        responses = [_make_response(503)] * 4
        with patch("requests.get", side_effect=responses) as mock_get:
            result = _download_eprint("2605.02064")

        assert result is None
        assert mock_get.call_count == 4

    def test_404_no_retry(self, monkeypatch):
        """404 → devuelve None sin reintentar."""
        monkeypatch.setattr(paper_extractor, "EPRINT_RETRY_DELAYS", _FAST_DELAYS)

        with patch("requests.get", return_value=_make_response(404)) as mock_get:
            result = _download_eprint("9999.99999")

        assert result is None
        assert mock_get.call_count == 1

    def test_400_no_retry(self, monkeypatch):
        """Cualquier 4xx != 429 → no retryable."""
        monkeypatch.setattr(paper_extractor, "EPRINT_RETRY_DELAYS", _FAST_DELAYS)

        for status in (400, 403, 410, 422):
            with patch("requests.get", return_value=_make_response(status)) as mock_get:
                result = _download_eprint("2605.02064")
            assert result is None, f"HTTP {status} debería devolver None"
            assert mock_get.call_count == 1, f"HTTP {status} no debe reintentar"

    def test_network_error_retries(self, monkeypatch):
        """ConnectionError → retryable, éxito en segundo intento."""
        monkeypatch.setattr(paper_extractor, "EPRINT_RETRY_DELAYS", _FAST_DELAYS)

        side_effects = [requests.ConnectionError("refused"), _make_response(200, b"ok")]
        with patch("requests.get", side_effect=side_effects) as mock_get:
            result = _download_eprint("2605.02064")

        assert result == b"ok"
        assert mock_get.call_count == 2

    def test_network_error_exhausts_retries(self, monkeypatch):
        """Red falla 4 veces → None."""
        monkeypatch.setattr(paper_extractor, "EPRINT_RETRY_DELAYS", _FAST_DELAYS)

        side_effects = [requests.ConnectionError("timeout")] * 4
        with patch("requests.get", side_effect=side_effects) as mock_get:
            result = _download_eprint("2605.02064")

        assert result is None
        assert mock_get.call_count == 4

    def test_sleep_delays_are_correct(self, monkeypatch):
        """Los delays de sleep corresponden a EPRINT_RETRY_DELAYS en orden."""
        monkeypatch.setattr(paper_extractor, "EPRINT_RETRY_DELAYS", _FAST_DELAYS)

        responses = [_make_response(503), _make_response(503), _make_response(503),
                     _make_response(200, b"data")]
        sleep_calls = []

        def spy_sleep(secs):
            sleep_calls.append(secs)

        with patch("src.novelty.paper_extractor.time.sleep", side_effect=spy_sleep):
            with patch("requests.get", side_effect=responses):
                _download_eprint("2605.02064")

        assert sleep_calls == list(_FAST_DELAYS), (
            f"Sleep delays {sleep_calls} != EPRINT_RETRY_DELAYS {list(_FAST_DELAYS)}"
        )

    def test_returns_none_not_exception_on_total_failure(self, monkeypatch):
        """No debe lanzar excepción al agotarse los reintentos."""
        monkeypatch.setattr(paper_extractor, "EPRINT_RETRY_DELAYS", _FAST_DELAYS)

        with patch("requests.get", return_value=_make_response(503)):
            result = _download_eprint("2605.02064")

        assert result is None

    def test_logs_error_on_total_failure(self, monkeypatch, caplog):
        """Se loguea ERROR al agotar todos los reintentos."""
        import logging
        monkeypatch.setattr(paper_extractor, "EPRINT_RETRY_DELAYS", _FAST_DELAYS)

        with patch("requests.get", return_value=_make_response(503)):
            with caplog.at_level(logging.ERROR, logger="src.novelty.paper_extractor"):
                _download_eprint("2605.02064")

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert error_records, "Se esperaba al menos un registro ERROR al agotar reintentos"
