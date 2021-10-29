from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Points.PointClouds import *
from MetaStruct.Objects.Lattices.StrutLattice import *


def voro_test():
    ds = DesignSpace(200)
    shape = Sphere(ds)

    points = RandomPoints(50, shape, seed=1)

    lat = VoronoiLattice(ds, points, r=0.05)

    lat.find_surface()

    lat.decimate_mesh(0.1)

    lat.preview_model()


if __name__ == "__main__":
    voro_test()