import numexpr as ne
from Objects.Lattices.Gyroid import Gyroid
from Objects.DesignSpace import DesignSpace
from math import sin, cos
from numba import vectorize
from numpy import ascontiguousarray

import cProfile
import pstats
import io
import time


@vectorize(['float32(float32, float32, float32, float32, float32, float32, float32, float32, float32, float32)'], target='cuda')
def evaluate_point_cuda(x, y, z, x0, y0, z0, kx, ky, kz, t):
    a = sin(kx * (x - x0)) * cos(ky * (y - y0))
    b = sin(ky * (y - y0)) * cos(kz * (z - z0))
    c = sin(kz * (z - z0)) * cos(kx * (x - x0))

    return a + b + c - t


def evaluate_point_ne(x, y, z, x0, y0, z0, kx, ky, kz, t):
    """Returns the function value at point (x, y, z)."""

    expr = 'sin(kx*(x-x0))*cos(ky*(y-y0)) + \
                sin(ky * (y - y0)) * cos(kz * (z - z0)) + \
                sin(kz*(z-z0))*cos(kx*(x-x0)) - t '

    ne.set_num_threads(ne.ncores)

    return ne.evaluate(expr)


def main():

    ds = DesignSpace(1000)

    latt = Gyroid(ds)

    t = (latt.vf-0.501)/0.3325

    x = ascontiguousarray(ds.coordinate_list[:, 0])
    y = ascontiguousarray(ds.coordinate_list[:, 1])
    z = ascontiguousarray(ds.coordinate_list[:, 2])

    t_start = time.time()

    a = evaluate_point_cuda(x, y, z, latt.x, latt.y, latt.z,
                            latt.kx, latt.ky, latt.kz, t)

    print(time.time() - t_start)


if __name__ == '__main__':
    main()
