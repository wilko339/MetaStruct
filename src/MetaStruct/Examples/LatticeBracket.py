from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.Shapes.Shape import Shape
from MetaStruct.Objects.Shapes.ImportedMesh import ImportedMesh
from MetaStruct.Objects.designspace import DesignSpace


def lattice_bracket():

    ds = DesignSpace(100)

    shape = ImportedMesh(ds)

    shape /= Gyroid(ds)

    shape.previewModel()
