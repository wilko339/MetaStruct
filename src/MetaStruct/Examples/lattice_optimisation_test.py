from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Lattices.StrutLattice import OptimisationLattice


def main():
    ds = DesignSpace(resolution=150, x_bounds=[-1, 11], y_bounds=[-1, 11], z_bounds=[-1, 11])
    lattice = OptimisationLattice(ds, 'AM_Cube_LB007_BD_X_B_100.csv')

    lattice.preview_model()

if __name__ == '__main__':
    main()