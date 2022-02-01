import numexpr as ne
import numpy as np

from MetaStruct.Objects.Lattices.Lattice import Lattice


class GyroidSurface(Lattice):
    """Gyroid Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction. """

    # https://tinyurl.com/ybjoblaw

    def evaluate_point(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        t = ne.evaluate('(vf-0.501)/0.3325', local_dict={'vf': self.vf})

        return np.sin(self.kx * (x - self.x)) * np.cos(self.ky * (y - self.y)) + \
               np.sin(self.ky * (y - self.y)) * np.cos(self.kz * (z - self.z)) + \
               np.sin(self.kz * (z - self.z)) * np.cos(self.kx * (x - self.x)) - t
