from Objects.Booleans.Boolean import Boolean

import numpy as np
import numexpr as ne


class Intersection(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        return np.maximum(self.shape1.evaluatePoint(x, y, z), self.shape2.evaluatePoint(x, y, z))

    def evaluateGrid(self):
        for shape in self.shapes:

            if not hasattr(shape, 'evaluatedGrid'):

                shape.evaluateGrid()

        g1 = self.shape1.evaluatedGrid
        g2 = self.shape2.evaluatedGrid

        expr = 'where(g1>g2, g1, g2)'

        self.evaluatedGrid = ne.evaluate(expr)
        '''
        self.evaluatedGrid = np.maximum(
            self.shape1.evaluatedGrid, self.shape2.evaluatedGrid)
        '''
