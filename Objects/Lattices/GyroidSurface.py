from Objects.Lattices.Lattice import Lattice

import numexpr as ne


class GyroidSurface(Lattice):
    """Gyroid Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction. """

    # https://tinyurl.com/ybjoblaw

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, vf=0.5):

        self.vf = vf

        t = (vf-0.501)/0.3325

        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, vf)

    def evaluatePoint(self, x, y, z):
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

        return ne.evaluate(expr)
