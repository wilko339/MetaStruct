from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Torus import Torus

from line_profiler_pycharm import profile


@profile
def main():
    ds = DesignSpace(resolution=500, create_grid=False)
    torus = Torus(ds, r1=0.5, r2=0.25)

    torus.evaluate_grid()

    #cube.preview_model()


# Original (300): 538339
# Numpy (300) : 77579

# Original (500): 2499305
# Numpy (500): 336159

if __name__ == '__main__':
    main()