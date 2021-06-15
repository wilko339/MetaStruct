from Objects.DesignSpace import DesignSpace
from Objects.Shapes.Cylinder import Cylinder
import math
from Objects.Lattices.GyroidNetwork import GyroidNetwork


def leos_rings():

    ds = DesignSpace(resolution=500, x_resolution=0, y_resolution=200, z_resolution=1200, x_bounds=[-20, 20],
                     y_bounds=[-20, 20], z_bounds=[-7, 7])

    outer_removal_band = Cylinder(ds, r1=21, r2=21, l=5) - \
        Cylinder(ds, r1=19, r2=19, l=5)

    inner_removal_band = Cylinder(ds, r1=16, r2=16, l=5) - \
        Cylinder(ds, r1=14, r2=14, l=5)

    outer_skin = Cylinder(ds, r1=20, r2=20, l=6) - \
        Cylinder(ds, r1=19.5, r2=19.5, l=6) - outer_removal_band

    inner_skin = Cylinder(ds, r1=15.5, r2=15.5, l=6) - \
        Cylinder(ds,  r1=15, r2=15, l=6) - inner_removal_band

    lattice_region = Cylinder(ds, r1=20, r2=20, l=6) - \
        Cylinder(ds, r1=15, r2=15, l=6)

    lat_x = 5
    lat_y = math.pi / 10
    lat_z = 6

    for vf in [0.2, 0.3, 0.4, 0.5]:

        for lattice in [GyroidNetwork(
                ds, x=-0.35, z=0.2, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf)]:

            lattice.convertToCylindrical()

            latticed = lattice_region / lattice

            latticed.previewModel(mode='volume')

            raise

            latticed.findSurface()

            latticed.decimate_mesh(0.2)

            latticed.save_mesh(latticed.name+str(vf))
