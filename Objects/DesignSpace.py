import numpy as np
import numexpr as ne


class DesignSpace:
    DATA_TYPE = np.dtype('f8')

    def __init__(self, res=200, xRes=0, yRes=0, zRes=0, xBounds=[-1.1, 1.1], yBounds=[-1.1, 1.1], zBounds=[-1.1, 1.1]):

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

        self.n_threads = ne.ncores

        print(self.n_threads)

        offset = 1e-6

        if self.xRes == 0:

            self.X, self.xStep = np.linspace(
                self.xLower - offset, self.xUpper + offset, res, retstep=True, dtype=DesignSpace.DATA_TYPE)
            self.Y, self.yStep = np.linspace(
                self.yLower - offset, self.yUpper + offset, res, retstep=True, dtype=DesignSpace.DATA_TYPE)
            self.Z, self.zStep = np.linspace(
                self.zLower - offset, self.zUpper + offset, res, retstep=True, dtype=DesignSpace.DATA_TYPE)

        else:

            self.X, self.xStep = np.linspace(
                self.xLower - offset, self.xUpper + offset, xRes, retstep=True, dtype=DesignSpace.DATA_TYPE)
            self.Y, self.yStep = np.linspace(
                self.yLower - offset, self.yUpper + offset, yRes, retstep=True, dtype=DesignSpace.DATA_TYPE)
            self.Z, self.zStep = np.linspace(
                self.zLower - offset, self.zUpper + offset, zRes, retstep=True, dtype=DesignSpace.DATA_TYPE)

        print('Generating Sample Grid in Design Space')

        self.XX, self.YY, self.ZZ = np.meshgrid(
            self.X, self.Y, self.Z, indexing='ij')
