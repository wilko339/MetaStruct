import numexpr as ne
import numpy as np
from numpy.linalg import norm
from numba import njit, prange
import time

from MetaStruct.Objects.Misc.Vector import Vector
from MetaStruct.Objects.Shapes.Shape import Shape

from line_profiler_pycharm import profile


def clamp(num, a, b):
    return ne.evaluate('where(where(num<b, num, b)>a, where(num<b, num, b), a)')


def numpy_norm(arr):
    return norm(arr, axis=0)


@njit(fastmath=True, parallel=True)
def numba_bah(ba, h):
    out = np.empty((3, h.shape[0], h.shape[1], h.shape[2]), dtype=h.dtype)

    for i in range(3):
        for j in prange(h.shape[0]):
            for k in range(h.shape[1]):
                for l in range(h.shape[2]):
                    out[i][j][k][l] = ba[i] * h[j][k][l]

    return out


@njit(fastmath=True, parallel=True)
def numba_norm(a, r):
    norms = np.empty((a.shape[1], a.shape[2], a.shape[3]), dtype=a.dtype)
    for i in prange(a.shape[1]):
        for j in range(a.shape[2]):
            for k in range(a.shape[3]):
                norms[i][j][k] = np.sqrt(a[0][i][j][k] * a[0][i][j][k] + a[1][i][j][k] * a[1][i][j][k]
                                         + a[2][i][j][k] * a[2][i][j][k]) - r
    return norms


@njit(fastmath=True, parallel=True)
def numba_pa(x, y, z, p1):
    x_ = x.shape[0]
    y_ = y.shape[1]
    z_ = z.shape[2]

    pa = np.empty((3, x_, y_, z_), dtype=x.dtype)

    for i in prange(3):
        for j in range(x_):
            for k in range(y_):
                for l in range(z_):
                    pa[i][j][0][0] = x[j][0][0] - p1[i]
                    pa[i][0][k][0] = y[0][k][0] - p1[i]
                    pa[i][0][0][l] = z[0][0][l] - p1[i]

    return pa


class Line(Shape):

    def __init__(self, design_space, p1=None, p2=None, r=0.015):

        if p1 is None:
            p1 = [0, 0, 0]
        if p2 is None:
            p2 = [1, 1, 1]

        super().__init__(design_space, p1[0], p1[1], p1[2])

        self.p1 = Vector(p1)
        self.p1_ = np.array(p1)
        self.p2 = Vector(p2)
        self.p2_ = np.array(p2)
        self.r = r

        self.x_limits = np.array(([min(p1[0], p2[0]) - r, max(p1[0], p2[0]) + r]), dtype=self.design_space.DATA_TYPE)
        self.y_limits = np.array(([min(p1[1], p2[1]) - r, max(p1[1], p2[1]) + r]), dtype=self.design_space.DATA_TYPE)
        self.z_limits = np.array(([min(p1[2], p2[2]) - r, max(p1[2], p2[2]) + r]), dtype=self.design_space.DATA_TYPE)

    @profile
    def evaluate_point_grid(self, x, y, z):
        ts = time.time()
        pa = Vector([x, y, z]) - self.p1
        ba = self.p2 - self.p1
        bax = ba.x
        bay = ba.y
        baz = ba.z
        paba = pa * ba
        baba = ba * ba
        h = clamp(ne.evaluate('(paba)/(baba)'), 0.0, 1.0)
        baxh = ne.evaluate('ba*h', local_dict={'ba': bax, 'h': h})
        bayh = ne.re_evaluate({'ba': bay, 'h': h})
        bazh = ne.re_evaluate({'ba': baz, 'h': h})

        norm = np.linalg.norm(pa - Vector([baxh, bayh, bazh])) - self.r

        print(time.time()-ts)

        return norm

    @profile
    def evaluate_point(self, x, y, z):
        t_s = time.time()

        pa = np.array([x, y, z], dtype=object) - self.p1_

        ba_ = self.p2_ - self.p1_

        ba_h = np.empty([3, self.design_space.resolution[0], self.design_space.resolution[1],
                         self.design_space.resolution[2]])

        clip = np.clip(np.dot(pa, ba_) / np.dot(ba_, ba_), 0.0, 1.0)

        ba_h = numba_bah(ba_, clip)

        ba_h[0] -= pa[0]
        ba_h[1] -= pa[1]
        ba_h[2] -= pa[2]

        _norm = numba_norm(ba_h, self.r)

        print(time.time() - t_s)

        return _norm


class SimpleLine(Line):

    def __init__(self, design_space, p=None, l=1, r=0.25, ax='x'):

        if p is None:
            p = [0, 0, 0]

        p1 = [p[0] - l / 2, p[1], p[2]]
        p2 = [p[0] + l / 2, p[1], p[2]]

        self.centre = np.array(p)

        self.length = l
        self.ax = ax

        super().__init__(design_space, p1, p2, r)

    @profile
    def evaluate_point(self, x, y, z):

        clip = np.empty_like(self.design_space.x_grid, dtype=self.design_space.DATA_TYPE)

        if self.ax == 'x':
            np.clip(x - self.centre[0], -self.length / 2, self.length / 2, out=clip)

            return norm(np.array([x - self.centre[0] - clip, y - self.centre[1], z - self.centre[2]],
                                 dtype=self.design_space.DATA_TYPE), axis=0) - self.r

        if self.ax == 'y':
            np.clip(y - self.centre[1], -self.length / 2, self.length / 2, out=clip)

            return norm(np.array([x - self.centre[0], y - self.centre[1] - clip, z - self.centre[2]],
                                 dtype=self.design_space.DATA_TYPE), axis=0) - self.r

        if self.ax == 'z':
            np.clip(z - self.centre[2], -self.length / 2, self.length / 2, out=clip)

            return norm(np.array([x - self.centre[0], y - self.centre[1], z - self.centre[2] - clip],
                                 dtype=self.design_space.DATA_TYPE), axis=0) - self.r


class LineZ(Line):

    def __init__(self, design_space, l=1, r=0.25):
        p = [0, 0, 0]

        p1 = [p[0] - l / 2, p[1], p[2]]
        p2 = [p[0] + l / 2, p[1], p[2]]

        self.length = l
        self.r = r

        super().__init__(design_space, p1, p2, r)

    @profile
    def evaluate_point(self, x, y, z):
        clip = np.empty_like(self.design_space.x_grid, dtype=self.design_space.DATA_TYPE)

        z -= np.clip(z, -self.length / 2, self.length / 2)

        return np.linalg.norm(np.array([x, y, z - clip]), axis=0) - self.r
