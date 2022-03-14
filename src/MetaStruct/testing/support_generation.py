from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Shapes.SupportVolume import SupportVolume


def main():
    ds = DesignSpace(resolution=300, x_bounds=[-1.1, 1.1], y_bounds=[-1.1, 1.1], z_bounds=[-1.1, 2.1])
    shape = Sphere(ds, z=0.5) / Gyroid(ds, vf=0.3)

    shape.preview_model()

    shape.preview_projection()

    support = SupportVolume(shape)

    support.preview_model()

    support /= Gyroid(ds, lx=0.3, ly=0.3, lz=0.3, vf=0.2)

    support.preview_model()

    support += shape

    support.preview_model()


if __name__ == "__main__":
    main()