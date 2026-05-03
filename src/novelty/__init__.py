"""AViD Journal - Novelty Check Module.

Pipeline en cascada (barato -> caro, parar pronto) para determinar si un
bloque matematico de un paper nuevo es novedoso respecto a Mathlib y a la
literatura indexada en Semantic Scholar / ArXiv.

Stages activos en esta version:
  0. Mathlib check via Leandex                (mathlib_checker)
  1. Semantic Scholar + ArXiv search          (arxiv_search)
  2. Block-level embedding comparison         (paper_extractor + block_comparator)
  3. Claude judge sobre pares similares       (llm_judge)

Stages 4 y 5 (formalizacion del bloque candidato + arbol de tipos, comparacion
de terminos de prueba) estan fuera de scope en v1: tras un veredicto
"equivalent" en Stage 3 se devuelve NOT_NOVEL directamente.
"""

from src.novelty.novelty_checker import (
    BlockVerdict,
    NoveltyChecker,
    NoveltyLabel,
    PaperVerdict,
)

__all__ = [
    "BlockVerdict",
    "NoveltyChecker",
    "NoveltyLabel",
    "PaperVerdict",
]
