import numexpr as ne
import numpy as np

from MetaStruct.Objects.Geometry import Geometry


class Noise(Geometry):

    def __init__(self, design_space, shape, intensity=1.5):
        super().__init__(design_space)

        self.shape = shape
        self.designSpace = design_space
        self.intensity = 10000/intensity

        self.xLims = self.shape.x_limits
        self.yLims = self.shape.y_limits
        self.zLims = self.shape.z_limits

    def evaluate_grid(self):

        grid = np.random.randint(
            100, size=self.designSpace.x_grid.shape)
        intensity = self.intensity

        self.noiseGrid = ne.evaluate('grid / intensity')

        if not hasattr(self.shape, 'evaluated_grid'):

            self.shape.evaluate_grid()

        shapeGrid = self.shape.evaluated_grid
        noiseGrid = self.noiseGrid

        self.evaluatedGrid = ne.evaluate('shapeGrid + noiseGrid')
