"""Stage 2 (parte 1): Descarga el source LaTeX de un paper de ArXiv y
extrae sus bloques matematicos usando el mismo parser de AViD.

Tambien expone `fetch_abstract` para obtener el abstract human-written de
un paper directamente desde la API de metadatos de ArXiv (Atom/OAI-PMH),
util como abstract proxy de calidad para Stage 1 de novelty checking.
"""

from __future__ import annotations

import gzip
import io
import logging
import re
import shutil
import tarfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree

import requests

from src.novelty import _cache
from src.parser.latex_parser import LaTeXParser

logger = logging.getLogger(__name__)

ARXIV_EPRINT_URL = "https://arxiv.org/e-print/{arxiv_id}"
ARXIV_METADATA_URL = "https://export.arxiv.org/api/query?id_list={arxiv_id}"
USER_AGENT = "AViD-Journal/0.1 (https://github.com/ayrtonporto/avid-journal)"
REQUEST_TIMEOUT = 60
METADATA_TIMEOUT = 10

# Atom namespace usado por la API de ArXiv
_ATOM_NS = "http://www.w3.org/2005/Atom"

# Backoff delays (segundos) para reintentos ante errores de red
_ABSTRACT_RETRY_DELAYS = (2, 5, 10)

_REPO_ROOT = Path(__file__).resolve().parents[2]
ARXIV_CACHE_ROOT = _REPO_ROOT / "cache" / "novelty" / "arxiv"
INPUT_PATTERN = re.compile(r"\\(?:input|include)\{([^}]+)\}")


# ---------------------------------------------------------------------------
# Abstract desde metadatos ArXiv
# ---------------------------------------------------------------------------

def _normalize_arxiv_id(arxiv_id: str) -> str:
    """Normaliza un arxiv_id a la forma canonica (sin prefijo ni version)."""
    aid = arxiv_id.strip()
    aid = aid.replace("arXiv:", "").replace("arxiv:", "")
    aid = aid.split("/")[-1]
    # Eliminar version (e.g. "2404.13480v2" → "2404.13480")
    if re.match(r".*v\d+$", aid):
        aid = aid.rsplit("v", 1)[0]
    return aid


def _parse_abstract_from_atom(xml_text: str) -> str:
    """Extrae el abstract del XML Atom devuelto por la API de ArXiv.

    Lanza ValueError si no hay entrada (<entry>) en la respuesta.
    Devuelve string vacio si hay entrada pero no tiene <summary>.
    """
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError as exc:
        raise ValueError(f"Invalid XML from ArXiv metadata API: {exc}") from exc

    entry = root.find(f"{{{_ATOM_NS}}}entry")
    if entry is None:
        raise ValueError("ArXiv metadata API returned no <entry> — paper ID may not exist")

    summary_el = entry.find(f"{{{_ATOM_NS}}}summary")
    if summary_el is None or not summary_el.text:
        return ""

    # Limpiar whitespace excesivo preservando separacion de parrafos
    abstract = summary_el.text.strip()
    abstract = re.sub(r"\n{2,}", "\n\n", abstract)
    abstract = re.sub(r"[ \t]+", " ", abstract)
    return abstract


def fetch_abstract(arxiv_id: str, use_cache: bool = True) -> str:
    """Obtiene el abstract human-written de un paper desde la API de metadatos
    de ArXiv.

    Usa la API Atom de export.arxiv.org, que devuelve XML con el campo
    <summary> (el abstract escrito por los autores, legible sin LaTeX).

    Args:
        arxiv_id: ID del paper (con o sin prefijo arXiv:, con o sin version).
        use_cache: Si True, usa el cache local antes de hacer la llamada HTTP.

    Returns:
        El abstract como string limpio. Puede ser string vacio si ArXiv no lo
        tiene (raro).

    Raises:
        ValueError: Si el paper no existe en ArXiv.
    """
    aid = _normalize_arxiv_id(arxiv_id)
    if not aid:
        raise ValueError(f"Invalid arxiv_id: {arxiv_id!r}")

    def _fetch() -> str:
        url = ARXIV_METADATA_URL.format(arxiv_id=aid)
        last_exc: Optional[Exception] = None

        for attempt, delay in enumerate((*_ABSTRACT_RETRY_DELAYS, None), start=1):
            try:
                response = requests.get(
                    url,
                    timeout=METADATA_TIMEOUT,
                    headers={"User-Agent": USER_AGENT},
                )
                response.raise_for_status()
                return _parse_abstract_from_atom(response.text)
            except ValueError:
                # ValueError de _parse_abstract_from_atom (paper no existe,
                # XML invalido) — no reintentamos, es un error semantico
                raise
            except requests.RequestException as exc:
                last_exc = exc
                if delay is None:
                    # Ultimo intento agotado
                    break
                logger.warning(
                    "fetch_abstract attempt %d failed for %s: %s — retrying in %ds",
                    attempt, aid, exc, delay,
                )
                time.sleep(delay)

        raise requests.RequestException(
            f"All {len(_ABSTRACT_RETRY_DELAYS) + 1} attempts failed for {aid}"
        ) from last_exc

    # El cache guarda el abstract como string; cache_or_fetch espera JSON-
    # serializable, y un string lo es. Para que el hit de cache distinga
    # None (no cacheado) de "" (paper sin abstract), guardamos {"abstract": ...}
    def _fetch_wrapped() -> Dict[str, str]:
        return {"abstract": _fetch()}

    cached = _cache.cache_or_fetch(
        namespace="arxiv_abstract",
        key=aid,
        fetch_fn=_fetch_wrapped,
        use_cache=use_cache,
    )
    if isinstance(cached, dict):
        return cached.get("abstract", "")
    # Fallback por si el cache tiene formato antiguo
    if isinstance(cached, str):
        return cached
    return ""


