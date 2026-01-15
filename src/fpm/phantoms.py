import numpy as np

def make_usaf_like_amp(N: int) -> np.ndarray:
    """Simple USAF-like multi-frequency bar patterns (amplitude-only, [0,1])."""
    img = np.ones((N, N), np.float32) * 0.2

    freqs = [2, 4, 8, 16, 32, 48]
    bh = N // 2
    bw = N // 3

    for i, f in enumerate(freqs):
        r0 = (i // 3) * bh
        c0 = (i % 3) * bw

        if i % 2 == 0:
            # 竖条纹：沿 x 方向变化，复制到所有行 -> (bh, bw)
            x = np.linspace(0, 1, bw, endpoint=False, dtype=np.float32)
            bars = (np.sin(2 * np.pi * f * x) > 0).astype(np.float32)   # (bw,)
            patch = np.tile(bars[None, :], (bh, 1))                    # (bh, bw)
        else:
            # 横条纹：沿 y 方向变化，复制到所有列 -> (bh, bw)
            y = np.linspace(0, 1, bh, endpoint=False, dtype=np.float32)
            bars = (np.sin(2 * np.pi * f * y) > 0).astype(np.float32)   # (bh,)
            patch = np.tile(bars[:, None], (1, bw))                     # (bh, bw)

        img[r0:r0+bh, c0:c0+bw] = 0.2 + 0.8 * patch

    return img



def make_amp_from_image(path: str, N: int, invert: bool = False) -> np.ndarray:
    """
    Load an image file as amplitude phantom in [0,1], resized to (N,N).
    Requires pillow: pip install pillow
    """
    from PIL import Image  # pillow

    img = Image.open(path).convert("L")           # grayscale
    img = img.resize((N, N), Image.BICUBIC)

    a = np.asarray(img, dtype=np.float32) / 255.0
    if invert:
        a = 1.0 - a

    # avoid exact 0 for stability
    return np.clip(a, 1e-3, 1.0).astype(np.float32)
