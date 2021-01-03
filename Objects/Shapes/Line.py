import numexpr as ne
import numpy as np
from numpy.linalg import norm

from Objects.Misc.Vector import Vector
from Objects.Shapes.Shape import Shape


class Line(Shape):

    def __init__(self, designSpace, p1=[0,0,0], p2=[1,1,1], r=0.015):
        super().__init__(designSpace, p1[0], p1[1], p1[2])

        self.p1 = Vector(p1)
        self.p2 = Vector(p2)
        self.r = r

        self.xLims = np.array(([min(p1[0], p2[0])-r, max(p1[0], p2[0])+r]), dtype=self.designSpace.DATA_TYPE)
        self.yLims = np.array(([min(p1[1], p2[1])-r, max(p1[1], p2[1])+r]), dtype=self.designSpace.DATA_TYPE)
        self.zLims = np.array(([min(p1[2], p2[2])-r, max(p1[2], p2[2])+r]), dtype=self.designSpace.DATA_TYPE)

    def clamp(self, num, a, b):

        return ne.evaluate('where(where(num<b, num, b)>a, where(num<b, num, b), a)')

    def evaluatePoint(self, x, y, z):

        pa = Vector([x, y, z]) - self.p1
        ba = self.p2 - self.p1

        bax = ba.x
        bay = ba.y
        baz = ba.z

        paba = pa*ba
        baba = ba*ba

        h = self.clamp(ne.evaluate('(paba)/(baba)'), 0.0, 1.0)

        baxh = ne.evaluate('bax*h')
        bayh = ne.evaluate('bay*h')
        bazh = ne.evaluate('baz*h')

        return norm(pa-Vector([baxh, bayh, bazh])) - self.r
