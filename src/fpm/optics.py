import numpy as np

def fft2c(x: np.ndarray) -> np.ndarray:
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(x)))

def ifft2c(X: np.ndarray) -> np.ndarray:
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(X)))

def make_circular_pupil(m: int, radius: float) -> np.ndarray:
    yy, xx = np.mgrid[-m//2:m//2, -m//2:m//2]
    rr = np.sqrt(xx**2 + yy**2)
    return (rr <= radius).astype(np.complex64)

def extract_patch(F: np.ndarray, cx: int, cy: int, m: int) -> np.ndarray:
    hs = m // 2
    return F[cy-hs:cy+hs, cx-hs:cx+hs]

def place_patch(F: np.ndarray, patch: np.ndarray, cx: int, cy: int) -> None:
    m = patch.shape[0]
    hs = m // 2
    F[cy-hs:cy+hs, cx-hs:cx+hs] = patch

def build_centers_grid(N: int, m: int, grid: int = 9, max_shift: int = 70) -> np.ndarray:
    """
    Return centers array of shape (K, 2), each row is (cx, cy) on HR Fourier grid.
    """
    c0 = N // 2
    hs = m // 2
    shifts = np.linspace(-max_shift, max_shift, grid).astype(int)

    centers = []
    for dy in shifts:
        for dx in shifts:
            cx = c0 + dx
            cy = c0 + dy
            if (cx-hs >= 0 and cx+hs < N and cy-hs >= 0 and cy+hs < N):
                centers.append((cx, cy))
    return np.array(centers, dtype=np.int32)
