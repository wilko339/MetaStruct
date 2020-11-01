from Objects.Geometry import Geometry

import numexpr as ne
import perlin3d


class PerlinNoise(Geometry):

    def __init__(self, designSpace, shape, freq=(8, 8, 8)):
        super().__init__(designSpace)

        self.morph = 'Shape'

        self.shape = shape
        self.designSpace = designSpace

        self.xLims = self.shape.xLims
        self.yLims = self.shape.yLims
        self.zLims = self.shape.zLims

        self.freq = freq

    def evaluateGrid(self):

        print('Generating Perlin Noise...')
        self.evaluatedGrid = perlin3d.generate_perlin_noise_3d(
            self.designSpace.XX.shape, self.freq)

    def noiseShape(self):

        if not hasattr(self, 'evaluatedGrid'):

            self.evaluateGrid()

        if not hasattr(self.shape, 'evaluatedGrid'):

            self.shape.evaluateGrid()

        g1 = self.shape.evaluatedGrid
        g2 = self.evaluatedGrid

        expr = 'g1 + (g2 * 1.5)'

        self.evaluatedGrid = ne.evaluate(expr)

    def noiseLattice(self):

        if not hasattr(self, 'evaluatedGrid'):

            self.evaluateGrid()

        g1 = self.evaluatedGrid
        g2 = -(self.evaluatedGrid + 0.1)

        expr = 'where(g1>g2, g1, g2)'

        self.evaluatedGrid = ne.evaluate(expr)
