import numexpr as ne

from MetaStruct.Objects.Lattices.Lattice import Lattice


class PrimitiveSurface(Lattice):

    def evaluate_point(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z
        kx = self.kx
        ky = self.ky
        kz = self.kz
        t = self.vf

        expr = '-(cos(kx*(x-x0)) + \
                cos(ky*(y-y0)) + \
                cos(kz*(z-z0)) - \
                  t) '

        return ne.evaluate(expr)
