from Objects.Shapes.Shape import Shape
import numpy as np
import numexpr as ne


class Sphere(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, r=1):
        super().__init__(designSpace, x, y, z)

        self.r = self.paramCheck(r)

        self.setLims()
        # self.compareLims()

    def setLims(self):

        self.xLims = np.array(
            [self.x - self.r, self.x + self.r])
        self.yLims = np.array(
            [self.y - self.r, self.y + self.r])
        self.zLims = np.array(
            [self.z - self.r, self.z + self.r])

    def __repr__(self):

        return f'Sphere({self.x}, {self.y}, {self.z}, {self.r})'

    def evaluatePoint(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z
        r = self.r

        expr = '(x-x0)**2 + (y-y0)**2 + (z-z0)**2 - r**2'

        arr = ne.evaluate(expr)

        return arr
