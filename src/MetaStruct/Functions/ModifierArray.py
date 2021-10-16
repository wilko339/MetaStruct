import numpy as np


def create_modifier_array(shape, min_val=0., max_val=1., dim='x', func=None):

    res = shape.design_space.resolution

    arr2D = np.linspace(min_val, max_val, res, dtype=np.dtype('f4'))

    Y, Z, X = np.meshgrid(arr2D, arr2D, arr2D)

    if dim == 'x':

        return X

    if dim == 'y':

        return Y

    if dim == 'z':

        return Z
