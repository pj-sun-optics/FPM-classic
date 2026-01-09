# FPM-classic

A minimal, reproducible implementation of **classic Fourier Ptychographic Microscopy (FPM)**:
- forward simulation (multi-illumination intensity stack)
- iterative reconstruction (object update; optional pupil recovery)
- basic tests for sanity & maintainability

## Demo results

Amplitude | Phase
:--:|:--:
![](assets/amp.png) | ![](assets/phase.png)

(Optional) Pupil amplitude | Pupil phase
:--:|:--:
![](assets/pupil_amp.png) | ![](assets/pupil_phase.png)

## Project structure

- `src/fpm/` : core library (optics utils, forward model, reconstruction)
- `scripts/` : runnable entry points (simulate data / run reconstruction)
- `tests/` : minimal sanity tests (`pytest`)

## Setup (Windows / PowerShell)

```powershell
cd "F:\github code\FPM\FPM-classic"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
