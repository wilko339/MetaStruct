from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Lattices.StrutLattice import RepeatingLattice, AxialCentric, BCCAxial, OctetTruss
from MetaStruct.Functions.ModifierArray import create_modifier_array
from MetaStruct.Objects.Shapes.Line import Line, LineZ
import numpy as np
from line_profiler_pycharm import profile

@profile
def main():
    ds = DesignSpace(resolution=300, x_bounds=[-5, 5], y_bounds=[-5, 5], z_bounds=[-5, 5])

    cell = OctetTruss(ds, cell_size=2, r=0.15)

    uc = RepeatingLattice(ds, unit_cell=cell, period=2, r=0) / Cube(ds, dim=4)

    uc.evaluate_grid()

    return

if __name__ == '__main__':
    main()