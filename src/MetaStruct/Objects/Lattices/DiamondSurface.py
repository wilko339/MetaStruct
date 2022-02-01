import numpy as np
import numexpr as ne

from MetaStruct.Objects.Lattices.Lattice import Lattice


class DiamondSurface(Lattice):

    def evaluate_point(self, x, y, z):
        t = ne.evaluate('2.691*vf -1.333')

        return np.sin(self.kx * (x - self.x)) * np.sin(self.ky * (y - self.y)) * np.sin(self.kz * (z - self.z)) + \
            np.sin(self.kx * (x - self.x)) * np.cos(self.ky * (y - self.y)) * np.cos(self.kz * (z - self.z)) + \
            np.cos(self.kx * (x - self.x)) * np.sin(self.ky * (y - self.y)) * np.cos(self.kz * (z - self.z)) + \
            np.cos(self.kx * (x - self.x)) * np.cos(self.ky * (y - self.y)) * np.cos(self.kz * (z - self.z)) - t
