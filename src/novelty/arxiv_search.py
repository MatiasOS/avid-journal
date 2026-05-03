"""Stage 1: Busqueda de papers candidatos en Semantic Scholar y ArXiv.

Recupera papers cuyo abstract es semanticamente similar al del paper nuevo
para acotar el espacio de comparacion antes de Stages 2-3 (mas caros).

Estrategia v1:
  - Semantic Scholar paper/search: usa el ranking del propio servicio + el
    embedding SPECTER2 que devuelve la API cuando se pide en `fields`.
    Como SS no expone "embed arbitrary text", calculamos `similarity_score`
    via MiniLM (block_comparator) entre el abstract de consulta y el del
    candidato. Si SS devuelve `embedding.vector` lo guardamos para usos
    futuros pero no lo combinamos en el score base.
  - ArXiv: paquete `arxiv` con sort_by=Relevance.
  - Deduplicar por arxiv_id, filtrar por threshold, ordenar desc.
"""

from __future__ import annotations

import logging
import os
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional

import requests
from dotenv import load_dotenv

from src.novelty import _cache

load_dotenv()

logger = logging.getLogger(__name__)

SEMANTIC_SCHOLAR_ENDPOINT = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_FIELDS = "title,abstract,externalIds,embedding"
REQUEST_TIMEOUT = 30


@dataclass
class PaperCandidate:
    paper_id: str
    title: str
    abstract: str
    arxiv_id: Optional[str]
    similarity_score: float = 0.0
    embedding: Optional[List[float]] = None
    source: str = "semantic_scholar"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PaperCandidate":
        return cls(
            paper_id=data.get("paper_id", ""),
            title=data.get("title", ""),
            abstract=data.get("abstract", ""),
            arxiv_id=data.get("arxiv_id"),
            similarity_score=float(data.get("similarity_score", 0.0)),
            embedding=data.get("embedding"),
            source=data.get("source", "semantic_scholar"),
        )


# ---------------------------------------------------------------------------
# Similitud (importacion lazy para evitar cargar MiniLM si no hace falta)
# ---------------------------------------------------------------------------

def _cosine_similarity_text(a: str, b: str) -> float:
    """Cosine similarity entre dos textos via MiniLM (lazy import)."""
    from src.novelty import block_comparator

    if not a or not b:
        return 0.0
    model = block_comparator.get_model()
    embeddings = model.encode([a, b], convert_to_numpy=True, normalize_embeddings=True)
    return float(embeddings[0] @ embeddings[1])


# ---------------------------------------------------------------------------
# Semantic Scholar
# ---------------------------------------------------------------------------

def _ss_headers() -> Dict[str, str]:
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    headers = {"Accept": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key
    return headers


def _truncate_query(text: str, max_chars: int = 250) -> str:
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0]


