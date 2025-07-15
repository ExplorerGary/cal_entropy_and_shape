# scaling checker:
from scipy.stats import gennorm
import numpy as np

x = np.random.laplace(loc=0, scale=1, size=10000)  # 这是 gamma=1 的 GGD 特例（Laplace）
beta1, mu1, scale1 = gennorm.fit(x)

x_scaled = x * 1e8
beta2, mu2, scale2 = gennorm.fit(x_scaled)

print(f"Original:  γ={beta1:.4f}, μ={mu1:.4f}, β={scale1:.4f}")
print(f"Scaled  :  γ={beta2:.4f}, μ={mu2:.4e}, β={scale2:.4e}")

print(f"Scale factor: {scale2 / scale1:.4f}"
      f" (should be 1e8)")
print(f"μ ratio: {mu2 / mu1:.4f} (should be 1e8)")