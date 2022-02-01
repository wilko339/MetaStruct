import numexpr as ne
import numpy as np

from MetaStruct.Objects.Lattices.Lattice import Lattice


class PrimitiveSurface(Lattice):

    def evaluate_point(self, x, y, z):
        return -(np.cos(self.kx * (x - self.x)) + np.cos(self.ky * (y - self.y)) + np.cos(self.kz * (z - self.z)) -
                 self.vf)
