from Objects.Lattices.Lattice import Lattice

import numexpr as ne


class PrimitiveSurface(Lattice):

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, vf=0.9):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, vf)

    def evaluatePoint(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z
        kx = self.kx
        ky = self.ky
        kz = self.kz
        t = self.vf

        expr = '-(cos(kx*(x-x0)) + \
                 cos(ky*(y-y0)) - \
                  t) '

        return ne.evaluate(expr)
