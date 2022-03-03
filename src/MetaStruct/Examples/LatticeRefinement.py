import math

import numpy as np

from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Cuboid import Cuboid
from MetaStruct.Functions.ModifierArray import create_modifier_array


def lattice_modification_example():

    # Initialise the design space. Use a reasonable resolution to capture all detail
    # while being fast enough
    ds = DesignSpace(resolution=300, x_bounds=[-2, 2], y_bounds=[-2, 2], z_bounds=[-1, 1])

    # Initialise the Cuboid and Lattice objects
    cuboid = Cuboid(ds, xd=2, yd=2, zd=1)
    lattice = Gyroid(ds, vf=0.4)

    # Create the fields to vary the lattice parameters
    volume_fraction = create_modifier_array(lattice, 0.3, 0.6)
    unit_cell_size = create_modifier_array(lattice, 0.5, 1)

    # Assign the new properties to the lattice
    lattice.vf = volume_fraction
    lattice.lx = unit_cell_size
    lattice.ly = unit_cell_size
    lattice.lz = unit_cell_size

    # Perform a boolean intersection to create the final shape
    shape = cuboid / lattice

    # Preview the model
    shape.preview_model()

if __name__ == "__main__":

    lattice_modification_example()