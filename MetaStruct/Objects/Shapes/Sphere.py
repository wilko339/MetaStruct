import numexpr as ne

from MetaStruct.Objects.Shapes.Spheroid import Spheroid


class Sphere(Spheroid):

    def __init__(self, design_space, x=0, y=0, z=0, r=1):
        super().__init__(design_space, x, y, z, xr=r, yr=r, zr=r)

        self.r = r

    def __repr__(self):

        return f'Sphere({self.x}, {self.y}, {self.z}, {self.r})'

    def evaluate_point(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z

        r = self.r

        return ne.evaluate('sqrt((x-x0)**2 + (y-y0)**2 + (z-z0)**2) -r')
