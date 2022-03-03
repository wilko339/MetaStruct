from MetaStruct.Objects.Lattices.Lattice import Lattice
from MetaStruct.Objects.Lattices.PrimitiveSurface import PrimitiveSurface


class Primitive(Lattice):
    """Primitive Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def evaluate_point(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        lattice = PrimitiveSurface(self.design_space, self.x, self.y, self.z, self.nx,
                                   self.ny, self.nz, self.lx, self.ly, self.lz, -self.vf) - \
            PrimitiveSurface(self.design_space, self.x, self.y, self.z, self.nx, self.ny,
                             self.nz, self.lx, self.ly, self.lz, self.vf)

        return lattice.evaluate_point(x, y, z)

    def evaluate_point_grid(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        lattice = PrimitiveSurface(self.design_space, self.x, self.y, self.z, self.nx,
                                   self.ny, self.nz, self.lx, self.ly, self.lz, -self.vf) - \
            PrimitiveSurface(self.design_space, self.x, self.y, self.z, self.nx, self.ny,
                             self.nz, self.lx, self.ly, self.lz, self.vf)

        return lattice.evaluate_point_grid(x, y, z)
