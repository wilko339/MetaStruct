import copy

from MetaStruct.Objects.Shapes.Shape import Shape


class Pattern(Shape):

    def __init__(self, shape, nx=3, ny=2, nz=2, xd=0.5, yd=0.5, zd=0.5):

        self.x = shape.x
        self.y = shape.y
        self.z = shape.z

        super().__init__(self.x, self.y, self.z)

        self.nx = nx
        self.ny = ny
        self.nz = nz

        self.xd = xd
        self.yd = yd
        self.zd = zd

        self.sourceShape = shape

        self.shape = shape

        self.set_limits(self.sourceShape)

        self.createPattern()

    def createPattern(self):

        for it in range(self.nx):

            it += 1

            new_shape = copy.deepcopy(self.sourceShape)

            new_shape.translate(it*self.xd, 0, 0)

            self.shape += new_shape

        self.set_limits(self.shape)

        for it in range(self.ny):

            it += 1

            new_shape = copy.deepcopy(self.sourceShape)

            new_shape.translate(0, it*self.yd, 0)

            self.shape += new_shape

        self.set_limits(self.shape)

        for it in range(self.nz):

            it += 1

            new_shape = copy.deepcopy(self.sourceShape)

            new_shape.translate(0, 0, it*self.zd)

            self.shape += new_shape

        self.set_limits(self.shape)

    def set_limits(self, obj):

        self.xLims = obj.x_limits
        self.yLims = obj.y_limits
        self.zLims = obj.z_limits

    def evaluate_point(self, x, y, z):

        return self.shape.evaluate_point(x, y, z)

    def translate(self, x, y, z):

        self.sourceShape.translate(x, y, z)

        self.set_limits(self.sourceShape)

        self.__init__(self.sourceShape, self.nx, self.ny,
                      self.nz, self.xd, self.yd, self.zd)
