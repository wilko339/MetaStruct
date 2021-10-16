import numpy as np

from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Shapes.Shape import Shape


class HollowCube(Shape):

    def __init__(self, design_space, x=0, y=0, z=0, dim=1, t=0.3):
        super().__init__(design_space, x, y, z)

        self.dim = parameter_check(dim)
        self.t = parameter_check(t)
        self.set_limits()

    def set_limits(self):

        self.xLims = np.array(
            [self.x - self.dim, self.x + self.dim])
        self.yLims = np.array(
            [self.y - self.dim, self.y + self.dim])
        self.zLims = np.array(
            [self.z - self.dim, self.z + self.dim])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.dim}, {self.t})'

    def __str__(self):

        return super().__str__() + f'\nCube Radius: {self.dim}\nWall Thickness: {self.t}'

    def evaluate_point(self, x, y, z):

        box = Cube(self.design_space, self.x, self.y, self.z, self.dim) - \
              Cube(self.design_space, self.x, self.y, self.z, self.dim - self.t)

        return box.evaluate_point(x, y, z)
