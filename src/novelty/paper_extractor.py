"""Stage 2 (parte 1): Descarga el source LaTeX de un paper de ArXiv y
extrae sus bloques matematicos usando el mismo parser de AViD.
"""

from __future__ import annotations

import gzip
import io
import logging
import re
import shutil
import tarfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from src.novelty import _cache
from src.parser.latex_parser import LaTeXParser

logger = logging.getLogger(__name__)

ARXIV_EPRINT_URL = "https://arxiv.org/e-print/{arxiv_id}"
USER_AGENT = "AViD-Journal/0.1 (https://github.com/ayrtonporto/avid-journal)"
REQUEST_TIMEOUT = 60

_REPO_ROOT = Path(__file__).resolve().parents[2]
ARXIV_CACHE_ROOT = _REPO_ROOT / "cache" / "novelty" / "arxiv"
INPUT_PATTERN = re.compile(r"\\(?:input|include)\{([^}]+)\}")


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
