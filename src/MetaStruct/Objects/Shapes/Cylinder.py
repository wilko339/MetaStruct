import numexpr as ne
import numpy as np

from MetaStruct.Objects.Shapes.Shape import Shape


def broadcast_sdf(p1, p2, p3, a, b, c, r1, r2, l):

    circle = ((p1 - a) ** 2) / r1 ** 2 + ((p2 - b) ** 2) / r2 ** 2 - 1
    length = (p3 - c) ** 2 - l ** 2

    return np.maximum(circle, length)


class Cylinder(Shape):

    def __init__(self, design_space, x=0, y=0, z=0, r1=1, r2=1, l=1, ax='z'):
        super().__init__(design_space, x, y, z)

        self.r1 = r1
        self.r2 = r2
        self.l = l
        self.ax = ax

        if self.ax == 'z':
            self.x_limits = np.array(
                [self.x - self.r1, self.x + self.r1])
            self.y_limits = np.array(
                [self.y - self.r2, self.y + self.r2])
            self.z_limits = np.array(
                [self.z - self.l, self.z + self.l])

        if self.ax == 'x':
            self.x_limits = np.array(
                [self.x - self.l, self.x + self.l])
            self.y_limits = np.array(
                [self.y - self.r1, self.y + self.r1])
            self.z_limits = np.array(
                [self.z - self.r2, self.z + self.r2])

        if self.ax == 'y':
            self.x_limits = np.array(
                [self.x - self.r1, self.x + self.r1])
            self.y_limits = np.array(
                [self.y - self.l, self.y + self.l])
            self.z_limits = np.array(
                [self.z - self.r2, self.z + self.r2])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.r1}, {self.r2}, {self.l}, {self.ax})'

    def __str__(self):

        string = super().__str__() + \
            f'\nAxis: {self.ax}' + \
            f'\nLength: {self.l}'

        if self.ax == 'z':
            return string + f'\nRadii(x, y): ({self.r1}, {self.r2})'

        if self.ax == 'x':
            return string + f'\nRadii(y, z): ({self.r1}, {self.r2})'

        if self.ax == 'y':
            return string + f'\nRadii(x, z): ({self.r1}, {self.r2})'

    def evaluate_point(self, x, y, z):

        if self.ax == 'z':

            return broadcast_sdf(x, y, z, self.x, self.y, self.z, self.r1, self.r2, self.l)

        if self.ax == 'x':

            return broadcast_sdf(y, z, x, self.y, self.z, self.x, self.r1, self.r2, self.l)

        if self.ax == 'y':

            return broadcast_sdf(x, z, y, self.x, self.z, self.y, self.r1, self.r2, self.l)
