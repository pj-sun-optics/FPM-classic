import numpy as np
from .optics import fft2c, ifft2c, extract_patch

def build_demo_object(N: int, seed: int = 0) -> np.ndarray:
    """
    Return complex object in spatial domain, shape (N, N).
    """
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:N, 0:N]

    amp = 0.3 + 0.7 * (((xx // 16 + yy // 16) % 2).astype(np.float32))
    phase = 0.8*np.sin(2*np.pi*xx/N*6) + 0.6*np.cos(2*np.pi*yy/N*4)

    # add mild random phase texture
    phase = phase + 0.15 * rng.standard_normal((N, N)).astype(np.float32)
    obj = amp * np.exp(1j * phase)
    return obj.astype(np.complex64)

def simulate_fpm_intensity(obj_hr: np.ndarray, pupil_lr: np.ndarray, centers: np.ndarray) -> np.ndarray:
    """
    obj_hr: (N,N) complex, spatial domain
    pupil_lr: (m,m) complex
    centers: (K,2) int, (cx,cy) on HR Fourier grid
    return: I (K,m,m) float32
    """
    N = obj_hr.shape[0]
    m = pupil_lr.shape[0]
    O = fft2c(obj_hr)

    K = centers.shape[0]
    I = np.zeros((K, m, m), dtype=np.float32)
    for k in range(K):
        cx, cy = int(centers[k, 0]), int(centers[k, 1])
        O_patch = extract_patch(O, cx, cy, m)                #  取频域patch
        psi = ifft2c(O_patch * pupil_lr)                     #  取出来的patch乘pupil并做逆傅里叶变换
        I[k] = (np.abs(psi) ** 2).astype(np.float32)         #  相机最终测得的强度
    return I
