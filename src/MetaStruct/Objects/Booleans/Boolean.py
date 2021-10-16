import numexpr as ne
import numpy as np

from MetaStruct.Objects.Geometry import Geometry


class Boolean(Geometry):

    def __init__(self, shape1, shape2):

        if shape1.design_space is not shape2.design_space:
            raise ValueError('Mismatching Design Spaces')

        super().__init__(shape1.design_space)

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

        self.set_limits()

        self.x = (shape1.x + shape2.x) / 2
        self.y = (shape1.z + shape2.y) / 2
        self.z = (shape1.x + shape2.z) / 2

        self.name = shape1.name + '_' + shape2.name

        self.expression = None
        self.evaluated_grid = None
        self.blend = None

    def set_limits(self):

        self.x_limits = [0., 0.]
        self.y_limits = [0., 0.]
        self.z_limits = [0., 0.]

        if self.shape2.morph != 'Lattice':

            for shape in self.shapes:
                self.shapesXmins.append(shape.x_limits[0])
                self.shapesXmaxs.append(shape.x_limits[1])
                self.shapesYmins.append(shape.y_limits[0])
                self.shapesYmaxs.append(shape.y_limits[1])
                self.shapesZmins.append(shape.z_limits[0])
                self.shapesZmaxs.append(shape.z_limits[1])

            self.x_limits = [min(self.shapesXmins), max(self.shapesXmaxs)]
            self.y_limits = [min(self.shapesYmins), max(self.shapesYmaxs)]
            self.z_limits = [min(self.shapesZmins), max(self.shapesZmaxs)]

        if self.shape2.morph == 'Lattice':
            self.morph == 'Lattice'

            self.x_limits = self.shape1.x_limits
            self.y_limits = self.shape1.y_limits
            self.z_limits = self.shape1.z_limits

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

            if not hasattr(shape, 'evaluated_grid'):
                shape.evaluateGrid()

    def translate(self, x, y, z):

        for shape in self.shapes:
            shape.translate(x, y, z)

        self.set_limits()

    def evaluate_grid(self):

        for shape in self.shapes:

            if shape.evaluated_grid is None:
                shape.evaluate_grid()

        g1 = self.shape1.evaluated_grid
        g2 = self.shape2.evaluated_grid

        if self.blend is not None:

            b = self.blend

        self.evaluated_grid = ne.evaluate(self.expression)

    def evaluate_point(self, x, y, z):

        g1 = self.shape1.evaluate_point(x, y, z)
        g2 = self.shape2.evaluate_point(x, y, z)

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
