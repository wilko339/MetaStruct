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
            layer_t = 0.05

        z_resolution = (z_bounds[1] - z_bounds[0]) / layer_t

        if type(z_resolution) is not int:
            print("Warning: Object not divisible into integer number of layers with current layer thickness /"
                  ", modifying z height.")

            z_resolution = math.ceil(z_resolution)
            z_bounds[1] = z_bounds[0] + layer_t * z_resolution

        print(z_resolution)

        resolution = xy_resolution.append(z_resolution)

        print(resolution)

        super().__init__(xy_resolution, x_bounds, y_bounds, z_bounds)

