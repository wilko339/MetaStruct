import numexpr as ne
import numpy as np

from MetaStruct.Objects.Shapes.Shape import Shape


class Cuboid(Shape):

    def __init__(self, design_space, x=0, y=0, z=0, xd=1, yd=1.5, zd=1):
        super().__init__(design_space, x, y, z)

        self.xd = xd
        self.yd = yd
        self.zd = zd

        self.x_limits = np.array(
            [self.x - self.xd, self.x + self.xd])
        self.y_limits = np.array(
            [self.y - self.yd, self.y + self.yd])
        self.z_limits = np.array(
            [self.z - self.zd, self.z + self.zd])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.xd}, {self.yd}, {self.zd})'

    def __str__(self):

        return super().__str__() + f'\nDimensions(x, y, z): ({self.xd}, {self.yd}, {self.zd})'

    def evaluate_point(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z
        xd = self.xd
        yd = self.yd
        zd = self.zd

        arr1 = ne.evaluate('(x-x0)**2 - xd**2')
        arr2 = ne.evaluate('(y-y0)**2 - yd**2')
        arr3 = ne.evaluate('(z-z0)**2 - zd**2')

        max1 = ne.evaluate('where(arr1>arr2, arr1, arr2)')

        return ne.evaluate('where(max1>arr3, max1, arr3)')
