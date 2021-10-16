from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.ImportedMesh import ImportedMesh
from importlib import resources
import io


def main(file="Engine_Bracket.STL"):

    ds = DesignSpace(100, x_bounds=[-1, 180], y_bounds=[-1, 93], z_bounds=[-1, 112])
    shape = ImportedMesh(ds, file)
    shape.preview_model()


if __name__ == "__main__":
    main()
