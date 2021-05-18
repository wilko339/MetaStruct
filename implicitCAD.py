from Objects.DesignSpace import DesignSpace
from Objects.Shapes.Cube import Cube
from Objects.Lattices.Gyroid import Gyroid
from smt.surrogate_models import RMTB
import numpy as np
from Functions.ModifierArray import createModifierArray

from Objects.Shapes.ImportedShape import ImportedShape

import igl


def main():

    v, f = igl.read_triangle_mesh('Stanford_Bunny.stl')
    print("Mesh Loaded")

    raise

    bbox = mesh.bbox
    n = 75

    offset = 5

    ds = DesignSpace(n,
                     x_bounds=[bbox[0][0] - offset, bbox[1][0] + offset],
                     y_bounds=[bbox[0][1] - offset, bbox[1][1] + offset],
                     z_bounds=[bbox[0][2] - offset, bbox[1][2] + offset])
    limits = np.array([ds.x_bounds, ds.y_bounds, ds.z_bounds])

    try:

        dists = np.load('bunny_dists.npy')

    except FileNotFoundError:

        print(f"Computing mesh sdf...")
        dists, _, _, _ = pymesh.signed_distance_to_mesh(
            mesh, ds.coordinate_list)

        np.save('bunny_dists', dists)
        print("Done")

    ds2 = DesignSpace(resolution=200,
                      x_bounds=ds.x_bounds,
                      y_bounds=ds.y_bounds,
                      z_bounds=ds.z_bounds)
    bunny_outer = Cube(ds2)

    try:

        bunny_outer.evaluated_grid = np.load('bunny_grid.npy')

    except FileNotFoundError:

        print("Interpolating...")

        interp = RMTB(xlimits=limits,
                      nonlinear_maxiter=10,
                      min_energy=False,
                      order=3)
        interp.set_training_values(ds.coordinate_list, dists)

        interp.train()

        print("Done")

        print("Predicting new data")
        bunny_outer.evaluated_grid = interp.predict_values(
            ds2.coordinate_list).reshape(ds2.resolution, ds2.resolution,
                                         ds2.resolution)
        np.save('bunny_grid', bunny_outer.evaluated_grid)
        print("Done")

    lattice = Gyroid(ds2, lx=20, ly=20, lz=20)

    lattice.evaluateDistance()

    lattice.vf = createModifierArray(lattice, 0.2, 1, 'z')

    bunny_outer /= lattice

    bunny_outer.previewModel()


if __name__ == '__main__':
    main()
