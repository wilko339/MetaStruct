from Objects.DesignSpace import DesignSpace
from Objects.Lattices.Diamond import Diamond
from Objects.Lattices.Primitive import Primitive
from Objects.Shapes.Cuboid import Cuboid
from Objects.Shapes.Sphere import Sphere
from Objects.Shapes.HollowSphere import HollowSphere
from Functions.ModifierArray import createModifierArray
import numpy as np


def main():

    ds = DesignSpace(res=400)

    region = Cuboid(ds, xd=0.5, yd=1, zd=0.5)

    lattice = Primitive(ds, nx=3, nz=3, vf=0.3)

    lattice.ny = createModifierArray(lattice, 1.5, 3, 'y')

    region /= lattice

    region.saveMesh('graded_primitive')


if __name__ == '__main__':
    main()
