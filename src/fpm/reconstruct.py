import numpy as np
from .optics import fft2c, ifft2c, extract_patch, place_patch, make_circular_pupil

def reconstruct_fpm(
    intensities: np.ndarray,
    centers: np.ndarray,
    N: int,
    m: int,
    n_iters: int = 6,
    alpha: float = 0.8,
    beta: float = 0.2,
    recover_pupil: bool = True,
    pupil_init: np.ndarray | None = None,
    eps: float = 1e-3,
    seed: int = 0,
):
    """
    intensities: (K,m,m) float
    centers: (K,2) int
    return: (obj_est (N,N) complex spatial), (pupil_est (m,m) complex)
    """
    rng = np.random.default_rng(seed)
    K = intensities.shape[0]

    # init pupil
    if pupil_init is None:
        pupil = make_circular_pupil(m, radius=m*0.22)
    else:
        pupil = pupil_init.astype(np.complex64).copy()

    if not recover_pupil:
        beta = 0.0

    # init object (embed central LR field into HR, rest zeros)
    amp0 = np.sqrt(np.maximum(intensities[0], 0.0))
    phase0 = np.exp(1j * 2*np.pi * rng.random((m, m)).astype(np.float32))
    obj_lr0 = amp0 * phase0

    obj_hr = np.zeros((N, N), dtype=np.complex64)
    hs = m // 2
    obj_hr[N//2-hs:N//2+hs, N//2-hs:N//2+hs] = obj_lr0.astype(np.complex64)
    O = fft2c(obj_hr)
    print(intensities.shape)
    for it in range(n_iters):
        for k in range(K):
            cx, cy = int(centers[k, 0]), int(centers[k, 1])
            O_patch = extract_patch(O, cx, cy, m)

            psi = ifft2c(O_patch * pupil)
            meas_amp = np.sqrt(np.maximum(intensities[k], 0.0))
            psi_updated = meas_amp * np.exp(1j * np.angle(psi))

            PsiF_updated = fft2c(psi_updated)
            PsiF = O_patch * pupil
            dPsiF = PsiF_updated - PsiF

            # object patch update
            denom_p = (np.abs(pupil) ** 2 + eps)
            O_patch_new = O_patch + alpha * (np.conj(pupil) / denom_p) * dPsiF

            # pupil update (optional)
            if recover_pupil and beta > 0:
                denom_o = (np.abs(O_patch) ** 2 + eps)
                pupil = pupil + beta * (np.conj(O_patch) / denom_o) * dPsiF

            place_patch(O, O_patch_new, cx, cy)

        # 可选：每轮做一次轻微归一化，避免数值漂移（保守写法）
        # scale = np.mean(np.abs(ifft2c(O)))
        # if scale > 0: O /= scale

    obj_est = ifft2c(O)
    return obj_est.astype(np.complex64), pupil.astype(np.complex64)
