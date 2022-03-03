import numpy as np


def create_modifier_array(shape, min_val=0., max_val=1., dim='x', func=None):

    res = shape.design_space.resolution

    _X = np.linspace(min_val, max_val, res[0], dtype=shape.design_space.DATA_TYPE)
    _Y = np.linspace(min_val, max_val, res[1], dtype=shape.design_space.DATA_TYPE)
    _Z = np.linspace(min_val, max_val, res[2], dtype=shape.design_space.DATA_TYPE)

    X, Y, Z = np.meshgrid(_X, _Y, _Z, indexing='ij')

    if dim == 'x':

        return X

    if dim == 'y':

        return Y

    if dim == 'z':

        return Z
