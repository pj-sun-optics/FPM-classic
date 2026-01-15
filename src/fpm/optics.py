import numpy as np

def fft2c(x: np.ndarray) -> np.ndarray:
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(x)))

def ifft2c(X: np.ndarray) -> np.ndarray:
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(X)))

##生成一个圆形的孔径函数
def make_circular_pupil(m: int, radius: float) -> np.ndarray:
    yy, xx = np.mgrid[-m//2:m//2, -m//2:m//2]
    rr = np.sqrt(xx**2 + yy**2)
    return (rr <= radius).astype(np.complex64)


##从全局频谱 F 中提取出以 (cx,cy) 为中心，边长为 m 的子矩阵
def extract_patch(F: np.ndarray, cx: int, cy: int, m: int) -> np.ndarray:
    hs = m // 2
    return F[cy-hs:cy+hs, cx-hs:cx+hs]


##把全局频谱 F 的某一块，用我现在算出来的新子矩阵覆盖掉
def place_patch(F: np.ndarray, patch: np.ndarray, cx: int, cy: int) -> None:
    m = patch.shape[0]
    hs = m // 2
    F[cy-hs:cy+hs, cx-hs:cx+hs] = patch



##该函数在频域中定义了一组理想的照明频移中心，假设每个照明角对应的频谱平移位置是严格已知的，并以此在全局高分辨率频谱上定位各个子孔径。
def build_centers_grid(N: int, m: int, grid: int = 9, max_shift: int = 70) -> np.ndarray:
    """
    Return centers array of shape (K, 2), each row is (cx, cy) on HR Fourier grid.
    """
    c0 = N // 2
    hs = m // 2
    shifts = np.linspace(-max_shift, max_shift, grid).astype(int)




    centers = []
    for dy in shifts:
        for dx in shifts:
            cx = c0 + dx
            cy = c0 + dy
            if (cx-hs >= 0 and cx+hs < N and cy-hs >= 0 and cy+hs < N):
                centers.append((cx, cy))    


    return np.array(centers, dtype=np.int32)

