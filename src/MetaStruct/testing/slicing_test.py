from MetaStruct.Objects.slice_parameters import SliceParameters
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from skimage.measure import find_contours
import matplotlib.pyplot as plt


def main():
    sp = SliceParameters()
    shape = Cube(sp) / Gyroid(sp)

    shape.preview_model()

    return

    shape.evaluate_grid()

    for z in range(shape.design_space.resolution[2]):
        image = find_contours(shape.evaluated_grid[:, :, z], 0)
        image1 = find_contours(shape.evaluated_grid[:, :, z], -0.1)

        fig, ax = plt.subplots()
        #ax.imshow(shape.evaluated_grid[:, :, z])

        for contour in image:
            ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

        plt.show()


if __name__ == "__main__":
    main()
