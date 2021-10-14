import math

import numexpr as ne

from MetaStruct.Objects.Lattices.Lattice import Lattice


class SquareLattice(Lattice):

    def evaluate_point(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        qx = 2
        px = 0
        lx = 0.1
        qy = 2
        py = 0
        ly = 0.1
        qz = 2
        pz = 0
        lz = 0.1

        pi = math.pi

        sx = ne.evaluate('sin((qx*x + px)*pi) - lx')
        sy = ne.evaluate('sin((qy*y + py)*pi) - ly')
        sz = ne.evaluate('sin((qz*z + pz)*pi) - lz')

        xy = ne.evaluate('where(sx>sy, sx, sy)')
        xz = ne.evaluate('where(sx>sz, sx, sz)')
        yz = ne.evaluate('where(sy>sz, sy, sz)')

        xyxz = ne.evaluate('where(xy<xz, xy, xz)')
        all = ne.evaluate('where(yz<xyxz, yz, xyxz)')

        return all
