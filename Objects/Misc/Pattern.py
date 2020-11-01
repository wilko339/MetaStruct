from Objects.Shapes.Shape import Shape
import copy


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

        self.setLims(self.sourceShape)

        self.createPattern()

    def createPattern(self):

        for it in range(self.nx):

            it += 1

            new_shape = copy.deepcopy(self.sourceShape)

            new_shape.translate(it*self.xd, 0, 0)

            self.shape += new_shape

        self.setLims(self.shape)

        for it in range(self.ny):

            it += 1

            new_shape = copy.deepcopy(self.sourceShape)

            new_shape.translate(0, it*self.yd, 0)

            self.shape += new_shape

        self.setLims(self.shape)

        for it in range(self.nz):

            it += 1

            new_shape = copy.deepcopy(self.sourceShape)

            new_shape.translate(0, 0, it*self.zd)

            self.shape += new_shape

        self.setLims(self.shape)

    def setLims(self, obj):

        self.xLims = obj.xLims
        self.yLims = obj.yLims
        self.zLims = obj.zLims

    def evaluatePoint(self, x, y, z):

        return self.shape.evaluatePoint(x, y, z)

    def translate(self, x, y, z):

        self.sourceShape.translate(x, y, z)

        self.setLims(self.sourceShape)

        self.__init__(self.sourceShape, self.nx, self.ny,
                      self.nz, self.xd, self.yd, self.zd)
