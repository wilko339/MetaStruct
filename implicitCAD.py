from Objects.DesignSpace import DesignSpace
from Objects.Lattices.StrutLattice import ConvexHullLattice
from Objects.Points.PointClouds import LHSPoints
from Objects.Shapes.Cube import Cube


def main():

    ds = DesignSpace(res=100, xBounds=[-1.1, 1.1], yBounds=[-1.1, 1.1], zBounds=[-1.1, 1.1])

    cube = Cube(ds, round_r=1).previewModel()

    pc = LHSPoints(n_points=2000, shape=cube)

    lattice = ConvexHullLattice(ds, pc) + cube

    lattice.previewModel()

if __name__ == '__main__':
    main()
