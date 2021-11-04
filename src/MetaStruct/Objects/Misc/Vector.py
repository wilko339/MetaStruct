import numexpr as ne
from line_profiler_pycharm import profile

import MetaStruct.vector_subtract as vs
import MetaStruct.vector_multiply as vm


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


@profile
def subtract(a, b):

    ax = a.x
    ay = a.y
    az = a.z

    bx = b.x
    by = b.y
    bz = b.z

    if ax.ndim > 0:
        arrx = ne.evaluate('ax-bx')
    if ay.ndim > 0:
        arry = ne.evaluate('ay-by')
    if az.ndim > 0:
        arrz = ne.evaluate('az-bz')


    # if ax.ndim == 3 and bx.ndim == 0:
    #     arrx_test = vs.compute_3_1(ax, bx)
    # if ay.ndim == 3 and by.ndim == 0:
    #     arry_test = vs.compute_3_1(ay, by)
    # if az.ndim == 3 and bz.ndim == 0:
    #     arrz_test = compute_3_1(az, bz)
    #
    # if ax.ndim == 3 and bx.ndim == 3:
    #     arrx_test = vs.compute_3_3(ax, bx)
    # if ay.ndim == 3 and by.ndim == 3:
    #     arry_test = vs.compute_3_3(ay, by)
    # if az.ndim == 3 and bz.ndim == 3:
    #     arrz_test = vs.compute_3_3(az, bz)

    if ax.ndim == 0 and bx.ndim == 0:
        arrx = ax - bx
    if ay.ndim == 0 and by.ndim == 0:
        arry = ay - by
    if az.ndim == 0 and bz.ndim == 0:
        arrz = az - bz

    return Vector([arrx, arry, arrz])

@profile
def mult(a, b):
    ax = a.x
    ay = a.y
    az = a.z

    bx = b.x
    by = b.y
    bz = b.z

    if ax.ndim == 0 and bx.ndim == 0:
        if ay.ndim == 0 and by.ndim == 0:
            if az.ndim == 0 and bz.ndim == 0:
                return (ax*bx)+(ay*by)+(az*bz)

    else:

        if ax.ndim == 3 and bx.ndim == 3:
            vm.compute_3_3(ax, bx, ay, by, az, bz)
            ne.evaluate('(ax*bx)+(ay*by)+(az*bz)')

        if ax.ndim == 3 and bx.ndim == 0:
            vm.compute_3_1(ax, bx, ay, by, az, bz)
            ne.evaluate('(ax*bx)+(ay*by)+(az*bz)')

        return ne.evaluate('(ax*bx)+(ay*by)+(az*bz)')
