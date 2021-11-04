import numexpr as ne
import numpy as np


class Vector:

    def __init__(self, p):
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]

    @property
    def magnitude(self):
        x = self.x
        y = self.y
        z = self.z
        return ne.evaluate('sqrt(x**2 + y**2 + z**2)')

    def __sub__(self, other):
        return subtract(self, other)

    def __mul__(self, other):
        return mult(self, other)


def subtract(a, b):
    ax = a.x
    ay = a.y
    az = a.z

    bx = b.x
    by = b.y
    bz = b.z

    if ax.ndim == 0 and bx.ndim == 0:
        arrx = ax-bx
    if ay.ndim == 0 and by.ndim == 0:
        arry = ay-by
    if az.ndim == 0 and bz.ndim == 0:
        arrz = az-bz

    else:

        arrx = np.empty(ax.shape, dtype=np.float32)
        arry = np.empty(ay.shape, dtype=np.float32)
        arrz = np.empty(az.shape, dtype=np.float32)

        ne.evaluate('a-b', local_dict={'a': ax, 'b': bx}, out=arrx, casting='same_kind')
        ne.evaluate('a-b', local_dict={'a': ay, 'b': by}, out=arry, casting='same_kind')
        ne.evaluate('a-b', local_dict={'a': az, 'b': bz}, out=arrz, casting='same_kind')

    return Vector([arrx, arry, arrz])


def mult(a, b):
    ax = a.x
    ay = a.y
    az = a.z

    bx = b.x
    by = b.y
    bz = b.z

    if ax.ndim == 0 and bx.ndim == 0:
        return (ax*bx)+(ay*by)+(az*bz)

    else:
        out = np.empty_like(ax, dtype=np.float32)
        ne.evaluate('(ax*bx)+(ay*by)+(az*bz)', out=out, casting='same_kind')
        return out
