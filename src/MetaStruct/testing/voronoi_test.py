from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Shapes.Shape import Shape
from MetaStruct.Objects.Points.PointClouds import *
from MetaStruct.Objects.Lattices.StrutLattice import *
from MetaStruct.Objects.Booleans.Boolean import *

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
    ds = DesignSpace(100, create_grid=True)
    region = Sphere(ds)

    points = RandomPoints(40, region, seed=1)

    lat = VoronoiLattice(ds, points, r=0.03)

    #lat.preview_model()

if __name__ == "__main__":
    voro_test()