from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Shapes.Spheroid import Spheroid

from line_profiler_pycharm import profile


@profile
def main():
    ds = DesignSpace(resolution=500, create_grid=False)
    cube = Spheroid(ds)

    cube.evaluate_grid()

    #cube.preview_model()


# Original (500): 2395565
# Numpy (500):   343328

if __name__ == '__main__':
    main()