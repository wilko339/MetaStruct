from Objects.Shapes.Cuboid import Cuboid
import numpy as np
import numexpr as ne


class Cube(Cuboid):

    def __init__(self, designSpace, x=0, y=0, z=0, dim=1):
        super().__init__(designSpace, x, y, z, xd=dim, yd=dim, zd=dim)

        self.dim = dim

    def __str__(self):

        return super().__str__() + f'\nCube Radius: {self.dim}'


