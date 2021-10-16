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

        sx = ne.evaluate('sin((q*v + p)*pi) - l', local_dict={'q': qx, 'v':x, 'p': px, 'pi': math.pi, 'l': lx})
        sy = ne.re_evaluate(local_dict={'q': qy, 'v': y, 'p': py, 'pi': math.pi, 'l': ly})
        sz = ne.re_evaluate(local_dict={'q': qz, 'v': z, 'p': pz, 'pi': math.pi, 'l': lz})

        xy = ne.evaluate('where(s1>s2, s1, s2)', local_dict={'s1':sx, 's2':sy})
        xz = ne.re_evaluate(local_dict={'s1': sx, 's2': sz})
        yz = ne.re_evaluate(local_dict={'s1': sy, 's2': sz})

        xy_xz = ne.re_evaluate(local_dict={'s1':xy, 's2': xz})
        combine = ne.re_evaluate(local_dict={'s1': yz, 's2': xy_xz})

        return -combine
