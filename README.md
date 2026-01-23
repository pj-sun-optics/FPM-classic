# FPM-classic

A minimal, reproducible implementation of **classic Fourier Ptychographic Microscopy (FPM)**:
- forward simulation (multi-illumination intensity stack)
- iterative reconstruction (object update; optional pupil recovery)
- basic tests for sanity & maintainability


## Quickstart

```bash
pip install -r requirements.txt

# simulate (USAF)
python scripts/simulate_data.py --out data/usaf_base.npz --phantom usaf --seed 0

# reconstruct
python scripts/run_recon.py --in data/usaf_base.npz --out runs/quickstart_usaf --n-iters 6
```

## Demo results

Amplitude | Phase | USAF-1951
:--:|:--:|:--:
<img src="assets/amp.png" width="260"> | <img src="assets/phase.png" width="260"> | <img src="assets/USAF1951.png" width="260">


(Optional) Pupil amplitude | Pupil phase
:--:|:--:
![](assets/pupil_amp.png) | ![](assets/pupil_phase.png)

## Project structure

- `src/fpm/` : core library (optics utils, forward model, reconstruction)
- `scripts/` : runnable entry points (simulate data / run reconstruction)
- `tests/` : minimal sanity tests (`pytest`)

## Setup (Windows / PowerShell)

Clone the repository:

```powershell
git clone https://github.com/pj-sun-optics/FPM-classic.git
cd FPM-classic
```




## Physical Process  （物理过程）

![FPM pipeline](assets/physical_process.png)
