import numpy as np
import numexpr as ne

from MetaStruct.Objects.Lattices.Lattice import Lattice


class DiamondSurface(Lattice):

    def evaluate_point(self, x, y, z):
        t = ne.evaluate('2.691*vf -1.333', local_dict={'vf': self.vf})

        return np.sin(self.kx * (x - self.x)) * np.sin(self.ky * (y - self.y)) * np.sin(self.kz * (z - self.z)) + \
            np.sin(self.kx * (x - self.x)) * np.cos(self.ky * (y - self.y)) * np.cos(self.kz * (z - self.z)) + \
            np.cos(self.kx * (x - self.x)) * np.sin(self.ky * (y - self.y)) * np.cos(self.kz * (z - self.z)) + \
            np.cos(self.kx * (x - self.x)) * np.cos(self.ky * (y - self.y)) * np.cos(self.kz * (z - self.z)) - t

    def evaluate_point_grid(self, x, y, z):

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