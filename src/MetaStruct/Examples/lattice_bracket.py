from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.Shapes.ImportedMesh import ImportedMesh
from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Lattices.StrutLattice import RepeatingLattice, OctetTruss
from MetaStruct.Objects.Shapes.Cube import Cube


"""
This file shows how to import an existing triangular mesh and convert it into volumetric representation so it can work
with the other primitives and lattices in the package.
"""


# Change the argument here to point to the triangular mesh of choice.
def lattice_bracket(filepath='Engine_Bracket.stl'):
    # Initialise the design space as usual. Check the bounding box of your input mesh! This will be printed on import.
    # Change the resolution of the design space to change the level of detail of the mesh import.
    ds = DesignSpace(100, x_bounds=[-0.5, 179], y_bounds=[-0.5, 93], z_bounds=[-0.5, 112])

    # Intialise the imported shape object
    shape = ImportedMesh(ds, filepath)

    # Intersect the shape with a lattice or other shape of choice.
    unit_cell = OctetTruss(ds, [0, 0, 0], cell_size=20, r=2)

    uc = RepeatingLattice(ds, unit_cell=unit_cell, period=20, r=0)

    lattice_region = shape / uc

    lattice_region.evaluate_grid()

    shape.shell(4)

    final = shape + lattice_region

    # Either preview or save the mesh.
    final.preview_model(clip='x', clip_value=90)


def main():
    lattice_bracket()

if __name__ == '__main__':
    main()
