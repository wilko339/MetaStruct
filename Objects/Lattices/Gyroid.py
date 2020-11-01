from Objects.Lattices.Lattice import Lattice
from Objects.Lattices.GyroidSurface import GyroidSurface

import numexpr as ne


class Gyroid(Lattice):
    """Gyroid Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, vf=0.5):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, vf)

        self.coordSys = 'car'

    def evaluatePoint(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        if self.transform is not None:

            x, y, z = self.transformInputs(x, y, z)

        vf = self.vf

        vfHigh = ne.evaluate('0.5 + vf/2')
        vfLow = ne.evaluate('0.5 - vf/2')

        lattice = GyroidSurface(self.designSpace, self.x, self.y, self.z, self.nx,
                                self.ny, self.nz, self.lx, self.ly, self.lz, vfHigh) - \
            GyroidSurface(self.designSpace, self.x, self.y, self.z, self.nx, self.ny,
                          self.nz, self.lx, self.ly, self.lz, vfLow)

        for shape in lattice.shapes:

            shape.XX = self.XX
            shape.YY = self.YY
            shape.ZZ = self.ZZ

        return lattice.evaluatePoint(x, y, z)
