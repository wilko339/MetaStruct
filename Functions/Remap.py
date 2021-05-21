import numpy as np
import numexpr as ne

def remap(grid, lo, hi):

    [lower, upper] = [np.min(grid), np.max(grid)]

    diff_data = upper - lower
    diff_limits = hi - lo

    return ne.evaluate('lo + ((grid-lower)*(diff_limits))/(diff_data)')