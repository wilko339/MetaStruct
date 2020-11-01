from numpy import linalg as LA
import numpy as np

from Objects.Shapes.Shape import Shape


class Line(Shape):

    def __init__(self, x1, y1, z1, x2, y2, z2):

        self.p1 = np.array(([x1, y1, z1]))
        self.p2 = np.array(([x2, y2, z2]))
        self.l = LA.norm(self.p1 - self.p2)
        self.dir = self.p2 - self.p1

    def evaluatePoint(self, x, y, z):

        NotImplemented
