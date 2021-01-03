import numexpr as ne

from Objects.Shapes.Cuboid import Cuboid


class Cube(Cuboid):

    def __init__(self, designSpace, x=0, y=0, z=0, dim=1, round_r=0):
        super().__init__(designSpace, x, y, z, xd=dim, yd=dim, zd=dim)

        self.dim = dim
        self.round_r = round_r

    def __str__(self):
        return super().__str__() + f'\nCube Radius: {self.dim}'

    def ne_max(self, a, b):
        return ne.evaluate('where(a>b, a, b)')

    def ne_min(self, a, b):
        return ne.evaluate('where(a<b, a, b)')

    def evaluatePoint(self, x, y, z):
        x0 = self.x
        y0 = self.y
        z0 = self.z

        dim = self.dim
        round_r = self.round_r

        scale = dim / (dim + round_r)

        x_abs = ne.evaluate('abs(x/scale)-dim')
        y_abs = ne.evaluate('abs(y/scale)-dim')
        z_abs = ne.evaluate('abs(z/scale)-dim')

        x_max = self.ne_max(x_abs, 0.0)
        y_max = self.ne_max(y_abs, 0.0)
        z_max = self.ne_max(z_abs, 0.0)

        mag = ne.evaluate('sqrt((x_max)**2+(y_max)**2+(z_max)**2)')

        minmax = self.ne_min(self.ne_max(x_abs, self.ne_max(y_abs, z_abs)), 0.0)

        return ne.evaluate('(mag + minmax - round_r)*scale')
