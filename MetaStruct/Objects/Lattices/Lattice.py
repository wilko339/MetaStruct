import math

import numpy as np

from MetaStruct.Objects.Booleans.Boolean import Difference, Intersection, Union, Geometry


# TODO: Compress lattice types into one class? Use dict of functions?

class Lattice(Geometry):
    morph = 'Lattice'

    def __init__(self, design_space, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, vf=0.5):
        super().__init__(design_space)

        self.name = self.__class__.__name__

        self.x = self.paramCheck(x)
        self.y = self.paramCheck(y)
        self.z = self.paramCheck(z)

        self.nx = nx
        self.ny = ny
        self.nz = nz

        self.lx = lx
        self.ly = ly
        self.lz = lz

        self.vf = vf

        self.kx = 2 * math.pi * (self.nx / self.lx)
        self.ky = 2 * math.pi * (self.ny / self.ly)
        self.kz = 2 * math.pi * (self.nz / self.lz)

        self.xLims = np.array([-self.lx, self.lx])
        self.yLims = np.array([-self.ly, self.ly])
        self.zLims = np.array([-self.lz, self.lz])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.nx}, {self.ny}, {self.nz}, {self.lx}, {self.ly}, {self.lz}, {self.vf})'

    def __str__(self):

        return f'{self.name} {self.morph}\n' + \
               f'Centre(x, y, z): ({self.x}, {self.y}, {self.z})\n' + \
               f'Number of Unit Cells per Unit Length(x, y, z): ({self.nx}, {self.ny}, {self.nz})\n' + \
               f'Unit Cell Size (x, y, z): ({self.lx}, {self.ly}, {self.lz})\n' + \
               f'Volume Fraction: {self.vf}'

    def __add__(self, other):

        return Union(self, other)

    def __sub__(self, other):

        return Difference(self, other)

    def __truediv__(self, other):

        return Intersection(self, other)

    def changeZ(self, value):

        self.lx = value
        self.ly = value
        self.lz = value
        self.kx = 2 * math.pi * (self.nx / self.lx)
        self.ky = 2 * math.pi * (self.ny / self.ly)
        self.kz = 2 * math.pi * (self.nz / self.lz)
        self.xLims = np.array([-self.lx, self.lx])
        self.yLims = np.array([-self.ly, self.ly])
        self.zLims = np.array([-self.lz, self.lz])

    def paramCheck(self, n):

        try:

            float(n)
            return n

        except ValueError:
            print(f'{n} is not a number.')
            raise
