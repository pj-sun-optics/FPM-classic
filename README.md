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

##物理流程图
flowchart TB
  %% =========================
  %% Data generation (simulate)
  %% =========================
  subgraph S0["数据生成（仿真：等价于实验拍摄）"]
    A["scripts/simulate_data.py<br/>定义 N,m,grid,max_shift<br/>生成 obj_gt, pupil_gt, centers"] 
    B["src/fpm/simulate.py<br/>simulate_fpm_intensity(obj_gt, pupil_gt, centers)"]
    C["src/fpm/optics.py<br/>fft2c/ifft2c, make_circular_pupil,<br/>extract_patch, build_centers_grid"]
    D["data/demo.npz<br/>保存: I, centers, N, m,<br/>(obj_gt, pupil_gt 可选)"]
    A -->|调用| C
    A -->|调用| B
    B -->|输出| D
    C -->|提供工具| B
  end

  %% =========================
  %% Reconstruction (inverse)
  %% =========================
  subgraph R0["重建（反问题：FPM 迭代）"]
    E["scripts/run_recon.py<br/>读取 demo.npz<br/>调用 reconstruct_fpm<br/>保存 results + metrics"]
    F["src/fpm/reconstruct.py<br/>reconstruct_fpm(I, centers, N, m,<br/>alpha, beta, eps, n_iters)"]
    G["src/fpm/metrics.py<br/>rmse/psnr 等（仿真对比 GT）"]
    H["results/<br/>amp.png, phase.png,<br/>pupil_amp.png, metrics.json"]
    E -->|读取| D
    E -->|调用| F
    E -->|调用| G
    F -->|输出| H
    G -->|写入| H
  end

  %% =========================
  %% Physics per illumination
  %% =========================
  subgraph P0["单个照明 k 的物理过程（核心：把“强度约束”回传到频域 patch）"]
    P1["(k-th illumination)<br/>由 centers[k]=(cx,cy)<br/>表示频域平移 Δk_k"]
    P2["从 HR 频谱 O 中取 patch<br/>O_patch = extract_patch(O,cx,cy,m)"]
    P3["pupil 截断/像差<br/>PsiF = O_patch * pupil"]
    P4["像面复场（预测）<br/>psi = ifft2c(PsiF)"]
    P5["相机测强度（或仿真）<br/>I_k = |psi|^2<br/>intensities[k]"]
    P6["幅度替换（测量约束）<br/>meas_amp = sqrt(I_k)<br/>psi_updated = meas_amp * exp(j*angle(psi))"]
    P7["回到频域<br/>PsiF_updated = fft2c(psi_updated)"]
    P8["误差（驱动更新）<br/>dPsiF = PsiF_updated - PsiF"]
    P9["更新物体频谱 patch<br/>O_patch_new = O_patch + alpha*(P* / (|P|^2+eps))*dPsiF"]
    P10["可选：更新 pupil（自校正）<br/>pupil = pupil + beta*(O_patch* / (|O_patch|^2+eps))*dPsiF"]
    P11["写回全局频谱 O<br/>place_patch(O,O_patch_new,cx,cy)"]
    P12["迭代结束输出<br/>obj_est = ifft2c(O)"]

    P1 --> P2 --> P3 --> P4 --> P5
    P5 --> P6 --> P7 --> P8 --> P9 --> P11 --> P12
    P8 --> P10 --> P3
  end

  %% Map physics loop to reconstruct.py
  F -. "内部循环 for it / for k 实现 P0 全部步骤<br/>变量: O,O_patch,pupil,psi,PsiF_updated,dPsiF,alpha,beta,eps" .-> P0

  %% Test linkage
  subgraph T0["测试（保证你以后改代码不把物理链路改坏）"]
    T["tests/test_forward_consistency.py<br/>import fpm.* 并做 sanity check"]
    U["pytest -q"]
    T --> U
  end
  T -. "覆盖 simulate + reconstruct + optics 的基本数值稳定性" .-> S0
  T -. "覆盖 reconstruct 内循环不 NaN/Inf" .-> R0
