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

Clone the repository:

```powershell
git clone https://github.com/pj-sun-optics/FPM-classic.git
cd FPM-classic
```




## Physical Process  （物理过程）

![FPM pipeline](assets/physical process.png)
