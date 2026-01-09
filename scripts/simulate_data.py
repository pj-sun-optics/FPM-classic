import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import argparse
import numpy as np

from fpm.optics import make_circular_pupil, build_centers_grid
from fpm.simulate import build_demo_object, simulate_fpm_intensity

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="data/demo.npz")
    p.add_argument("--N", type=int, default=256)
    p.add_argument("--m", type=int, default=64)
    p.add_argument("--grid", type=int, default=9)
    p.add_argument("--max_shift", type=int, default=70)
    p.add_argument("--pupil_radius", type=float, default=None)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    N, m = args.N, args.m
    centers = build_centers_grid(N, m, grid=args.grid, max_shift=args.max_shift)

    obj_gt = build_demo_object(N, seed=args.seed)

    radius = args.pupil_radius if args.pupil_radius is not None else (m * 0.22)
    pupil_gt = make_circular_pupil(m, radius=radius)

    I = simulate_fpm_intensity(obj_gt, pupil_gt, centers)

    np.savez_compressed(
        out_path,
        I=I,
        centers=centers,
        N=N,
        m=m,
        pupil_radius=float(radius),
        obj_gt=obj_gt,          # 方便算指标与做对比
        pupil_gt=pupil_gt,
    )
    print(f"Saved: {out_path} | I shape={I.shape} | centers={centers.shape[0]}")

if __name__ == "__main__":
    main()
