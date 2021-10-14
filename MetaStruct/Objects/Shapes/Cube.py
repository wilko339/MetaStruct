import numexpr as ne

from MetaStruct.Objects.Shapes.Cuboid import Cuboid


class Cube(Cuboid):

    def __init__(self, design_space, x=0, y=0, z=0, dim=1, round_r=0):
        super().__init__(design_space, x, y, z, xd=dim, yd=dim, zd=dim)

        self.dim = dim
        self.round_r = round_r
        ne.set_num_threads(ne.ncores)

    def __str__(self):
        return super().__str__() + f'\nCube Radius: {self.dim}'

    def ne_max(self, a, b):
        return ne.evaluate('where(a>b, a, b)')

    def ne_min(self, a, b):
        return ne.evaluate('where(a<b, a, b)')

    def evaluate_point(self, x, y, z):
        x0 = self.x
        y0 = self.y
        z0 = self.z

        dim = self.dim
        round_r = self.round_r

        scale = dim / (dim + round_r)

        x_abs = ne.evaluate('abs((x-x0)/scale)-dim', casting='same_kind')
        y_abs = ne.re_evaluate({'x': y, 'x0': y0, 'scale': scale, 'dim': dim})
        z_abs = ne.re_evaluate({'x': z, 'x0': z0, 'scale': scale, 'dim': dim})

        x_max = ne.evaluate('where(x_abs>0.0, x_abs, 0.0)')
        y_max = ne.re_evaluate(local_dict={'x_abs': y_abs})
        z_max = ne.re_evaluate(local_dict={'x_abs': z_abs})

        mag = ne.evaluate(
            'sqrt(((where(x_abs>0.0, x_abs, 0.0))**2+((where(y_abs>0.0, y_abs, 0.0))**2+((where(z_abs>0.0, z_abs, 0.0))**2))))')

        minmax = self.ne_min(self.ne_max(
            x_abs, self.ne_max(y_abs, z_abs)), 0.0)

        return ne.evaluate('(mag + minmax - round_r)*scale')
