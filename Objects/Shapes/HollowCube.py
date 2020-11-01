from Objects.Shapes.Shape import Shape
from Objects.Shapes.Cube import Cube

import numpy as np
import numexpr as ne


class HollowCube(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, dim=1, t=0.3):
        super().__init__(designSpace, x, y, z)

        self.dim = self.paramCheck(dim)
        self.t = self.paramCheck(t)
        self.setLims()

    def setLims(self):

        self.xLims = np.array(
            [self.x - self.dim, self.x + self.dim])
        self.yLims = np.array(
            [self.y - self.dim, self.y + self.dim])
        self.zLims = np.array(
            [self.z - self.dim, self.z + self.dim])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.dim}, {self.t})'

    def __str__(self):

        return super().__str__() + f'\nCube Radius: {self.dim}\nWall Thickness: {self.t}'

    def evaluatePoint(self, x, y, z):

        box = Cube(self.designSpace, self.x, self.y, self.z, self.dim) - \
            Cube(self.designSpace, self.x, self.y, self.z, self.dim - self.t)

        return box.evaluatePoint(x, y, z)
