
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # FPM-classic/
sys.path.insert(0, str(ROOT / "src"))
import argparse
from pathlib import Path
import numpy as np

from fpm.reconstruct import reconstruct_fpm  # 你已有

def main():
    p = argparse.ArgumentParser(description="CLI wrapper for reconstruct_fpm")
    p.add_argument("--in", dest="inp", required=True, help="input npz containing intensities/centers/N/m")
    p.add_argument("--out", required=True, help="output folder")
    p.add_argument("--n-iters", type=int, default=6)
    p.add_argument("--alpha", type=float, default=0.8)
    p.add_argument("--beta", type=float, default=0.2)
    p.add_argument("--recover-pupil", action="store_true")
    p.add_argument("--eps", type=float, default=1e-3)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--permute-centers", action="store_true")
    p.add_argument("--perm-seed", type=int, default=0)

    args = p.parse_args()

    data = np.load(args.inp, allow_pickle=True)

    intensities = data["I"]                 
    centers = data["centers"].astype(np.int32)
    N = int(np.array(data["N"]).reshape(()))
    m = int(np.array(data["m"]).reshape(()))
    pupil_init = data["pupil_gt"] if ("pupil_gt" in data.files) else None

    print(f"[load] I: {intensities.shape} {intensities.dtype}")
    print(f"[load] centers: {centers.shape} {centers.dtype}, N={N}, m={m}")



    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.permute_centers:
        rng = np.random.default_rng(args.perm_seed)
        perm = rng.permutation(intensities.shape[0])
        centers = centers[perm]
  

    recon = reconstruct_fpm(
        intensities=intensities,
        centers=centers,
        N=N,
        m=m,
        n_iters=args.n_iters,
        alpha=args.alpha,
        beta=args.beta,
        recover_pupil=args.recover_pupil,
        pupil_init=pupil_init,
        eps=args.eps,
        seed=args.seed,
    )

    
    
    pupil_hat = None

    if isinstance(recon, dict):
        obj_hat = recon.get("object", None)
        pupil_hat = recon.get("pupil", None)

    elif isinstance(recon, tuple):
   
        obj_hat = recon[0]
    if len(recon) > 1:
        pupil_hat = recon[1]

    else:
        obj_hat = recon

    if obj_hat is None:
        raise RuntimeError("reconstruct_fpm did not return object estimate.")

    np.save(out_dir / "obj_hat.npy", obj_hat)
    print("[OK] saved:", out_dir / "obj_hat.npy")

    if pupil_hat is not None:
      np.save(out_dir / "pupil_hat.npy", pupil_hat)
      print("[OK] saved:", out_dir / "pupil_hat.npy")

    print("[OK] saved:", out_dir / "obj_hat.npy")

if __name__ == "__main__":
    main()
