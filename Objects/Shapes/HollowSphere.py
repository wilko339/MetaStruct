from Objects.Shapes.Shape import Shape
from Objects.Shapes.Sphere import Sphere
import numpy as np
import numexpr as ne


class HollowSphere(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, r=1, t=0.3):

        self.designSpace = designSpace

        super().__init__(self.designSpace, x, y, z)

        self.r = self.paramCheck(r)
        self.t = self.paramCheck(t)
        self.setLims()

    def setLims(self):

        self.xLims = np.array(
            [self.x - self.r, self.x + self.r])
        self.yLims = np.array(
            [self.y - self.r, self.y + self.r])
        self.zLims = np.array(
            [self.z - self.r, self.z + self.r])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.r}, {self.t})'

    def __str__(self):

        return super().__str__() + f'\nRadius: {self.r}\nWall Thickness: {self.t}'

    def evaluatePoint(self, x, y, z):

        ball = Sphere(self.designSpace, self.x, self.y, self.z, self.r) - \
            Sphere(self.designSpace, self.x, self.y, self.z, self.r -
                   self.t)

        return ball.evaluatePoint(x, y, z)
