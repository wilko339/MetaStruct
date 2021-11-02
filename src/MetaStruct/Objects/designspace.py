import numpy as np


class DesignSpace:
    DATA_TYPE = np.float32
    OFFSET = 0.1

    def __init__(self,
                 resolution=None,
                 x_resolution=0,
                 y_resolution=0,
                 z_resolution=0,
                 x_bounds=None,
                 y_bounds=None,
                 z_bounds=None,
                 create_grid=False):
        if resolution is None:
            resolution = 200
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

        self.x_resolution = x_resolution
        self.y_resolution = y_resolution
        self.z_resolution = z_resolution

        self.x_lower = min(self.x_bounds)
        self.x_upper = max(self.x_bounds)
        self.y_lower = min(self.y_bounds)
        self.y_upper = max(self.y_bounds)
        self.z_lower = min(self.z_bounds)
        self.z_upper = max(self.z_bounds)

        self.create_grids = create_grid

        if self.x_resolution == 0:

            self.X, self.x_step = np.linspace(self.x_lower - self.OFFSET,
                                              self.x_upper + self.OFFSET,
                                              resolution,
                                              retstep=True,
                                              dtype=DesignSpace.DATA_TYPE)
            self.Y, self.y_step = np.linspace(self.y_lower - self.OFFSET,
                                              self.y_upper + self.OFFSET,
                                              resolution,
                                              retstep=True,
                                              dtype=DesignSpace.DATA_TYPE)
            self.Z, self.z_step = np.linspace(self.z_lower - self.OFFSET,
                                              self.z_upper + self.OFFSET,
                                              resolution,
                                              retstep=True,
                                              dtype=DesignSpace.DATA_TYPE)

        else:

            self.X, self.x_step = np.linspace(self.x_lower - self.OFFSET,
                                              self.x_upper + self.OFFSET,
                                              x_resolution,
                                              retstep=True,
                                              dtype=DesignSpace.DATA_TYPE)
            self.Y, self.y_step = np.linspace(self.y_lower - self.OFFSET,
                                              self.y_upper + self.OFFSET,
                                              y_resolution,
                                              retstep=True,
                                              dtype=DesignSpace.DATA_TYPE)
            self.Z, self.z_step = np.linspace(self.z_lower - self.OFFSET,
                                              self.z_upper + self.OFFSET,
                                              z_resolution,
                                              retstep=True,
                                              dtype=DesignSpace.DATA_TYPE)

        print('Generating Sample Grid in Design Space')

        if self.create_grids is True:

            self.x_grid, self.y_grid, self.z_grid = np.meshgrid(self.X,
                                                                self.Y,
                                                                self.Z,
                                                                indexing='ij', copy=True)

            if self.x_resolution == 0:
                self.coordinate_list = np.empty(
                    (self.resolution * self.resolution * self.resolution, 3), dtype=np.float32)

            else:
                self.coordinate_list = np.empty(
                    (self.x_resolution * self.y_resolution * self.z_resolution, 3), dtype=np.float32)
            self.coordinate_list[:, 0] = self.x_grid.flatten()
            self.coordinate_list[:, 1] = self.y_grid.flatten()
            self.coordinate_list[:, 2] = self.z_grid.flatten()

        else:
            self.x_grid = None
            self.y_grid = None
            self.z_grid = None
