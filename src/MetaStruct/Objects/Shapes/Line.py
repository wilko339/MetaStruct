import numexpr as ne
import numpy as np
from numpy.linalg import norm

from MetaStruct.Objects.Misc.Vector import Vector
from MetaStruct.Objects.Shapes.Shape import Shape


def clamp(num, a, b):

    return ne.evaluate('where(where(num<b, num, b)>a, where(num<b, num, b), a)')


class Line(Shape):

    def __init__(self, design_space, p1=None, p2=None, r=0.015):
        super().__init__(design_space, p1[0], p1[1], p1[2])

        if p1 is None:
            p1 = [0, 0, 0]
        if p2 is None:
            p2 = [1, 1, 1]

        self.p1 = Vector(p1)
        self.p2 = Vector(p2)
        self.r = r

        self.x_limits = np.array(([min(p1[0], p2[0]) - r, max(p1[0], p2[0]) + r]), dtype=self.design_space.DATA_TYPE)
        self.y_limits = np.array(([min(p1[1], p2[1]) - r, max(p1[1], p2[1]) + r]), dtype=self.design_space.DATA_TYPE)
        self.z_limits = np.array(([min(p1[2], p2[2]) - r, max(p1[2], p2[2]) + r]), dtype=self.design_space.DATA_TYPE)

    def evaluate_point(self, x, y, z):

        pa = Vector([x, y, z]) - self.p1
        ba = self.p2 - self.p1

        bax = ba.x
        bay = ba.y
        baz = ba.z

        paba = pa*ba
        baba = ba*ba

        h = clamp(ne.evaluate('(paba)/(baba)'), 0.0, 1.0)

        baxh = ne.evaluate('ba*h', local_dict={'ba': bax, 'h': h})
        bayh = ne.re_evaluate({'ba': bay, 'h': h})
        bazh = ne.re_evaluate({'ba': baz, 'h': h})

        return norm(pa-Vector([baxh, bayh, bazh])) - self.r
