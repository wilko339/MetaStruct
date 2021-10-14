import numexpr as ne
import numpy as np

from MetaStruct.Objects.Shapes.Shape import Shape


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

        x0 = self.x
        y0 = self.y
        z0 = self.z
        r1 = self.r1
        r2 = self.r2
        l = self.l

        circles = {'z': '(x-x0)**2/r1**2 + (y-y0)**2/r2**2 - 1',
                   'x': '(y-y0)**2/r1**2 + (z-z0)**2/r2**2 - 1',
                   'y': '(x-x0)**2/r1**2 + (z-z0)**2/r2**2 - 1'}

        lengths = {'z': '(z-z0)**2 - l**2',
                   'x': '(x-x0)**2 - l**2',
                   'y': '(y-y0)**2 - l**2'}

        array1 = ne.evaluate(circles[self.ax])
        array2 = ne.evaluate(lengths[self.ax])

        return ne.evaluate('where(array1 > array2, array1, array2)')
