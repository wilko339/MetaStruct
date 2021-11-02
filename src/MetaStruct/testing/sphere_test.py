from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere

from line_profiler_pycharm import profile


@profile
def main():
    ds = DesignSpace(resolution=500, create_grid=False)
    sphere = Sphere(ds)

    sphere.evaluate_grid()

    #sphere.preview_model()


# True:             2185947
# False:            486961
# False (numexpr):  800699

if __name__ == '__main__':
    main()