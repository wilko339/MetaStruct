from Objects.Lattices.Lattice import Lattice

import numexpr as ne


class DiamondSurface(Lattice):

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, vf=0.5):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, vf)

    def evaluatePoint(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z
        kx = self.kx
        ky = self.ky
        kz = self.kz
        vf = self.vf
        t = ne.evaluate('2.691*vf -1.333')

        expr = 'sin(kx * (x - x0)) * sin(ky * (y - y0)) * sin(kz * (z - z0)) + \
                sin(kx * (x - x0)) * cos(ky * (y - y0)) * cos(kz * (z - z0)) + \
                cos(kx * (x - x0)) * sin(ky * (y - y0)) * cos(kz * (z - z0)) + \
                cos(kx * (x - x0)) * cos(ky * (y - y0)) * cos(kz * (z - z0)) - t'

        return ne.evaluate(expr)
