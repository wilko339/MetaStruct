from Examples.LeosRings import leos_rings

from Objects.Shapes.Cube import Cube
from Objects.Lattices.Gyroid import Gyroid
from Objects.DesignSpace import DesignSpace
from Objects.Shapes.ImportedMesh import ImportedMesh
from Objects.DesignSpace import DesignSpace

import igl
import numpy as np


def main():
    ds = DesignSpace(200, x_bounds=[-23.5508194,  84.19611359],
                     y_bounds=[-42.00993729, 45.79184723], z_bounds=[5.27508545, 113.1668396])

    lattice = Gyroid(ds, lx=10, ly=10, lz=10)

    bunny = ImportedMesh(ds, 'Stanford_Bunny.stl')

    #bunny /= lattice

    # bunny.previewModel(mode='volume')


if __name__ == '__main__':
    main()
