import numpy as np
from skfmm import distance
from MetaStruct.Objects.Shapes.Shape import Shape


class SupportVolume(Shape):

    def __init__(self, shape, h=1):

        self.shape = shape
        self.h = h

        super().__init__(self.shape.design_space, self.shape.x, self.shape.y, self.shape.z)

        self.x_limits = self.shape.x_limits
        self.y_limits = self.shape.y_limits
        self.z_limits = np.array([-h, h])

    def evaluate_grid(self):

        self.evaluated_grid = self.shape.extrude_projection()