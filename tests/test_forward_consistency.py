import numpy as np

from fpm.optics import make_circular_pupil, build_centers_grid
from fpm.simulate import build_demo_object, simulate_fpm_intensity
from fpm.reconstruct import reconstruct_fpm

def test_forward_and_recon_sanity():
    N, m = 128, 32
    centers = build_centers_grid(N, m, grid=7, max_shift=35)
    obj_gt = build_demo_object(N, seed=0)
    pupil = make_circular_pupil(m, radius=m*0.22)

    I = simulate_fpm_intensity(obj_gt, pupil, centers)

    assert I.shape[0] == centers.shape[0]
    assert np.all(np.isfinite(I))
    assert np.min(I) >= 0.0

    obj_est, pupil_est = reconstruct_fpm(
        I, centers, N=N, m=m, n_iters=2,
        recover_pupil=True, seed=0
    )

    assert obj_est.shape == (N, N)
    assert pupil_est.shape == (m, m)
    assert np.all(np.isfinite(obj_est))
    assert np.all(np.isfinite(pupil_est))
