import numexpr as ne
import numpy as np

from MetaStruct.Objects.Shapes.Shape import Shape


class Spheroid(Shape):

    def __init__(self, design_space, x=0, y=0, z=0, xr=1, yr=2, zr=1, ):
        super().__init__(design_space, x, y, z)

        self.xr = xr
        self.yr = yr
        self.zr = zr

        self.x_limits = np.array(
            [self.x - self.xr, self.x + self.xr])
        self.y_limits = np.array(
            [self.y - self.yr, self.y + self.yr])
        self.z_limits = np.array(
            [self.z - self.zr, self.z + self.zr])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.xr}, {self.yr}, {self.zr})'

    def __str__(self):

        return super().__str__() + f'\nRadii(xr, yr, zr): ({self.xr}, {self.yr}, {self.zr})'

    def evaluate_point(self, x, y, z):

        return ((x-self.x)**2)/(self.xr**2) + ((y-self.y)**2)/(self.yr**2) + ((z-self.z)**2)/(self.zr**2) - 1
