import numpy as np

def rmse(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a)
    b = np.asarray(b)
    return float(np.sqrt(np.mean(np.abs(a - b) ** 2)))

def psnr(a: np.ndarray, b: np.ndarray, data_range: float | None = None) -> float:
    a = np.asarray(a)
    b = np.asarray(b)
    mse = np.mean(np.abs(a - b) ** 2)
    if mse <= 0:
        return float("inf")
    if data_range is None:
        data_range = float(np.max(np.abs(a)) - np.min(np.abs(a)) + 1e-12)
    return float(20 * np.log10(data_range) - 10 * np.log10(mse))
