import numexpr as ne
import perlin3d

from MetaStruct.Objects.Geometry import Geometry


class PerlinNoise(Geometry):

    def __init__(self, design_space, shape, freq=(8, 8, 8)):
        super().__init__(design_space)

        self.morph = 'Shape'

        self.shape = shape
        self.designSpace = design_space

        self.xLims = self.shape.x_limits
        self.yLims = self.shape.y_limits
        self.zLims = self.shape.z_limits

        self.freq = freq

    def evaluate_grid(self):

        print('Generating Perlin Noise...')
        self.evaluatedGrid = perlin3d.generate_perlin_noise_3d(
            self.designSpace.x_grid.shape, self.freq)

    def noiseShape(self):

        if not hasattr(self, 'evaluated_grid'):

            self.evaluate_grid()

        if not hasattr(self.shape, 'evaluated_grid'):

            self.shape.evaluate_grid()

        g1 = self.shape.evaluated_grid
        g2 = self.evaluatedGrid

        expr = 'g1 + (g2 * 1.5)'

        self.evaluatedGrid = ne.evaluate(expr)

    def noiseLattice(self):

        if not hasattr(self, 'evaluated_grid'):

            self.evaluate_grid()

        g1 = self.evaluatedGrid
        g2 = -(self.evaluatedGrid + 0.1)

        expr = 'where(g1>g2, g1, g2)'

        self.evaluatedGrid = ne.evaluate(expr)
