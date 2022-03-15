from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Lattices.StrutLattice import RepeatingLattice
from MetaStruct.Objects.Lattices.StrutLattice import RhombicDodecahedron
from MetaStruct.Objects.Lattices.StrutLattice import OctetTruss
from MetaStruct.Objects.Shapes.Cube import Cube


def main():
    ds = DesignSpace()

    p = 1
    uc1 = RhombicDodecahedron(ds, r=0.05, cell_size=p, centre=[-0.5, -0.5, -0.5])
    uc2 = OctetTruss(ds, r=0.05, cell_size=p, centre=[-0.5, -0.5, -0.5])
    lattice1 = RepeatingLattice(ds, uc1, period=p) / Cube(ds)
    lattice2 = RepeatingLattice(ds, uc2, period=p) / Cube(ds)

    uc1.preview_model()
    lattice1.preview_model()

    uc2.preview_model()
    lattice2.preview_model()


if __name__ == "__main__":
    main()
