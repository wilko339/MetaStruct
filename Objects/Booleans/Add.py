from Objects.Booleans.Boolean import Boolean

import numexpr as ne


class Add(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        outputs = [self.shape1.evaluatedGrid, self.shape2.evaluatedGrid]

        return sum(outputs)

    def evaluateGrid(self):

        self.checkShapeGrids()

        g1 = self.shape1.evaluatedGrid
        g2 = self.shape2.evaluatedGrid

        expr = 'g1 + g2'

        self.evaluatedGrid = ne.evaluate(expr)
