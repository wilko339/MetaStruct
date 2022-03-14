import matplotlib.patches

from MetaStruct.Objects.slice_parameters import SliceParameters
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.Lattices.GyroidSurface import GyroidSurface
from skimage.measure import find_contours
import skfmm
import matplotlib.pyplot as plt
import numpy as np
import math


def hatch(sp, period=0.5, layer_t=None, phi=math.pi/4):

    if layer_t is None:
        layer_t = sp.layer_t

    x = sp.X
    y = sp.Y
    z = sp.Z

    out = x*np.cos(phi) + y*np.sin(phi)*(np.power(-1, np.mod(z/layer_t, 2)))

    return -np.abs(out)


def main():
    sp = SliceParameters(xy_resolution=200, layer_t=0.1)

    shape = Cube(sp) / Gyroid(sp)

    infill = GyroidSurface(sp, lx=0.1, ly=0.1, lz=0.2)

    shape.evaluate_grid()
    infill.evaluate_grid()

    for z in range(shape.design_space.resolution[2]):

        try:

            # hatching_ = skfmm.distance(infill.evaluated_grid[:, :, z], [sp.x_step, sp.y_step])
            # hatching_ = skfmm.distance(hatch(sp)[:, :, z], [sp.x_step, sp.y_step])

            distances = skfmm.distance(shape.evaluated_grid[:, :, z], [sp.x_step, sp.y_step])

            hatching_ = hatch(sp)[:, :, z]

            hatching = np.maximum(hatching_, shape.evaluated_grid[:, :, z])

            outer = find_contours(distances, 0)
            outer_1 = find_contours(distances, -0.02)

            levels = np.linspace(0, 0.5, 5)

            fig, ax = plt.subplots()

            for contour in outer:
                ax.plot(contour[:, 1], contour[:, 0], linewidth=1, color='b')

            for contour in outer_1:
                ax.plot(contour[:, 1], contour[:, 0], linewidth=1, color='r')

            for level in levels:
                hatching_ = find_contours(hatching, -level)
                for contour in hatching_:
                    #ax.plot(contour[:, 1], contour[:, 0], linewidth=1, color='g')

            plt.show()

        except ValueError:

            print('No 0 level set found.')



if __name__ == "__main__":
    main()
