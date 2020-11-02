from Objects.Shapes.Spheroid import Spheroid
import numpy as np
import numexpr as ne


class Sphere(Spheroid):

    def __init__(self, designSpace, x=0, y=0, z=0, r=1):
        super().__init__(designSpace, x, y, z, xr=r, yr=r, zr=r)

        self.r = r

    def __repr__(self):

        return f'Sphere({self.x}, {self.y}, {self.z}, {self.r})'

