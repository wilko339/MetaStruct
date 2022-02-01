import numpy as np

from MetaStruct.Objects.Shapes.Shape import Shape


class Cuboid(Shape):

    def __init__(self, design_space, x=0, y=0, z=0, xd=1, yd=1.5, zd=1):
        super().__init__(design_space, x, y, z)

        self.xd = xd
        self.yd = yd
        self.zd = zd

        self.x_limits = np.array(
            [self.x - self.xd, self.x + self.xd])
        self.y_limits = np.array(
            [self.y - self.yd, self.y + self.yd])
        self.z_limits = np.array(
            [self.z - self.zd, self.z + self.zd])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.xd}, {self.yd}, {self.zd})'

    def __str__(self):

        return super().__str__() + f'\nDimensions(x, y, z): ({self.xd}, {self.yd}, {self.zd})'

    def evaluate_point(self, x, y, z):

        x_abs = np.abs(x) - self.xd
        y_abs = np.abs(y) - self.yd
        z_abs = np.abs(z) - self.zd

        x_max = np.maximum(x_abs, 0)
        y_max = np.maximum(y_abs, 0)
        z_max = np.maximum(z_abs, 0)

        return np.sqrt(x_max ** 2 + y_max ** 2 + z_max ** 2) + np.minimum(
            np.maximum(x_abs, np.maximum(y_abs, z_abs)), 0)

