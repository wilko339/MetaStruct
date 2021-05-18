from Objects.DesignSpace import DesignSpace
from Objects.Shapes.Cylinder import Cylinder
import math
from Objects.Lattices.GyroidNetwork import GyroidNetwork


def leos_rings():

    ds = DesignSpace(resolution=200, x_resolution=0, y_resolution=200, z_resolution=1200, x_bounds=[-20, 20],
                     y_bounds=[-2.5, 2.5], z_bounds=[-20, 20])

    outer_removal_band = Cylinder(ds, r1=21, r2=21, l=2) - \
        Cylinder(ds, r1=19, r2=19, l=2)

    inner_removal_band = Cylinder(ds, r1=16, r2=16, l=2) - \
        Cylinder(ds, r1=14, r2=14, l=2)

    outer_skin = Cylinder(ds, r1=20, r2=20, l=2.5) - \
        Cylinder(ds, r1=19.5, r2=19.5, l=2.5) - outer_removal_band

    inner_skin = Cylinder(ds, r1=15.5, r2=15.5, l=2.5) - \
        Cylinder(ds,  r1=15, r2=15, l=2.5) - inner_removal_band

    lattice_region = Cylinder(ds, r1=20, r2=20, l=2.5) - \
        Cylinder(ds, r1=15, r2=15, l=2.5)

    lat_x = 2.5
    lat_y = math.pi / 20
    lat_z = 2.5

    for vf in [0.2]:

        for lattice in [GyroidNetwork(
                ds, x=-0.35, z=-0.35, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf)]:

            lattice.convertToCylindrical()

            latticed = lattice_region / lattice

            latticed += outer_skin

            latticed += inner_skin

            latticed.previewModel()
