from Objects.Booleans.Boolean import Boolean

import numexpr as ne


class Difference(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        for shape in self.shapes:

            if not hasattr(shape, 'evaluatedGrid'):

                shape.evaluateGrid()

        g1 = self.shape1.evaluatedGrid
        g2 = -self.shape2.evaluatedGrid

        expr = 'where(g1>g2, g1, g2)'

        return ne.evaluate(expr)
