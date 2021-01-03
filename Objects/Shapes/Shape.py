from Objects.Booleans.Boolean import Intersection, Union, Difference, Multiply
from Objects.Geometry import Geometry


class Shape(Geometry):

    morph = 'Shape'

    def __init__(self, designSpace, x=0, y=0, z=0):

        self.designSpace = designSpace

        super().__init__(self.designSpace)

        self.name = self.__class__.__name__

        self.x = self.paramCheck(x)
        self.y = self.paramCheck(y)
        self.z = self.paramCheck(z)

        self.transform = None

        self.XX = self.designSpace.XX
        self.YY = self.designSpace.YY
        self.ZZ = self.designSpace.ZZ

    def setLims(self):

        self.xLims = self.yLims = self.zLims = [0, 0]

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z})'

    def __str__(self):

        return f'{self.name} {self.morph}\nCentre(x, y, z): ({self.x}, {self.y}, {self.z})'

    def __add__(self, other):

        return Union(self, other)

    def __sub__(self, other):

        return Difference(self, other)

    def __truediv__(self, other):

        return Intersection(self, other)

    def __mul__(self, other):

        return Multiply(self, other)

    def paramCheck(self, n):

        try:

            float(n)
            return n

        except ValueError:
            print(f'{n} != a number.')
            raise

    def evaluatePoint(self, x, y, z):
        pass
