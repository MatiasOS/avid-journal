"""Stage 2 (parte 2): Embeddings y emparejamiento bloque-a-bloque.

Usa sentence-transformers/all-MiniLM-L6-v2 (rapido, ~80MB) para teoremas:
los enunciados son textos cortos donde el modelo generico funciona bien.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def get_model():
    """Carga (lazy, singleton) el modelo MiniLM."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        logger.info("Loading SentenceTransformer model %s...", MODEL_NAME)
        _model = SentenceTransformer(MODEL_NAME)
    return _model


@dataclass
class BlockPair:
    block_new: Dict[str, Any]
    block_candidate: Dict[str, Any]
    similarity_score: float


# ── regexes para _block_text (embedding) ─────────────────────────────────────
_LATEX_NOISE = re.compile(
    r"\\(?:label|cite|ref|eqref|footnote)\{[^}]*\}"
)
_LATEX_CMD = re.compile(r"\\[a-zA-Z]+\*?")
_LATEX_BRACES = re.compile(r"[{}]")
_WHITESPACE = re.compile(r"\s+")

# ── regexes para strip_latex_for_query (búsqueda) ────────────────────────────
# Comandos que deben eliminarse por completo junto con su argumento.
_QUERY_NOISE = re.compile(
    r"\\(?:cite|ref|label|eqref|footnote|bibitem|hyperref|url)\{[^}]*\}"
)
# Acentos LaTeX: \'a  \"o  \`e  \^i  \~n  con o sin llaves alrededor de la letra.
_QUERY_ACCENTS = re.compile(r"\\['\"`^~=.]{1}\{?([a-zA-Z])\}?")
# Comandos con argumento: \textbf{word} → word, \mathbb{N} → N.
_QUERY_CMD_WITH_ARG = re.compile(r"\\[a-zA-Z]+\*?\{([^}]*)\}")
# Comandos restantes sin argumento: \alpha → espacio.
_QUERY_CMD_BARE = re.compile(r"\\[a-zA-Z]+\*?")
# Caracteres especiales LaTeX que no aportan semántica de búsqueda.
_QUERY_SPECIAL = re.compile(r"[{}$\\~&_^]")
_QUERY_WS = re.compile(r"\s+")


def strip_latex_for_query(text: str) -> str:
    """Limpia LaTeX de un string para usarlo como query de búsqueda.

    Más agresivo que _block_text: extrae el contenido de argumentos
    {…}, translitera acentos LaTeX a su letra base, y elimina comandos
    de citación/referencia por completo. Diseñado para producir texto
    plano legible que funcione como query en Semantic Scholar / ArXiv.

    Extiende la misma estrategia de los regexes privados usados por
    _block_text, añadiendo manejo de acentos y preservación de contenido.

    Ejemplos:
        "Commutativity of addition"         → "Commutativity of addition"
        "S\\'ark\\"ozy~\\cite{Sarkozy2001}" → "Sarkozy"
        "\\textbf{Lagrange}'s theorem"      → "Lagrange 's theorem"
    """
    if not text:
        return ""
    # 1. Eliminar comandos ruidosos completos (comando + argumento).
    text = _QUERY_NOISE.sub(" ", text)
    # 2. Transliterar acentos: \'a → a, \"o → o, \^e → e, etc.
    text = _QUERY_ACCENTS.sub(r"\1", text)
    # 3. Comandos con argumento: \textbf{word} → word.
    text = _QUERY_CMD_WITH_ARG.sub(r"\1", text)
    # 4. Comandos sin argumento restantes: \alpha → espacio.
    text = _QUERY_CMD_BARE.sub(" ", text)
    # 5. Caracteres especiales LaTeX (incluyendo ~ no-break-space).
    text = _QUERY_SPECIAL.sub(" ", text)
    # 6. Colapsar whitespace.
    text = _QUERY_WS.sub(" ", text)
    return text.strip()


def _block_text(block: Dict[str, Any]) -> str:
    """Texto representativo del bloque para embedding."""
    title = (block.get("title") or "").strip()
    content = block.get("content_latex") or ""
    raw = f"{title}. {content}" if title else content
    raw = _LATEX_NOISE.sub(" ", raw)
    raw = _LATEX_CMD.sub(" ", raw)
    raw = _LATEX_BRACES.sub(" ", raw)
    raw = _WHITESPACE.sub(" ", raw)
    return raw.strip()


def embed_block(block: Dict[str, Any]) -> List[float]:
    """Embedding L2-normalizado del bloque."""
    text = _block_text(block) or "empty"
    model = get_model()
    vec = model.encode([text], convert_to_numpy=True, normalize_embeddings=True)[0]
    return vec.tolist()


def _embed_batch(blocks: List[Dict[str, Any]]):
    """Embeddings normalizados para una lista de bloques (np.ndarray)."""
    if not blocks:
        import numpy as np
        return np.zeros((0, 0))
    texts = [_block_text(b) or "empty" for b in blocks]
    model = get_model()
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)


def find_similar_pairs(
    blocks_new: List[Dict[str, Any]],
    blocks_candidate: List[Dict[str, Any]],
    threshold: float = 0.7,
) -> List[BlockPair]:
    """Devuelve pares (bloque_nuevo, bloque_candidato) con similitud >= threshold."""
    if not blocks_new or not blocks_candidate:
        return []

    emb_new = _embed_batch(blocks_new)
    emb_cand = _embed_batch(blocks_candidate)

    if emb_new.size == 0 or emb_cand.size == 0:
        return []

    # Producto de matrices: ya estan normalizados, asi que es coseno directo.
    sim_matrix = emb_new @ emb_cand.T

    pairs: List[BlockPair] = []
    for i, row in enumerate(sim_matrix):
        for j, score in enumerate(row):
            score_f = float(score)
            if score_f >= threshold:
                pairs.append(
                    BlockPair(
                        block_new=blocks_new[i],
                        block_candidate=blocks_candidate[j],
                        similarity_score=score_f,
                    )
                )

    pairs.sort(key=lambda p: p.similarity_score, reverse=True)
    return pairs


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    a = {"title": "Pythagoras", "content_latex": "$a^2 + b^2 = c^2$ for right triangles."}
    b = {"title": "Pythagorean theorem", "content_latex": "In a right triangle $a^2+b^2=c^2$."}
    c = {"title": "Euler", "content_latex": "$e^{i\\pi}+1=0$."}
    pairs = find_similar_pairs([a], [b, c], threshold=0.5)
    for p in pairs:
        print(p.similarity_score, p.block_candidate["title"])
