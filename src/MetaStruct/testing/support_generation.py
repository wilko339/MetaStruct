from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Shapes.SupportVolume import SupportVolume


def main():
    ds = DesignSpace(resolution=400, x_bounds=[-1.1, 1.1], y_bounds=[-1.1, 1.1], z_bounds=[-1.1, 2.1])
    shape = Sphere(ds, z=0.5) / Gyroid(ds, vf=0.5)

    support = SupportVolume(shape)

    support /= Gyroid(ds, lx=0.3, ly=0.3, lz=0.3, vf=0.2)

    support += shape

    support.preview_model()


if __name__ == "__main__":
    main()