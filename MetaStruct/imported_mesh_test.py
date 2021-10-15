from MetaStruct.Objects.DesignSpace import DesignSpace
from MetaStruct.Objects.Shapes.ImportedMesh import ImportedMesh


def main():
    ds = DesignSpace(100, x_bounds=[-1, 180], y_bounds=[-1, 93], z_bounds=[-1, 112])
    shape = ImportedMesh(ds, "Engine_Bracket.STL")
    shape.preview_model()


if __name__ == "__main__":
    main()