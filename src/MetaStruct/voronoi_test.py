from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Points.PointClouds import *
from MetaStruct.Objects.Lattices.StrutLattice import *

import cProfile
import io
import pstats

def profile(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
        ps.print_stats()
        print(s.getvalue())
        return retval
    return wrapper

@profile
def voro_test():
    ds = DesignSpace(100)
    shape = Cube(ds)

    points = RandomPoints(5, shape, seed=1)

    lat = VoronoiLattice(ds, points, r=0.05)

    lat.preview_model()


if __name__ == "__main__":
    voro_test()