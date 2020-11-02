from Objects.Lattices.Lattice import Lattice
from Objects.Lattices.PrimitiveSurface import PrimitiveSurface


class Primitive(Lattice):
    """Primitive Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def evaluatePoint(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        lattice = PrimitiveSurface(self.designSpace, self.x, self.y, self.z, self.nx,
                                   self.ny, self.nz, self.lx, self.ly, self.lz, -self.vf) - \
            PrimitiveSurface(self.designSpace, self.x, self.y, self.z, self.nx, self.ny,
                             self.nz, self.lx, self.ly, self.lz, self.vf)

        return lattice.evaluatePoint(x, y, z)
