# cal_shape.py

"""
shape parameters (来自论文的定义：https://arxiv.org/html/2506.00486v3#S3)

μ
 is the location parameter, 
β
 is the scale parameter, 
γ
 is the shape parameter. 

我们使用scipy.stats 的 gennorm 来拟合

"""
import numpy as np
import torch
import os
from scipy.stats import gennorm
from utilities import read_pt,to_int
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import matplotlib.pyplot as plt

def cal_shape(pt_path:str,
              filter_percentile=[1, 99],
              enable_filter = True) -> dict:
    """
    计算shape_parameters
    :param pt_path: 输入pt文件的路径
    :param filter_percentile: 过滤极值的百分位数
    :param enable_filter: 是否启用过滤极值
    :return: dict: 名称和对应的shape parameters
    {
    "name":name, 
    "gamma":GAMMA,
    "mu":MU,
    "beta":BETA
    }
        
    """
    try:
        name = os.path.basename(pt_path)
        arr = to_int(read_pt(pt_path))
        if not isinstance(arr, np.ndarray):
            raise TypeError("pt_array must be a numpy array")
        # 注意，gennorm.fit返回的：
        # beta 是 shape parameter 对应论文中的 γ (GAMMA) 
        # loc 是 location parameter 对应论文中的 μ (MU)
        # scale 是 scale parameter 对应论文中的 β (BETA)
        if enable_filter:
            print("filtering...")
            low, high = np.percentile(arr, filter_percentile)
            arr = arr[(arr >= low) & (arr <= high)]
            print("filtered!")
        
        beta, loc, scale = gennorm.fit(arr)
        print("fitted!!!")
        GAMMA,MU,BETA = beta, loc, scale
        
        return {
            "name":name, 
            "gamma":GAMMA,
            "mu":MU,
            "beta":BETA
            }
        
    except Exception as e:
        print(e)
        return {
            "name":None, 
            "gamma":None,
            "mu":None,
            "beta":None
            }

def local_test():
    """
    本地测试函数
    """
    pt_path = "D:\\NYU_Files\\2025 SPRING\\Summer_Research\\新\\PYTHON\\QWEN\\dummy_files\\R_1_E_0_S_9_B_89.pt"  # 替换为实际的.pt文件路径
    result = cal_shape(pt_path)
    print(f"Shape parameters for {result['name']}: {result}")
    
    
    
# local_test()


#参考：
def reference(pt_path = "D:\\NYU_Files\\2025 SPRING\\Summer_Research\\新\\PYTHON\\QWEN\\dummy_files\\R_1_E_0_S_9_B_91.pt",
              filter_percentile=[1, 99],
              enable_filter = True):


    # 读取 .pt 文件

    arr = read_pt(pt_path)
    arr = to_int(arr,scale = 1e8)
    print("beginning to fit")
    # 转为 numpy，并过滤极值（1%-99%）
    if enable_filter:
        print("filtering...")
        low, high = np.percentile(arr, filter_percentile)
        filtered = arr[(arr >= low) & (arr <= high)]

        # ✅ 拟合 GGD（广义高斯分布）
        print("filtered!")
        beta, loc, scale = gennorm.fit(filtered)
    else:
        filtered = arr
        beta, loc, scale = gennorm.fit(arr)
    print("fitting done!")
    print(f"拟合结果: beta={beta:.4f}, loc={loc:.4e}, scale={scale:.4e}")

    # ✅ 画直方图 + 拟合曲线
    x = np.linspace(filtered.min(), filtered.max(), 1000)
    pdf = gennorm.pdf(x, beta, loc, scale)

    plt.figure(figsize=(10, 5))
    plt.hist(filtered, bins=256, density=True, alpha=0.5, label="Histogram")
    plt.plot(x, pdf, 'r-', lw=2, label=f"GGD Fit (β={beta:.2f})")
    plt.title("GGD Fit to Filtered Tensor Data (1%-99%)")
    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{os.path.basename(pt_path)}_ggd_fit__beta={beta}, loc={loc}, scale={scale}.png")
    # R_1_E_0_S_9_B_79_ggd_fit_beta=1.2665, loc=2.8365e+00, scale=4.9384e+03
    # plt.show()

    return {
        "name": os.path.basename(pt_path),
        "gamma": beta,
        "mu": loc,
        "beta": scale
    }

# reference()




def main():
    pt_paths = ["D:\\NYU_Files\\2025 SPRING\\Summer_Research\\新\\PYTHON\\QWEN\\dummy_files\\R_1_E_0_S_9_B_91.pt",
            "D:\\NYU_Files\\2025 SPRING\\Summer_Research\\新\\PYTHON\\QWEN\\dummy_files\\R_1_E_0_S_9_B_79.pt"]
    enable_filter = False
    
    
    print("total cpu:", multiprocessing.cpu_count())
    max_workers=max(4,multiprocessing.cpu_count()-2)
    print(f"working on: {max_workers}")
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(reference, pt_path, enable_filter = enable_filter): pt_path for pt_path in pt_paths}
        for future in as_completed(futures):
            pt_path = futures[future]
            try:
                result = future.result()
                print(f"Result:\n{result}\n\n")
            except Exception as e:
                print(f"Error processing {pt_path}: {e}")

# if __name__ == "__main__":
#     main()
    