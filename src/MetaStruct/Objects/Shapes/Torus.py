import numexpr as ne
import numpy as np

from MetaStruct.Objects.Shapes.Shape import Shape


class Torus(Shape):

    def __init__(self, design_space, x=0, y=0, z=0, r1=1, r2=0.5):
        super().__init__(design_space, x, y, z)

        self.x = x
        self.y = y
        self.z = z
        self.r1 = r1
        self.r2 = r2

        self.set_limits()

    def set_limits(self):

        self.x_limits = np.array(
            [self.x - self.r1 - self.r2, self.x + self.r1 + self.r2])
        self.y_limits = np.array(
            [self.y - self.r1 - self.r2, self.y + self.r1 + self.r2])
        self.z_limits = np.array(
            [self.z - self.r2, self.z + self.r2])

    def evaluate_point(self, x, y, z):

        return (np.sqrt((x-self.x)**2 + (y-self.y)**2) - self.r1)**2 + (z - self.z)**2 - self.r2**2