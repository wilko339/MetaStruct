from Objects.DesignSpace import DesignSpace
from Objects.Shapes.Cuboid import Cuboid
from Objects.Lattices.Gyroid import Gyroid
import math
from Objects.Shapes.Sphere import Sphere
import numpy as np


def latticeRefinementExample():

    ds = DesignSpace(res=300)

    cuboid = Cuboid(ds, xd=2, yd=2, zd=0.5)

    refinedLattice = Gyroid(ds, 1, ny=math.pi/3, nz=2, vf=0.4)

    refinedLattice.convertToCylindrical()

    sphere = Sphere(ds, r=1.5)

    sphere.evaluateGrid()

    sphere.evaluatedGrid = np.where(
        sphere.evaluatedGrid > 0, 0, sphere.evaluatedGrid)

    refinedLattice.evaluatedGrid -= sphere.evaluatedGrid / 10

    shape = cuboid / refinedLattice

    shape.previewModel()
