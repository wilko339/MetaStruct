import numpy as np

from MetaStruct.Objects.Shapes.Cuboid import Cuboid


class Cube(Cuboid):

    def __init__(self, design_space, x=0, y=0, z=0, dim=1, round_r=0):
        super().__init__(design_space, x, y, z, xd=dim, yd=dim, zd=dim)

        self.dim = dim
        self.round_r = round_r
        ne.set_num_threads(ne.ncores)

    def __str__(self):
        return super().__str__() + f'\nCube Radius: {self.dim}'

    def evaluate_point(self, x, y, z):

        x_abs = np.abs(x) - self.dim
        y_abs = np.abs(y) - self.dim
        z_abs = np.abs(z) - self.dim

        x_max = np.maximum(x_abs, 0)
        y_max = np.maximum(y_abs, 0)
        z_max = np.maximum(z_abs, 0)

        return np.sqrt(x_max**2 + y_max**2 + z_max**2) + np.minimum(np.maximum(x_abs, np.maximum(y_abs, z_abs)), 0)