def _fetch_semantic_scholar(query: str, top_k: int) -> Dict[str, Any]:
    try:
        response = requests.get(
            SEMANTIC_SCHOLAR_ENDPOINT,
            params={
                "query": query,
                "limit": top_k,
                "fields": SEMANTIC_SCHOLAR_FIELDS,
            },
            headers=_ss_headers(),
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Semantic Scholar request failed: %s", exc)
        return {"data": [], "error": str(exc)}
    try:
        return response.json()
    except ValueError:
        return {"data": [], "error": "invalid_json"}


def search_semantic_scholar(
    abstract: str,
    top_k: int = 20,
    use_cache: bool = True,
) -> List[PaperCandidate]:
    """Busca candidatos via Semantic Scholar y los rankea por similitud MiniLM."""
    if not abstract or not abstract.strip():
        return []

    query = _truncate_query(abstract)
    cache_key = f"ss::{top_k}::{query}"
    payload = _cache.cache_or_fetch(
        namespace="search_ss",
        key=cache_key,
        fetch_fn=lambda: _fetch_semantic_scholar(query, top_k),
        use_cache=use_cache,
    )

    raw_papers = payload.get("data") or []
    candidates: List[PaperCandidate] = []
    for paper in raw_papers:
        external = paper.get("externalIds") or {}
        arxiv_id = external.get("ArXiv") or external.get("arxiv")
        if not arxiv_id:
            continue
        embedding_obj = paper.get("embedding") or {}
        embedding_vector = (
            embedding_obj.get("vector") if isinstance(embedding_obj, dict) else None
        )
        candidate = PaperCandidate(
            paper_id=str(paper.get("paperId") or ""),
            title=paper.get("title") or "",
            abstract=paper.get("abstract") or "",
            arxiv_id=str(arxiv_id),
            similarity_score=0.0,
            embedding=embedding_vector,
            source="semantic_scholar",
        )
        candidates.append(candidate)

    # Score por similitud MiniLM entre abstract de consulta y de cada candidato.
    for cand in candidates:
        try:
            cand.similarity_score = _cosine_similarity_text(abstract, cand.abstract)
        except Exception as exc:  # noqa: BLE001
            logger.warning("MiniLM scoring failed for %s: %s", cand.paper_id, exc)
            cand.similarity_score = 0.0

    candidates.sort(key=lambda c: c.similarity_score, reverse=True)
    return candidates


# ---------------------------------------------------------------------------
# ArXiv
# ---------------------------------------------------------------------------

def _fetch_arxiv(query: str, top_k: int) -> List[Dict[str, Any]]:
    try:
        import arxiv
    except ImportError:
        logger.warning("arxiv package not installed")
        return []

    try:
        search = arxiv.Search(
            query=query,
            max_results=top_k,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        results = []
        for r in search.results():
            arxiv_id = r.entry_id.rsplit("/", 1)[-1]
            arxiv_id = arxiv_id.replace("abs/", "")
            if "v" in arxiv_id:
                arxiv_id = arxiv_id.split("v", 1)[0] if arxiv_id.split("v", 1)[1].isdigit() else arxiv_id
            results.append(
                {
                    "paper_id": r.entry_id,
                    "title": r.title or "",
                    "abstract": r.summary or "",
                    "arxiv_id": arxiv_id,
                }
            )
        return results
    except Exception as exc:  # noqa: BLE001
        logger.warning("ArXiv search failed: %s", exc)
        return []


def search_arxiv(
    query: str,
    top_k: int = 10,
    reference_text: Optional[str] = None,
    use_cache: bool = True,
) -> List[PaperCandidate]:
    """Busca candidatos directamente en ArXiv.

    `reference_text` (opcional) se usa para calcular `similarity_score` via
    MiniLM. Si no se pasa, el score queda en 0.0 (los candidatos solo aportan
    cobertura adicional para el dedup).
    """
    if not query or not query.strip():
        return []

    cache_key = f"arxiv::{top_k}::{query.strip()}"
    raw = _cache.cache_or_fetch(
        namespace="search_arxiv",
        key=cache_key,
        fetch_fn=lambda: _fetch_arxiv(query, top_k),
        use_cache=use_cache,
    )

    candidates: List[PaperCandidate] = []
    for entry in raw:
        cand = PaperCandidate(
            paper_id=entry.get("paper_id", ""),
            title=entry.get("title", ""),
            abstract=entry.get("abstract", ""),
            arxiv_id=entry.get("arxiv_id"),
            similarity_score=0.0,
            embedding=None,
            source="arxiv",
        )
        candidates.append(cand)

    if reference_text:
        for cand in candidates:
            try:
                cand.similarity_score = _cosine_similarity_text(
                    reference_text, cand.abstract
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("MiniLM scoring failed for %s: %s", cand.paper_id, exc)
                cand.similarity_score = 0.0

    candidates.sort(key=lambda c: c.similarity_score, reverse=True)
    return candidates


# ---------------------------------------------------------------------------
# Combinacion / dedup / filtro
# ---------------------------------------------------------------------------

def _normalize_arxiv_id(arxiv_id: Optional[str]) -> Optional[str]:
    if not arxiv_id:
        return None
    aid = arxiv_id.strip()
    aid = aid.replace("arXiv:", "").replace("arxiv:", "")
    aid = aid.split("/")[-1]
    return aid or None


def combine_and_filter(
    candidates: Iterable[PaperCandidate],
    threshold: float = 0.3,
) -> List[PaperCandidate]:
    """Deduplica por arxiv_id, filtra por umbral y ordena desc."""
    by_id: Dict[str, PaperCandidate] = {}
    for cand in candidates:
        key = _normalize_arxiv_id(cand.arxiv_id)
        if not key:
            continue
        cand.arxiv_id = key
        existing = by_id.get(key)
        if existing is None:
            by_id[key] = cand
            continue
        # Conservar la entrada con mas metadata o mayor score.
        if (
            cand.similarity_score > existing.similarity_score
            or (not existing.abstract and cand.abstract)
            or (not existing.embedding and cand.embedding)
        ):
            # Combinar campos utiles
            cand.embedding = cand.embedding or existing.embedding
            cand.abstract = cand.abstract or existing.abstract
            cand.title = cand.title or existing.title
            cand.similarity_score = max(cand.similarity_score, existing.similarity_score)
            by_id[key] = cand

    filtered = [c for c in by_id.values() if c.similarity_score >= threshold]
    filtered.sort(key=lambda c: c.similarity_score, reverse=True)
    return filtered


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_abs = (
        "We prove a new bound on the number of squarefree integers in short intervals "
        "by combining sieve methods with bounds on character sums."
    )
    ss = search_semantic_scholar(sample_abs, top_k=5, use_cache=False)
    print(f"SS candidates: {len(ss)}")
    for c in ss[:3]:
        print(f"  {c.arxiv_id} sim={c.similarity_score:.3f} - {c.title[:60]}")
