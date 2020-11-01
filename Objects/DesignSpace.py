import numpy as np


class DesignSpace:

    def __init__(self, res=100, xRes=0, yRes=0, zRes=0, xBounds=[-1, 1], yBounds=[-1, 1], zBounds=[-1, 1]):

        self.data_type = np.dtype('f4')

        self.xBounds = xBounds
        self.yBounds = yBounds
        self.zBounds = zBounds

        self.res = res

        self.xRes = xRes
        self.yRes = yRes
        self.zRes = zRes

        self.xLower = min(self.xBounds)
        self.xUpper = max(self.xBounds)
        self.yLower = min(self.yBounds)
        self.yUpper = max(self.yBounds)
        self.zLower = min(self.zBounds)
        self.zUpper = max(self.zBounds)

        offset = 1e-6

        if self.xRes == 0:

            X, self.xStep = np.linspace(
                self.xLower - offset, self.xUpper + offset, res, retstep=True, dtype=self.data_type)
            Y, self.yStep = np.linspace(
                self.yLower - offset, self.yUpper + offset, res, retstep=True, dtype=self.data_type)
            Z, self.zStep = np.linspace(
                self.zLower - offset, self.zUpper + offset, res, retstep=True, dtype=self.data_type)

        else:

            X, self.xStep = np.linspace(
                self.xLower - offset, self.xUpper + offset, xRes, retstep=True, dtype=self.data_type)
            Y, self.yStep = np.linspace(
                self.yLower - offset, self.yUpper + offset, yRes, retstep=True, dtype=self.data_type)
            Z, self.zStep = np.linspace(
                self.zLower - offset, self.zUpper + offset, zRes, retstep=True, dtype=self.data_type)

        print('Generating Sample Grid in Design Space')

        self.YY, self.ZZ, self.XX = np.meshgrid(X, Y, Z)
