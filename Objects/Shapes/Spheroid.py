from Objects.Shapes.Shape import Shape
import numpy as np
import numexpr as ne


class Spheroid(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, xr=1, yr=2, zr=1, ):
        super().__init__(designSpace, x, y, z)

        self.xr = self.paramCheck(xr)
        self.yr = self.paramCheck(yr)
        self.zr = self.paramCheck(zr)

        self.xLims = np.array(
            [self.x - self.xr, self.x + self.xr])
        self.yLims = np.array(
            [self.y - self.yr, self.y + self.yr])
        self.zLims = np.array(
            [self.z - self.zr, self.z + self.zr])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.xr}, {self.yr}, {self.zr})'

    def __str__(self):

        return super().__str__() + f'\nRadii(xr, yr, zr): ({self.xr}, {self.yr}, {self.zr})'

    def evaluatePoint(self, x, y, z):

        if self.transform is not None:

            x, y, z = self.transformInputs(x, y, z)

        x0 = self.x
        y0 = self.y
        z0 = self.y
        xr = self.xr
        yr = self.yr
        zr = self.zr

        expr = '((x-x0)**2)/(xr**2) + ((y-y0)**2)/(yr**2) + ((z-z0)**2)/(zr**2) - 1'

        return ne.evaluate(expr)
