from Objects.DesignSpace import DesignSpace
from Objects.Shapes.Cube import Cube
from Objects.Lattices.Gyroid import Gyroid
from smt.surrogate_models import RMTB
import numpy as np
from Functions.ModifierArray import createModifierArray

from Objects.Shapes.ImportedMesh import ImportedMesh

import igl


def main():

    ds = DesignSpace(200, x_bounds=[-1, 180], y_bounds=[
                     -1, 93], z_bounds=[-1, 112])

    bracket = ImportedMesh(ds, 'Engine_Bracket.stl')

    bracket.previewModel()


if __name__ == '__main__':
    main()
