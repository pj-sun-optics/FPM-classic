import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fpm.phantoms import make_usaf_like_amp

import argparse
import numpy as np

from fpm.optics import make_circular_pupil, build_centers_grid
from fpm.simulate import build_demo_object, simulate_fpm_intensity
from fpm.phantoms import make_usaf_like_amp, make_amp_from_image




import numpy as np




def apply_center_jitter(centers: np.ndarray, N: int, m: int, jitter_px: float, seed: int) -> np.ndarray:
    """Add Gaussian jitter to integer centers, then round+clip to keep patches in-bounds."""
    if jitter_px <= 0:
        return centers.astype(np.int32, copy=True)

    hs = m // 2
    rng = np.random.default_rng(seed)

    c = centers.astype(np.float32).copy()
    c += rng.normal(0.0, jitter_px, size=c.shape)

    # 关键：让抖动真的影响到后续 int 索引
    c = np.rint(c).astype(np.int32)

    # 关键：中心必须保证 patch 不越界
    c[:, 0] = np.clip(c[:, 0], hs, N - hs - 1)
    c[:, 1] = np.clip(c[:, 1], hs, N - hs - 1)
    return c





def main():
    p = argparse.ArgumentParser()
    
    p.add_argument("--jitter_px", type=float, default=0.0, help="Gaussian jitter (pixels) added to centers; 0 disables")
    p.add_argument("--out", type=str, default="data/demo.npz")
    p.add_argument("--N", type=int, default=256)
    p.add_argument("--m", type=int, default=64)
    p.add_argument("--grid", type=int, default=9)
    p.add_argument("--max_shift", type=int, default=70)
    p.add_argument("--pupil_radius", type=float, default=None)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--obj", type=str, default="random",
                    choices=["random", "usaf", "usaf_img"])
    p.add_argument("--obj_path", type=str, default="assets/usaf1951.png")
    p.add_argument("--invert", action="store_true")

    args = p.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    N, m = args.N, args.m
    centers = build_centers_grid(N, m, grid=args.grid, max_shift=args.max_shift)
    centers = apply_center_jitter(centers, N=N, m=m, jitter_px=args.jitter_px, seed=args.seed)
    print("centers[0:5] =", centers[:5], "| jitter_px =", args.jitter_px)


    if args.obj == "usaf":
        amp = make_usaf_like_amp(N)
        obj_gt = (amp + 0j).astype(np.complex64)
    elif args.obj == "usaf_img":
        amp = make_amp_from_image(args.obj_path, N=N, invert=args.invert)
        obj_gt = (amp + 0j).astype(np.complex64)
    else:
        obj_gt = build_demo_object(N, seed=args.seed)


    

    radius = args.pupil_radius if args.pupil_radius is not None else (m * 0.22)
    pupil_gt = make_circular_pupil(m, radius=radius)

    I = simulate_fpm_intensity(obj_gt, pupil_gt, centers)

    np.savez_compressed(
    out_path,
    I=I,
    centers=centers.astype(np.int32),   # 确保是整数中心
    N=N,
    m=m,
    pupil_radius=float(radius),

    # 新增：抖动元信息（用于验证&复现）
    jitter_px=float(args.jitter_px),
    seed=int(args.seed),

    obj_gt=obj_gt,          # 方便算指标与做对比
    pupil_gt=pupil_gt,
    )
    print(
       f"Saved: {out_path} | I shape={I.shape} | centers={centers.shape[0]} "
       f"| jitter_px={args.jitter_px} | seed={args.seed}"
    )
    print("centers[0:5] =", centers[:5])




if __name__ == "__main__":
    main()
