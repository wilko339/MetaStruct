from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.Shapes.ImportedMesh import ImportedMesh
from MetaStruct.Objects.designspace import DesignSpace


"""
This file shows how to import an existing triangular mesh and convert it into volumetric representation so it can work
with the other primitives and lattices in the package.
"""


# Change the argument here to point to the triangular mesh of choice.
def lattice_bracket(filepath='Engine_Bracket.stl'):
    # Initialise the design space as usual. Check the bounding box of your input mesh! This will be printed on import.
    # Change the resolution of the design space to change the level of detail of the mesh import.
    ds = DesignSpace(150, x_bounds=[-0.5, 179], y_bounds=[-0.5, 93], z_bounds=[-0.5, 112])

    # Intialise the imported shape object
    shape = ImportedMesh(ds, filepath)

    # Intersect the shape with a lattice or other shape of choice.
    shape /= Gyroid(ds, lx=15, ly=15, lz=15)

    # Either preview or save the mesh.
    shape.preview_model()


def main():
    lattice_bracket()

if __name__ == '__main__':
    main()
