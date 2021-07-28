from Objects.DesignSpace import DesignSpace
from Objects.Shapes.Cylinder import Cylinder
import math
from Objects.Lattices.GyroidNetwork import GyroidNetwork
from Objects.Lattices.Gyroid import Gyroid
from Objects.Lattices.DoubleGyroidNetwork import DoubleGyroidNetwork
from Objects.Lattices.BCC import BCC
from Objects.Lattices.Diamond import Diamond

import igl


def leos_rings():

    height = 11

    ds = DesignSpace(resolution=200, x_resolution=0, y_resolution=600, z_resolution=300, x_bounds=[-30, 30],
                     y_bounds=[-30, 30], z_bounds=[-5.5, 5.5])

    lattice_region = Cylinder(ds, r1=30, r2=30, l=height/2) - \
        Cylinder(ds, r1=22.5, r2=22.5, l=height/2)

    lat_x = 7.5
    lat_y = math.pi / 10
    lat_z = 10

    x=0
    z=1

    for vf in [0.2, 0.3]:
        
        for lattice in [GyroidNetwork(
                ds, x=x+1, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf),
                DoubleGyroidNetwork(
                ds, x=x+1, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf),
                Gyroid(
                ds, x=x, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf),
                BCC(
                ds, x=x, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf),
                Diamond(
                ds, x=x, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf)]:

            lattice.convertToCylindrical()

            latticed = lattice_region / lattice

            latticed.previewModel(mode='volume')

            raise

            latticed.findSurface()

            latticed.decimate_mesh(0.2)

            latticed.smooth_mesh(5, 0.33)

            latticed.save_mesh(f'C:\\Users\\Toby Wilkinson\\Added Scientific Ltd\\Design & Comp. Team - General\\CAD Files\\LeoRings\\temp\\{latticed.name+str(vf)}')
