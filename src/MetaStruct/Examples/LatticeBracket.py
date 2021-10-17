from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.Shapes.ImportedMesh import ImportedMesh
from MetaStruct.Objects.designspace import DesignSpace


def lattice_bracket(filepath=None):

    ds = DesignSpace(100)

    shape = ImportedMesh(ds, filepath)

    shape /= Gyroid(ds)

    shape.previewModel()
