from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Points.PointClouds import *
from MetaStruct.Objects.Lattices.StrutLattice import *


def convex_test():
    ds = DesignSpace(150, create_grids=True)
    shape = Sphere(ds)

    points = PointsOnSphere(n_points=50, sphere=shape)

    #points.preview_points()

    lat = ConvexHullLattice(ds, points, r=0.05)

    lat.preview_model()


if __name__ == "__main__":
    convex_test()