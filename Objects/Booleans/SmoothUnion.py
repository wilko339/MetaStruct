from Objects.Booleans.Boolean import Boolean

import numexpr as ne
import numpy as np


class SmoothUnion(Boolean):

    def __init__(self, shape1, shape2, blend=4):
        super().__init__(shape1, shape2)

        self.blend = blend

    def evaluatePoint(self, x, y, z):

        res = np.exp(-self.blend * self.shape1.evaluatePoint(x, y, z)) + \
            np.exp(-self.blend * self.shape2.evaluatePoint(x, y, z))

        return -np.log(np.maximum(0.0001, res)) / self.blend

    def evaluateGrid(self):

        for shape in self.shapes:

            if not hasattr(shape, 'evaluatedGrid'):

                shape.evaluateGrid()

        res = np.exp(-self.blend * self.shape1.evaluatedGrid) + \
            np.exp(-self.blend * self.shape2.evaluatedGrid)

        self.evaluatedGrid = -np.log(np.maximum(0.0001, res)) / self.blend
