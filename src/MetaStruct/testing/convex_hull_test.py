from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Points.PointClouds import *
from MetaStruct.Objects.Lattices.StrutLattice import *


def convex_test():
    ds = DesignSpace(150)
    shape = Sphere(ds)

    points = RandomPoints(50, shape, seed=1)

    lat = ConvexHullLattice(ds, points, r=0.05)

    lat.preview_model()


if __name__ == "__main__":
    convex_test()