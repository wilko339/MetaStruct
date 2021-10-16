import numpy as np

from MetaStruct.Objects.Shapes.Shape import Shape
from MetaStruct.Objects.Shapes.Sphere import Sphere


class HollowSphere(Shape):

    def __init__(self, design_space, x=0, y=0, z=0, r=1, t=0.3):

        self.designSpace = design_space

        super().__init__(self.designSpace, x, y, z)

        self.r = r
        self.t = t
        self.set_limits()

    def set_limits(self):

        self.x_limits = np.array(
            [self.x - self.r, self.x + self.r])
        self.y_limits = np.array(
            [self.y - self.r, self.y + self.r])
        self.z_limits = np.array(
            [self.z - self.r, self.z + self.r])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.r}, {self.t})'

    def __str__(self):

        return super().__str__() + f'\nRadius: {self.r}\nWall Thickness: {self.t}'

    def evaluate_point(self, x, y, z):

        ball = Sphere(self.designSpace, self.x, self.y, self.z, self.r) - \
            Sphere(self.designSpace, self.x, self.y, self.z, self.r -
                   self.t)

        return ball.evaluate_point(x, y, z)
