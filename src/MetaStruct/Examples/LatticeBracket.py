from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.Shapes.ImportedMesh import ImportedMesh
from MetaStruct.Objects.designspace import DesignSpace


def lattice_bracket(filepath=None):

    ds = DesignSpace(100, x_bounds=[-1, 180], y_bounds=[-1, 93], z_bounds=[-1, 112])

    shape = ImportedMesh(ds, filepath)

    shape.preview_model()

    shape /= Gyroid(ds)

    shape.preview_model()


if __name__ ==  '__main__':
    lattice_bracket('/Users/tobywilkinson/PycharmProjects/MetaStruct/src/MetaStruct/Engine_Bracket.STL')