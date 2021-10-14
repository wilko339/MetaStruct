import numexpr as ne

from MetaStruct.Objects.Lattices.DiamondSurface import DiamondSurface
from MetaStruct.Objects.Lattices.Lattice import Lattice


class Diamond(Lattice):
    """Diamond Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""


    def evaluate_point(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        vf = self.vf

        vfHigh = ne.evaluate('0.5 + vf/2')
        vfLow = ne.evaluate('0.5 - vf/2')

        lattice = DiamondSurface(self.design_space, self.x, self.y, self.z, self.nx,
                                 self.ny, self.nz, self.lx, self.ly, self.lz, vfHigh) - \
            DiamondSurface(self.design_space, self.x, self.y, self.z, self.nx, self.ny,
                           self.nz, self.lx, self.ly, self.lz, vfLow)

        for shape in lattice.shapes:

            shape.x_grid = self.x_grid
            shape.y_grid = self.y_grid
            shape.z_grid = self.z_grid

        return lattice.evaluate_point(x, y, z)
