from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Points.PointClouds import *
from MetaStruct.Objects.Lattices.StrutLattice import *

def profile(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return wrapper

@profile
def voro_test():
    ds = DesignSpace(100)
    shape = Sphere(ds)

    points = RandomPoints(20, shape, seed=1)

    lat = VoronoiLattice(ds, points, r=0.03)

    #lat.preview_model()


if __name__ == "__main__":
    voro_test()