import numexpr as ne
import numpy as np


def remap(grid, lo=0, hi=1):

    [lower, upper] = [np.min(grid), np.max(grid)]

    diff_data = upper - lower
    diff_limits = hi - lo

    return ne.evaluate('lo + ((grid-lower)*(diff_limits))/(diff_data)')
