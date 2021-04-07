import numexpr as ne
import numpy as np

from Objects.Geometry import Geometry


class Boolean(Geometry):

    def __init__(self, shape1, shape2):

        if shape1.designSpace is not shape2.designSpace:
            raise ValueError('Mismatching Design Spaces')

        self.designSpace = shape1.designSpace

        self.XX = self.designSpace.XX
        self.YY = self.designSpace.YY
        self.ZZ = self.designSpace.ZZ

        self.xStep = self.designSpace.xStep
        self.yStep = self.designSpace.yStep
        self.zStep = self.designSpace.zStep

        if shape1.morph == 'Lattice' and shape2.morph != 'Lattice':
            raise TypeError('Please enter Lattice Object as 2nd Argument.')

        self.morph = 'Shape'

        self.transform = np.eye(3)

        self.shape1 = shape1
        self.shape2 = shape2
        self.shapes = [shape1, shape2]

        self.shapesXmins = []
        self.shapesXmaxs = []
        self.shapesYmins = []
        self.shapesYmaxs = []
        self.shapesZmins = []
        self.shapesZmaxs = []

        self.setLims()

        self.x = (shape1.x + shape2.x) / 2
        self.y = (shape1.z + shape2.y) / 2
        self.z = (shape1.x + shape2.z) / 2

        self.name = shape1.name + '_' + shape2.name

        self.expression = None
        ne.set_num_threads(ne.ncores)

    def setLims(self):

        self.xLims = [0., 0.]
        self.yLims = [0., 0.]
        self.zLims = [0., 0.]

        if self.shape2.morph != 'Lattice':

            for shape in self.shapes:
                self.shapesXmins.append(shape.xLims[0])
                self.shapesXmaxs.append(shape.xLims[1])
                self.shapesYmins.append(shape.yLims[0])
                self.shapesYmaxs.append(shape.yLims[1])
                self.shapesZmins.append(shape.zLims[0])
                self.shapesZmaxs.append(shape.zLims[1])

            self.xLims = [min(self.shapesXmins), max(self.shapesXmaxs)]
            self.yLims = [min(self.shapesYmins), max(self.shapesYmaxs)]
            self.zLims = [min(self.shapesZmins), max(self.shapesZmaxs)]

        if self.shape2.morph == 'Lattice':
            self.morph == 'Lattice'

            self.xLims = self.shape1.xLims
            self.yLims = self.shape1.yLims
            self.zLims = self.shape1.zLims

    def __repr__(self):

        return f'{self.__class__.__name__}({repr(self.shape1)}, {repr(self.shape2)})'

    def __add__(self, other):

        return Union(self, other)

    def __sub__(self, other):

        return Difference(self, other)

    def __truediv__(self, other):

        return Intersection(self, other)

    def checkShapeGrids(self):

        for shape in self.shapes:

            if not hasattr(shape, 'evaluatedGrid'):
                shape.evaluateGrid()

    def translate(self, x, y, z):

        for shape in self.shapes:
            shape.translate(x, y, z)

        self.setLims()

    def evaluateGrid(self):

        for shape in self.shapes:

            if not hasattr(shape, 'evaluatedGrid'):
                shape.evaluateGrid()

        g1 = self.shape1.evaluatedGrid
        g2 = self.shape2.evaluatedGrid

        if hasattr(self, 'blend'):

            b = self.blend

        self.evaluatedGrid = ne.evaluate(self.expression)
        self.evaluatedList = self.evaluatedGrid.flatten()

    def evaluatePoint(self, x, y, z):

        g1 = self.shape1.evaluatePoint(x, y, z)
        g2 = self.shape2.evaluatePoint(x, y, z)

        return ne.evaluate(self.expression)


class Union(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)
        self.expression = 'where(g1<g2, g1, g2)'


class Difference(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)
        self.expression = 'where(g1>-g2, g1, -g2)'


class Intersection(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)
        self.expression = 'where(g1>g2, g1, g2)'


class Add(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)
        self.expression = 'g1 + g2'


class Blend(Boolean):

    def __init__(self, shape1, shape2, blend=0.5):
        super().__init__(shape1, shape2)
        self.blend = blend
        self.expression = 'b * g1 + (1 - b) * g2'


class Divide(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)
        self.expression = 'g1 / g2'


class Multiply(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)
        self.expression = 'g1 * g2'


class SmoothUnion(Boolean):

    def __init__(self, shape1, shape2, blend=4):
        super().__init__(shape1, shape2)
        self.blend = blend
        self.expression = '-log(where((exp(-b*g1) + exp(-b*g2))>0.000, exp(-b*g1) + exp(-b*g2), 0.000))/b'


class Subtract(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)
        self.expression = 'g1 - g2'
