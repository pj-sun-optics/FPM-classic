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
flowchart TB
  %% Entry points
  A[scripts/simulate_data.py<br/>生成仿真数据] -->|调用| B[src/fpm/simulate.py<br/>前向模型]
  A -->|调用| C[src/fpm/optics.py<br/>FFT/pupil/patch/centers]
  B -->|输出| D[data/demo.npz<br/>I, centers, N, m, (obj_gt/pupil_gt)]
  C -->|提供工具| B

  %% Reconstruction
  E[scripts/run_recon.py<br/>运行重建并保存结果] -->|读取| D
  E -->|调用| F[src/fpm/reconstruct.py<br/>FPM迭代重建]
  E -->|调用| G[src/fpm/metrics.py<br/>RMSE/PSNR等]
  F -->|调用| C
  F -->|输出| H[results/<br/>amp.png, phase.png,<br/>pupil_amp.png, metrics.json]
  G -->|写入| H

  %% Tests
  T[tests/test_forward_consistency.py<br/>基本正确性/稳定性测试] -->|import| B
  T -->|import| F
  T -->|import| C
  T -->|运行| P[pytest -q<br/>CI/本地回归]

  %% Docs
  R[README.md<br/>说明/Quickstart/示例图] -->|展示| H
