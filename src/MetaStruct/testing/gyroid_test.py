from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Lattices.Gyroid import Gyroid

from line_profiler_pycharm import profile


@profile
def main():
    ds = DesignSpace(resolution=900, create_grid=False)
    cube = Cube(ds) / Gyroid(ds)

    cube.evaluate_grid()

    #cube.preview_model()


# Original (res = 300): 3665003
# Numpy (res = 300): 539539
# Numpy (res = 900): 20427916

# Original fails at res~500 due to running out of memory (2015 macbook pro with 16GB ram)
# Numpy version evaluates up to res~900 on same machine, but runs out of memory when previewing (:

if __name__ == '__main__':
    main()