# ggd_entropy.py

import numpy as np
from scipy.special import gamma

def ggd_entropy(alpha, beta, base=np.e):
    """Return differential entropy of GGD with given scale alpha and shape beta."""
    H = np.log(2 * alpha * gamma(1 / beta)) + (1 - 1 / beta)
    if base == 2:
        return H / np.log(2)
    return H

def local_test():
    
    
    
    pass