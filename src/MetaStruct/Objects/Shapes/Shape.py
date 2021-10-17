from MetaStruct.Objects.Booleans.Boolean import Intersection, Union, Difference, Multiply
from MetaStruct.Objects.Geometry import Geometry


class Shape(Geometry):

    morph = 'Shape'

    def __init__(self, design_space, x=0, y=0, z=0):

        self.design_space = design_space

        super().__init__(self.design_space)

        self.name = self.__class__.__name__

        self.x = x
        self.y = y
        self.z = z

        self.XX = self.design_space.x_grid
        self.YY = self.design_space.y_grid
        self.ZZ = self.design_space.z_grid

        self.x_limits = self.y_limits = self.z_limits = None

        self.evaluated_grid = self.evaluated_distance = None

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
