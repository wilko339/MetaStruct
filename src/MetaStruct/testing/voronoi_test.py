from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Shapes.Shape import Shape
from MetaStruct.Objects.Points.PointClouds import RandomPoints, LHSPoints
from MetaStruct.Objects.Lattices.StrutLattice import *
from MetaStruct.Objects.Booleans.Boolean import *


def voro_test():
    ds = DesignSpace(300)
    region = Sphere(ds)

    points = LHSPoints(ds, 50, shape=region)

    lat = DelaunayLattice(ds, point_cloud=points, r=0.03) / region
    lat += VoronoiLattice(ds, point_cloud=points, r=0.03) / region

    lat.preview_model()

if __name__ == "__main__":
    voro_test()