import numpy as np


def createModifierArray(shape, minVal=0., maxVal=1., dim='x', func=None):

    res = shape.design_space.resolution

    arr2D = np.linspace(minVal, maxVal, res, dtype=np.dtype('f4'))

    Y, Z, X = np.meshgrid(arr2D, arr2D, arr2D)

    if dim == 'x':

        return X

    if dim == 'y':

        return Y

    if dim == 'z':

        return Z
