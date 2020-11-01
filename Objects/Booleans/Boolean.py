import numpy as np
from Objects.Geometry import Geometry


class Boolean(Geometry):

    def __init__(self, shape1, shape2):

        if shape1.designSpace.XX is not shape2.designSpace.XX:
            if shape1.designSpace.YY is not shape2.designSpace.YY:
                if shape1.designSpace.ZZ is not shape2.designSpace.ZZ:
                    raise ValueError(
                        f'{shape1.name} and {shape2.name} are defined in different design spaces.')

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
        self.setLims()

        self.x = (shape1.x + shape2.x) / 2
        self.y = (shape1.z + shape2.y) / 2
        self.z = (shape1.x + shape2.z) / 2

        self.name = shape1.name + '_' + shape2.name

    def setLims(self):

        self.xLims = [0., 0.]
        self.yLims = [0., 0.]
        self.zLims = [0., 0.]

        self.shapesXmins = []
        self.shapesXmaxs = []
        self.shapesYmins = []
        self.shapesYmaxs = []
        self.shapesZmins = []
        self.shapesZmaxs = []

        if self.shape2.morph != 'Lattice':

            for shape in self.shapes:

                self.shapesXmins.append(shape.xLims[0])
                self.shapesXmaxs.append(shape.xLims[1])
                self.shapesYmins.append(shape.yLims[0])
                self.shapesYmaxs.append(shape.yLims[1])
                self.shapesZmins.append(shape.zLims[0])
                self.shapesZmaxs.append(shape.zLims[1])

            self.xLims[0] = min(self.shapesXmins)
            self.xLims[1] = max(self.shapesXmaxs)
            self.yLims[0] = min(self.shapesYmins)
            self.yLims[1] = max(self.shapesYmaxs)
            self.zLims[0] = min(self.shapesZmins)
            self.zLims[1] = max(self.shapesZmaxs)

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
