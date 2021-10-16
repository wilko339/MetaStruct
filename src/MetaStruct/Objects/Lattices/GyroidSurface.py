import numexpr as ne

from MetaStruct.Objects.Lattices.Lattice import Lattice


class GyroidSurface(Lattice):
    """Gyroid Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction. """

    # https://tinyurl.com/ybjoblaw

    def evaluate_point(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        x0 = self.x
        y0 = self.y
        z0 = self.z
        kx = self.kx
        ky = self.ky
        kz = self.kz
        vf = self.vf

        t = ne.evaluate('(vf-0.501)/0.3325')

        expr = 'sin(kx*(x-x0))*cos(ky*(y-y0)) + \
                sin(ky * (y - y0)) * cos(kz * (z - z0)) + \
                sin(kz*(z-z0))*cos(kx*(x-x0)) - t '

        ne.set_num_threads(ne.ncores)

        return ne.evaluate(expr)
