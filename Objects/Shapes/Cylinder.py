from Objects.Shapes.Shape import Shape

import numexpr as ne
import numpy as np


class Cylinder(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, r1=1, r2=1, l=1, ax='z'):
        super().__init__(designSpace, x, y, z)

        self.r1 = self.paramCheck(r1)
        self.r2 = self.paramCheck(r2)
        self.l = self.paramCheck(l)
        self.ax = ax

        if self.ax == 'z':

            self.xLims = np.array(
                [self.x - self.r1, self.x + self.r1])
            self.yLims = np.array(
                [self.y - self.r2, self.y + self.r2])
            self.zLims = np.array(
                [self.z - self.l, self.z + self.l])

        if self.ax == 'x':

            self.xLims = np.array(
                [self.x - self.l, self.x + self.l])
            self.yLims = np.array(
                [self.y - self.r1, self.y + self.r1])
            self.zLims = np.array(
                [self.z - self.r2, self.z + self.r2])

        if self.ax == 'y':

            self.xLims = np.array(
                [self.x - self.r1, self.x + self.r1])
            self.yLims = np.array(
                [self.y - self.l, self.y + self.l])
            self.zLims = np.array(
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

    def evaluatePoint(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z
        r1 = self.r1
        r2 = self.r2
        l = self.l

        if self.ax == 'z':

            array1 = ne.evaluate('(x-x0)**2/r1**2 + (y-y0)**2/r2**2 - 1')
            array2 = ne.evaluate('(z-z0)**2 - l**2')

            return ne.evaluate('where(array1 > array2, array1, array2)')

        if self.ax == 'x':

            array1 = ne.evaluate('(y-y0)**2/r1**2 + (z-z0)**2/r2**2 - 1')
            array2 = ne.evaluate('(x-x0)**2 - l**2')

            return ne.evaluate('where(array1 > array2, array1, array2)')

        if self.ax == 'y':

            array1 = ne.evaluate('(x-x0)**2/r1**2 + (z-z0)**2/r2**2 - 1')
            array2 = ne.evaluate('(y-y0)**2 - l**2')

            return ne.evaluate('where(array1 > array2, array1, array2)')
