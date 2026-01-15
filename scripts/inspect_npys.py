import argparse
from pathlib import Path
import numpy as np

def save_png(path: Path, x: np.ndarray, eps: float = 1e-12):
    x = np.asarray(x)
    if np.iscomplexobj(x):
        x = np.abs(x)
    x = x.astype(np.float32)
    x = x - x.min()
    x = x / (x.max() + eps)
    img = (255 * x).clip(0, 255).astype(np.uint8)

    # 用 imageio，没有就 pip install imageio
    import imageio.v2 as imageio
    imageio.imwrite(str(path), img)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run", required=True, help="run dir, e.g. runs/quick_cli")
    args = p.parse_args()

    run = Path(args.run)
    obj = np.load(run / "obj_hat.npy")
    out = run / "outputs"
    out.mkdir(parents=True, exist_ok=True)

    save_png(out / "amp.png", np.abs(obj))
    save_png(out / "phase.png", np.angle(obj))

    if (run / "pupil_hat.npy").exists():
        pupil = np.load(run / "pupil_hat.npy")
        save_png(out / "pupil_amp.png", np.abs(pupil))
        save_png(out / "pupil_phase.png", np.angle(pupil))

    print("[OK] saved pngs to", out)

if __name__ == "__main__":
    main()
