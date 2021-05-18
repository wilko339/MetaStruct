from Objects.DesignSpace import DesignSpace
from Objects.Shapes.Cuboid import Cuboid
from Objects.Lattices.Gyroid import Gyroid
import math
from Objects.Shapes.Sphere import Sphere
import numpy as np


def latticeRefinementExample():

    ds = DesignSpace(resolution=300)

    cuboid = Cuboid(ds, xd=2, yd=2, zd=0.5)

    refinedLattice = Gyroid(ds, 1, ny=math.pi/3, nz=2, vf=0.4)

    refinedLattice.convertToCylindrical()

    sphere = Sphere(ds, r=1.5)

    sphere.evaluate_grid()

    sphere.evaluated_grid = np.where(
        sphere.evaluated_grid > 0, 0, sphere.evaluated_grid)

    refinedLattice.evaluated_grid -= sphere.evaluated_grid / 10

    shape = cuboid / refinedLattice

    shape.previewModel()
