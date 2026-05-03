"""Helper interno para cachear respuestas de llamadas externas en disco.

Todas las llamadas a APIs (Leandex, Semantic Scholar, ArXiv, Anthropic) se
canalizan a traves de `cache_or_fetch` para no repetir trabajo entre runs.
Los archivos se serializan como JSON bajo `cache/novelty/<namespace>/`.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Optional


_REPO_ROOT = Path(__file__).resolve().parents[2]
CACHE_ROOT = _REPO_ROOT / "cache" / "novelty"


def _sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def cache_path(namespace: str, key: str) -> Path:
    """Devuelve la ruta del archivo de cache para `namespace`/`key`.

    `key` se hashea con SHA1 para garantizar nombres seguros en el sistema
    de archivos. Si `key` ya parece un identificador limpio (alfanumerico
    + . _ -) se usa directamente para facilitar inspeccion manual.
    """
    safe = key.replace("/", "_").replace("\\", "_")
    if all(c.isalnum() or c in "._-" for c in safe) and len(safe) <= 80:
        filename = safe
    else:
        filename = _sha1(key)
    return CACHE_ROOT / namespace / f"{filename}.json"


def load(namespace: str, key: str) -> Optional[Any]:
    """Lee del cache si existe; devuelve None si falta o esta corrupto."""
    path = cache_path(namespace, key)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def save(namespace: str, key: str, value: Any) -> None:
    """Guarda `value` (JSON-serializable) en el cache."""
    path = cache_path(namespace, key)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False)
    tmp.replace(path)


def cache_or_fetch(
    namespace: str,
    key: str,
    fetch_fn: Callable[[], Any],
    use_cache: bool = True,
) -> Any:
    """Devuelve cache hit o ejecuta `fetch_fn` y persiste el resultado.

    Si `fetch_fn` lanza una excepcion, NO se cachea; se propaga al llamador.
    El llamador es responsable de devolver un valor JSON-serializable.
    """
    if use_cache:
        cached = load(namespace, key)
        if cached is not None:
            return cached
    value = fetch_fn()
    if use_cache and value is not None:
        try:
            save(namespace, key, value)
        except (OSError, TypeError):
            pass
    return value
