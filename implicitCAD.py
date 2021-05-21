from Objects.DesignSpace import DesignSpace
from Objects.Lattices.Gyroid import Gyroid
from Objects.Shapes.Cube import Cube

from Objects.Shapes.ImportedMesh import ImportedMesh

from wildmeshing import Tetrahedralizer


def main():

    ds = DesignSpace(200, x_bounds=[-1, 180], y_bounds=[
                     -1, 93], z_bounds=[-1, 112])

    bracket = ImportedMesh(ds, 'Engine_Bracket.stl')

    bracket /= Gyroid(ds, lx=20, ly=20, lz=20)

    bracket.findSurface()

    bracket.decimate_mesh(0.5)


    bracket.save_mesh('decimated')


if __name__ == '__main__':
    main()
