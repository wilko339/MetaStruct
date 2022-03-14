import numpy as np
import math
from MetaStruct.Objects.designspace import DesignSpace


class SliceParameters(DesignSpace):
    DATA_TYPE = np.float32

    def __init__(self, x_bounds=None, y_bounds=None, z_bounds=None, layer_t=None, xy_resolution=None):
        if xy_resolution is None:
            xy_resolution = [100, 100]

        if type(xy_resolution) is int:
            xy_resolution = [xy_resolution, xy_resolution]

        assert len(xy_resolution) == 2

        if x_bounds is None:
            x_bounds = [-1.1, 1.1]

        if y_bounds is None:
            y_bounds = [-1.1, 1.1]

        if z_bounds is None:
            z_bounds = [-1.1, 1.1]

        if layer_t is None:
            layer_t = 0.1

        self.layer_t = layer_t

        self.z_resolution = (z_bounds[1] - z_bounds[0]) / layer_t

        print(self.z_resolution)

        if not self.z_resolution.is_integer():

            print("Warning: Object not divisible into integer number of layers with current layer thickness /"
                  ", modifying z height.")

            self.z_resolution = math.ceil(self.z_resolution)

            z_bounds[1] = z_bounds[0] + layer_t * self.z_resolution

        self.z_resolution = int(self.z_resolution)

        self.xy_resolution = xy_resolution

        print(z_bounds)

        resolution = [xy_resolution[0], xy_resolution[1], self.z_resolution+1]

        print(resolution)

        super().__init__(resolution, x_bounds, y_bounds, z_bounds)

