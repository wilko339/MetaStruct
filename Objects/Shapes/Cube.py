from Objects.Shapes.Shape import Shape
import numpy as np
import numexpr as ne


class Cube(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, dim=1):
        super().__init__(designSpace, x, y, z)

        self.dim = self.paramCheck(dim)

        self.setLims()

    def setLims(self):

        self.xLims = np.array(
            [self.x - self.dim, self.x + self.dim])
        self.yLims = np.array(
            [self.y - self.dim, self.y + self.dim])
        self.zLims = np.array(
            [self.z - self.dim, self.z + self.dim])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.dim})'

    def __str__(self):

        return super().__str__() + f'\nCube Radius: {self.dim}'

    def evaluatePoint(self, x, y, z):

        if self.transform is not None:

            x, y, z = self.transformInputs(x, y, z)

        x0 = self.x
        y0 = self.y
        z0 = self.z
        dim = self.dim

        arr1 = ne.evaluate('(x-x0)**2 - dim**2')
        arr2 = ne.evaluate('(y-y0)**2 - dim**2')
        arr3 = ne.evaluate('(z-z0)**2 - dim**2')

        max1 = ne.evaluate('where(arr1>arr2, arr1, arr2)')

        return ne.evaluate('where(max1>arr3, max1, arr3)')
