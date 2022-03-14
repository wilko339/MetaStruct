import numpy as np


class DesignSpace:
    DATA_TYPE = np.float32
    OFFSET = 0

    def __init__(self, resolution=None, x_bounds=None, y_bounds=None, z_bounds=None, create_grids=False):
        if resolution is None:
            resolution = [200, 200, 200]

        if type(resolution) is int:
            resolution = [resolution, resolution, resolution]

        assert len(resolution) == 3, 'Resolution list must be of length 3'

        if x_bounds is None:
            x_bounds = [-1.1, 1.1]

        if y_bounds is None:
            y_bounds = [-1.1, 1.1]

        if z_bounds is None:
            z_bounds = [-1.1, 1.1]

        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.z_bounds = z_bounds

        self.resolution = resolution

        self.x_lower = min(self.x_bounds)
        self.x_upper = max(self.x_bounds)
        self.y_lower = min(self.y_bounds)
        self.y_upper = max(self.y_bounds)
        self.z_lower = min(self.z_bounds)
        self.z_upper = max(self.z_bounds)

        self.create_grids = create_grids

        self.X, self.x_step = np.linspace(self.x_lower - self.OFFSET, self.x_upper + self.OFFSET, self.resolution[0],
                                          retstep=True, dtype=DesignSpace.DATA_TYPE)

        self.Y, self.y_step = np.linspace(self.y_lower - self.OFFSET, self.y_upper + self.OFFSET, self.resolution[1],
                                          retstep=True, dtype=DesignSpace.DATA_TYPE)

        self.Z, self.z_step = np.linspace(self.z_lower - self.OFFSET, self.z_upper + self.OFFSET, self.resolution[2],
                                          retstep=True, dtype=DesignSpace.DATA_TYPE)

        self.X = self.X[:, None, None]
        self.Y = self.Y[None, :, None]
        self.Z = self.Z[None, None, :]

        self.x_grid = None
        self.y_grid = None
        self.z_grid = None

        self.coordinate_list = None

    def generate_grids(self):

        self.x_grid, self.y_grid, self.z_grid = np.meshgrid(self.X, self.Y, self.Z, indexing='ij', copy=True)
        self.coordinate_list = np.empty(
            (self.resolution[0] * self.resolution[1] * self.resolution[2], 3), dtype=self.DATA_TYPE)

        self.coordinate_list[:, 0] = self.x_grid.flatten()
        self.coordinate_list[:, 1] = self.y_grid.flatten()
        self.coordinate_list[:, 2] = self.z_grid.flatten()