# ---------------------------------------------------------------------------
# Descarga / extraccion del tarball
# ---------------------------------------------------------------------------

def _download_eprint(arxiv_id: str) -> Optional[bytes]:
    url = ARXIV_EPRINT_URL.format(arxiv_id=arxiv_id)
    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            allow_redirects=True,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Failed to download %s: %s", url, exc)
        return None
    return response.content


def _extract_archive(data: bytes, dest_dir: Path) -> bool:
    """Extrae el blob a `dest_dir`. Soporta tar.gz, gzip simple y .tex pelado."""
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Intento 1: tar.gz / tar
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as tar:
            for member in tar.getmembers():
                # Proteccion contra path traversal
                target = (dest_dir / member.name).resolve()
                if not str(target).startswith(str(dest_dir.resolve())):
                    continue
                tar.extract(member, dest_dir)
            return True
    except (tarfile.TarError, EOFError):
        pass

    # Intento 2: gzip de un solo archivo
    try:
        decompressed = gzip.decompress(data)
        out_file = dest_dir / "main.tex"
        out_file.write_bytes(decompressed)
        return True
    except (OSError, EOFError):
        pass

    # Intento 3: .tex en crudo (heuristica)
    try:
        text = data.decode("utf-8", errors="ignore")
        if "\\documentclass" in text or "\\begin{document}" in text:
            (dest_dir / "main.tex").write_text(text, encoding="utf-8")
            return True
    except Exception:  # noqa: BLE001
        pass

    return False


# ---------------------------------------------------------------------------
# Localizacion del .tex principal
# ---------------------------------------------------------------------------

def _list_tex_files(root: Path) -> List[Path]:
    return sorted(p for p in root.rglob("*.tex") if p.is_file())


def _find_main_tex(root: Path) -> Optional[Path]:
    candidates = _list_tex_files(root)
    if not candidates:
        return None

    scored: List[tuple] = []
    for p in candidates:
        try:
            head = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        score = 0
        if "\\documentclass" in head:
            score += 100
        if "\\begin{document}" in head:
            score += 50
        score += len(head) // 1000
        scored.append((score, p))

    if not scored:
        return None
    scored.sort(reverse=True)
    return scored[0][1]


def _resolve_inputs(
    main_tex: Path, root: Path, max_depth: int = 5
) -> str:
    """Concatena el contenido de \\input{...} y \\include{...} (best-effort)."""
    visited: set = set()

    def _read(path: Path, depth: int) -> str:
        try:
            real = path.resolve()
        except OSError:
            return ""
        if real in visited or depth > max_depth:
            return ""
        visited.add(real)
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return ""

        def replace(match: re.Match) -> str:
            ref = match.group(1).strip()
            target = root / ref
            if target.suffix == "":
                target = target.with_suffix(".tex")
            if target.exists():
                return _read(target, depth + 1)
            alt = root / (ref + ".tex")
            if alt.exists():
                return _read(alt, depth + 1)
            return match.group(0)

        return INPUT_PATTERN.sub(replace, text)

    return _read(main_tex, 0)


# ---------------------------------------------------------------------------
# API publica
# ---------------------------------------------------------------------------

def download_arxiv_latex(
    arxiv_id: str, force: bool = False
) -> Optional[str]:
    """Descarga el source LaTeX de un paper de ArXiv y devuelve el .tex
    principal con los \\input{...} resueltos. Cachea la extraccion en
    `cache/novelty/arxiv/{arxiv_id}/`.
    """
    if not arxiv_id:
        return None

    aid = arxiv_id.strip().replace("arXiv:", "").replace("arxiv:", "")
    extracted_dir = ARXIV_CACHE_ROOT / aid

    if force and extracted_dir.exists():
        shutil.rmtree(extracted_dir, ignore_errors=True)

    needs_download = (
        not extracted_dir.exists()
        or not any(extracted_dir.iterdir())
    )
    if needs_download:
        if extracted_dir.exists():
            shutil.rmtree(extracted_dir, ignore_errors=True)
        data = _download_eprint(aid)
        if data is None:
            return None
        if not _extract_archive(data, extracted_dir):
            logger.warning("Could not extract archive for %s", aid)
            return None

    main_tex = _find_main_tex(extracted_dir)
    if main_tex is None:
        logger.warning("No main .tex found for %s", aid)
        return None

    return _resolve_inputs(main_tex, extracted_dir)


def extract_blocks(
    arxiv_id: str, use_cache: bool = True
) -> Optional[List[Dict[str, Any]]]:
    """Descarga el LaTeX y devuelve la lista de bloques parseados (cache JSON)."""
    if not arxiv_id:
        return None

    aid = arxiv_id.strip().replace("arXiv:", "").replace("arxiv:", "")

    def _do() -> Optional[List[Dict[str, Any]]]:
        text = download_arxiv_latex(aid)
        if not text:
            return None
        try:
            parser = LaTeXParser()
            return parser.parse_text(text)
        except Exception as exc:  # noqa: BLE001
            logger.warning("LaTeX parse failed for %s: %s", aid, exc)
            return None

    return _cache.cache_or_fetch(
        namespace="blocks",
        key=aid,
        fetch_fn=_do,
        use_cache=use_cache,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    blocks = extract_blocks("1706.03762", use_cache=False)
    print(f"blocks: {len(blocks) if blocks else 0}")
