from Objects.DesignSpace import DesignSpace
from Objects.Points.PointClouds import LHSPoints, RandomPoints
from Objects.Lattices.StrutLattice import VoronoiLattice, DelaunayLattice
from Objects.Shapes.Cube import Cube
from Objects.Shapes.Sphere import Sphere
from Objects.Shapes.HollowSphere import HollowSphere
import numpy as np


def main():

    ds = DesignSpace(res=200)

    region = Cube(ds)

    points = LHSPoints(20, region)

    # print(points.points)
    #
    # corners = np.array([
    #     [-1, -1, -1],
    #     [-1, -1, 1],
    #     [-1, 1, 1],
    #     [-1, 1, -1],
    #     [1, 1, -1],
    #     [1, 1, 1],
    #     [1, -1, 1],
    #     [1, -1, -1]
    # ])
    #
    # for corner in corners:
    #
    #     points.points = np.append(points.points, np.array([corner]), axis=0)

    latt = VoronoiLattice(ds, points)

    latt.previewModel()

if __name__ == '__main__':
    main()

