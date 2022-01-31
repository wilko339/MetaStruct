import numexpr as ne
import numpy as np
from numpy.linalg import norm
from numba import njit

from MetaStruct.Objects.Misc.Vector import Vector
from MetaStruct.Objects.Shapes.Shape import Shape

from line_profiler_pycharm import profile


def clamp(num, a, b):
    return ne.evaluate('where(where(num<b, num, b)>a, where(num<b, num, b), a)')


def numpy_norm(arr):
    return norm(arr, axis=0)


class Line(Shape):

    def __init__(self, design_space, p1=None, p2=None, r=0.015):
        super().__init__(design_space, p1[0], p1[1], p1[2])

        if p1 is None:
            p1 = [0, 0, 0]
        if p2 is None:
            p2 = [1, 1, 1]

        self.p1 = Vector(p1)
        self.p1_ = np.array(p1)
        self.p2 = Vector(p2)
        self.p2_ = np.array(p2)
        self.r = r

        self.x_limits = np.array(([min(p1[0], p2[0]) - r, max(p1[0], p2[0]) + r]), dtype=self.design_space.DATA_TYPE)
        self.y_limits = np.array(([min(p1[1], p2[1]) - r, max(p1[1], p2[1]) + r]), dtype=self.design_space.DATA_TYPE)
        self.z_limits = np.array(([min(p1[2], p2[2]) - r, max(p1[2], p2[2]) + r]), dtype=self.design_space.DATA_TYPE)

    @profile
    def evaluate_point(self, x, y, z):
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

        return np.linalg.norm(pa-Vector([baxh, bayh, bazh])) - self.r

    @profile
    def evaluate_point_bc(self, x_, y_, z_):

        pa_x = x_ - self.p1_[0]
        pa_y = y_ - self.p1_[1]
        pa_z = z_ - self.p1_[2]

        ba_ = self.p1_ - self.p2_
        baba_ = np.dot(ba_, ba_)

        paba_ = np.dot(np.array([pa_x, pa_y, pa_z], dtype=object), ba_)

        return norm(np.einsum('i,jkl->ijkl', ba_, np.clip((paba_ / baba_), 0.0, 1.0), dtype=self.design_space.DATA_TYPE,
                  casting='same_kind', optimize=True), axis=0) - self.r


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

            return np.linalg.norm(np.array([x - self.centre[0] - clip, y - self.centre[1], z - self.centre[2]],
                                           dtype=self.design_space.DATA_TYPE), axis=0) - self.r

        if self.ax == 'y':
            np.clip(y - self.centre[1], -self.length / 2, self.length / 2, out=clip)

            return np.linalg.norm(np.array([x - self.centre[0], y - self.centre[1] - clip, z - self.centre[2]],
                                           dtype=self.design_space.DATA_TYPE), axis=0) - self.r

        if self.ax == 'z':
            np.clip(z - self.centre[2], -self.length / 2, self.length / 2, out=clip)

            return np.linalg.norm(np.array([x - self.centre[0], y - self.centre[1], z - self.centre[2] - clip],
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
