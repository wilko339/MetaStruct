from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Cuboid import Cuboid

from line_profiler_pycharm import profile


@profile
def main():
    ds = DesignSpace(resolution=500, create_grid=False)
    cube = Cuboid(ds, xd=0.5, yd=0.5, zd=1)

    cube.evaluate_grid()

    #cube.preview_model()


# Original (300): 930872
# Numpy (300) : 257197

# Original (500): 5916069
# Numpy (500): 1242029

if __name__ == '__main__':
    main()