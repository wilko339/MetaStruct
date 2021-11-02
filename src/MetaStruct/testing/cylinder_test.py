from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Cylinder import Cylinder

from line_profiler_pycharm import profile


@profile
def main():
    ds = DesignSpace(resolution=300, create_grid=False)
    cube = Cylinder(ds)

    cube.evaluate_grid()

    #cube.preview_model()


# Original (300): 569366
# Numpy (300) : 85616

# Original (500): 2621778
# Numpy (500): 370715

if __name__ == '__main__':
    main()