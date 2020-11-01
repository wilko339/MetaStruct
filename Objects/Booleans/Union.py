import numexpr as ne
import numpy as np
from Objects.Booleans.Boolean import Boolean


class Union(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        return np.minimum(self.shape1.evaluatePoint(x, y, z), self.shape2.evaluatePoint(x, y, z))

    def evaluateGrid(self):

        if not hasattr(self.shape1, 'evaluatedGrid'):

            self.shape1.evaluateGrid()

        if not hasattr(self.shape2, 'evaluatedGrid'):

            self.shape2.evaluateGrid()

        s1 = self.shape1.evaluatedGrid
        s2 = self.shape2.evaluatedGrid

        self.evaluatedGrid = ne.evaluate('where(s1<s2, s1, s2)')
