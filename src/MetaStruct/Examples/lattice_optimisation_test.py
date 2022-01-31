from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Lattices.StrutLattice import RepeatingLattice, AxialCentric, BCCAxial, OctetTruss
from MetaStruct.Functions.ModifierArray import create_modifier_array
from MetaStruct.Objects.Shapes.Line import Line
import numpy as np
from line_profiler_pycharm import profile

@profile
def main():
    ds = DesignSpace(resolution=250, x_bounds=[-5, 5], y_bounds=[-5, 5], z_bounds=[-5, 5])

    cell = OctetTruss(ds, cell_size=2, r=0.1)

    uc = RepeatingLattice(ds, unit_cell=cell, period=2, r=0) / Cube(ds, dim=3)

    uc.vector_rotation()

    uc.preview_model()

    return

if __name__ == '__main__':
    main()