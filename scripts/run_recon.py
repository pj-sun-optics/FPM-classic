import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import argparse
import json
import numpy as np
import matplotlib.pyplot as plt

from fpm.reconstruct import reconstruct_fpm
from fpm.metrics import rmse

def save_img(path: Path, img: np.ndarray, cmap: str = "gray"):
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.imsave(path, img, cmap=cmap)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=str, default="data/demo.npz")
    p.add_argument("--out", type=str, default="results")
    p.add_argument("--iters", type=int, default=6)
    p.add_argument("--alpha", type=float, default=0.8)
    p.add_argument("--beta", type=float, default=0.2)
    p.add_argument("--recover_pupil", action="store_true")
    p.add_argument("--no_recover_pupil", action="store_true")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    recover_pupil = args.recover_pupil and (not args.no_recover_pupil)
    # 默认开启 pupil recovery（更符合你后续做系统失配/像差的路线）
    if (not args.recover_pupil) and (not args.no_recover_pupil):
        recover_pupil = True

    data = np.load(args.data, allow_pickle=True)
    I = data["I"]
    centers = data["centers"]
    N = int(data["N"])
    m = int(data["m"])

    obj_est, pupil_est = reconstruct_fpm(
        I, centers, N=N, m=m,
        n_iters=args.iters,
        alpha=args.alpha,
        beta=args.beta,
        recover_pupil=recover_pupil,
        seed=args.seed,
    )

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    save_img(out_dir / "amp.png", np.abs(obj_est))
    save_img(out_dir / "phase.png", np.angle(obj_est), cmap="twilight")

    save_img(out_dir / "pupil_amp.png", np.abs(pupil_est))
    save_img(out_dir / "pupil_phase.png", np.angle(pupil_est), cmap="twilight")

    metrics = {"recover_pupil": recover_pupil}
    if "obj_gt" in data:
        obj_gt = data["obj_gt"]
        metrics["rmse_amp"] = rmse(np.abs(obj_gt), np.abs(obj_est))
        metrics["rmse_phase"] = rmse(np.angle(obj_gt), np.angle(obj_est))

    with open(out_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Saved results to: {out_dir}")
    print(metrics)

if __name__ == "__main__":
    main()
