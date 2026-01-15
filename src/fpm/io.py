# src/fpm/io.py
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
try:
    from imageio import v2 as imageio
except Exception:
    import imageio

def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def dump_json(path: str | Path, obj: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def save_png(path: str | Path, img: np.ndarray, eps: float = 1e-12) -> None:
    """
    Save a float/complex array as a viewable PNG.
    - If complex: take abs
    - Normalize to 0..255
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    x = np.asarray(img)
    if np.iscomplexobj(x):
        x = np.abs(x)

    x = x.astype(np.float32)
    x = x - x.min()
    x = x / (x.max() + eps)
    u8 = (255.0 * x).clip(0, 255).astype(np.uint8)
    imageio.imwrite(path.as_posix(), u8)
