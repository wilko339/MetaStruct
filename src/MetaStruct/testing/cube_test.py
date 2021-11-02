from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Shapes.Sphere import Sphere

from line_profiler_pycharm import profile


@profile
def main():
    ds = DesignSpace(resolution=500, create_grid=False)
    cube = Cube(ds) + Sphere(ds, x=0.5)

    cube.evaluate_grid()

    cube.preview_model()


# Original: 9074092
# Numpy :   947725

if __name__ == '__main__':
    main()