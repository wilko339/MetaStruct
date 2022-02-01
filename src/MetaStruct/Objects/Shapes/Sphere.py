import numexpr as ne
import numpy as np

from MetaStruct.Objects.Shapes.Spheroid import Spheroid


class Sphere(Spheroid):

    def __init__(self, design_space, x=0, y=0, z=0, r=1):
        super().__init__(design_space, x, y, z, xr=r, yr=r, zr=r)

        self.r = r

    def __repr__(self):

        return f'Sphere({self.x}, {self.y}, {self.z}, {self.r})'

    def evaluate_point(self, x, y, z):

        return np.sqrt((x - self.x) ** 2 + (y - self.y) ** 2 + (z - self.z) ** 2) - self.r
