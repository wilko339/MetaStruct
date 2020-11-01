from Objects.Booleans.Boolean import Boolean

import numexpr as ne


class Blend(Boolean):

    def __init__(self, shape1, shape2, blend=0.5):

        super().__init__(shape1, shape2)

        self.blend = blend

    def evaluatePoint(self, x, y, z):

        return self.blend * self.shape1.evaluatePoint(x, y, z) + \
            (1 - self.blend) * self.shape2.evaluatePoint(x, y, z)

    def evaluateGrid(self):

        self.checkShapeGrids()

        g1 = self.shape1.evaluatedGrid
        g2 = self.shape2.evaluatedGrid
        b = self.blend

        expr = 'b * g1 + (1 - b) * g2'

        self.evaluatedGrid = ne.evaluate(expr)
