from Objects.Geometry import Geometry

import numpy as np
import numexpr as ne


class Noise(Geometry):

    def __init__(self, designSpace, shape, intensity=1.5):
        super().__init__(designSpace)

        self.shape = shape
        self.designSpace = designSpace
        self.intensity = 10000/intensity

        self.xLims = self.shape.xLims
        self.yLims = self.shape.yLims
        self.zLims = self.shape.zLims

    def evaluateGrid(self):

        grid = np.random.randint(
            100, size=self.designSpace.XX.shape)
        intensity = self.intensity

        self.noiseGrid = ne.evaluate('grid / intensity')

        if not hasattr(self.shape, 'evaluatedGrid'):

            self.shape.evaluateGrid()

        shapeGrid = self.shape.evaluatedGrid
        noiseGrid = self.noiseGrid

        self.evaluatedGrid = ne.evaluate('shapeGrid + noiseGrid')
