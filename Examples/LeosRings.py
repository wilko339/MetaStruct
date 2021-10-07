from Objects.DesignSpace import DesignSpace
from Objects.Shapes.Cylinder import Cylinder
import math
from Objects.Lattices.GyroidNetwork import GyroidNetwork
from Objects.Lattices.Gyroid import Gyroid
from Objects.Lattices.DoubleGyroidNetwork import DoubleGyroidNetwork
from Objects.Lattices.BCC import BCC
from Objects.Lattices.Diamond import Diamond
from Objects.Lattices.Primitive import Primitive
from Objects.Shapes.Cube import Cube


def leos_rings():

    height = 11
    rim = 0.5

    ds = DesignSpace(resolution=0, x_resolution=300, y_resolution=300, z_resolution=100, x_bounds=[-30, 30],
                     y_bounds=[-30, 30], z_bounds=[-5.5, 5.5])

    lattice_region = Cylinder(ds, r1=30, r2=30, l=height/2) - \
        Cylinder(ds, r1=22.5, r2=22.5, l=height/2)

    lat_x = 7.5
    lat_z = 10

    x = lat_x / 2
    z = height/2

    for use_rim in [True, False]:
        for rim in [0.5, 0.75, 1]:
            for cartesian in [True, False]:
                if cartesian is False:
                    lat_y = math.pi / 10
                else:
                    lat_y = 7.5
                for vf in [0.3, 0.5, 0.75]:
                    for lattice in [Primitive(
                        ds, x=x, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf),
                            Diamond(
                            ds, x=x, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf),
                            Gyroid(
                            ds, x=x, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf),
                            GyroidNetwork(
                            ds, x=x, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf),
                            DoubleGyroidNetwork(
                            ds, x=x, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf),
                            BCC(
                            ds, x=x, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf)]:

                        if cartesian is False:

                            lattice.convertToCylindrical()

                        latticed = lattice_region / lattice

                        if use_rim is True:

                            rims = Cylinder(ds, r1=30, r2=30, l=rim/2, z=height/2-rim/2) - \
                                Cylinder(ds, r1=30-rim, r2=30-rim, l=rim/2, z=height/2-rim/2) + \
                                Cylinder(ds, r1=30, r2=30, l=rim/2, z=-(height/2-rim/2)) - \
                                Cylinder(ds, r1=30-rim, r2=30-rim, l=rim/2, z=-(height/2-rim/2)) + \
                                Cylinder(ds, r1=22.5+rim, r2=22.5+rim, l=rim/2, z=height/2-rim/2) - \
                                Cylinder(ds, r1=22.5, r2=22.5, l=rim/2, z=height/2-rim/2) + \
                                Cylinder(ds, r1=22.5+rim, r2=22.5+rim, l=rim/2, z=-(height/2-rim/2)) - \
                                Cylinder(ds, r1=22.5, r2=22.5,
                                         l=rim/2, z=-(height/2-rim/2))

                            latticed += rims

                        # latticed.previewModel()

                        latticed.findSurface()

                        latticed.decimate_mesh(0.1)

                        latticed.smooth_mesh(4, 0.33)

                        name = f"{lattice.name+str(int(vf*100))}vf_"
                        if cartesian is True:
                            name += "cart_"
                        else:
                            name += "polar_"

                        if use_rim is True:
                            name += f"rim{rim}_"

                        name += "071021"

                        latticed.save_mesh(
                            f'C:\\Users\\Toby\\Added Scientific Ltd\\AISIN - General\\{name}')


def samples():
    ds = DesignSpace(200)
    volume = Cube(ds)

    for vf in [0.2, 0.3, 0.5]:

        for lattice in [Gyroid(ds, vf=vf),
                        DoubleGyroidNetwork(ds, vf=vf),
                        Diamond(ds, vf=vf),
                        BCC(ds, vf=vf),
                        GyroidNetwork(ds, vf=vf)]:

            sample = volume / lattice

            sample.findSurface()

            sample.decimate_mesh(0.5)

            sample.save_mesh(f'{lattice.name+str(vf)}')


def polar_v_cartesian():

    height = 11

    ds = DesignSpace(resolution=200, x_resolution=0, y_resolution=600, z_resolution=300, x_bounds=[-30, 30],
                     y_bounds=[-30, 30], z_bounds=[-5.5, 5.5])

    lattice_region = Cylinder(ds, r1=30, r2=30, l=height/2) - \
        Cylinder(ds, r1=22.5, r2=22.5, l=height/2)

    lat_x = 7.5
    lat_y = 7.5
    lat_z = 10

    x = 0
    z = 1

    for vf in [0.5]:

        for lattice in [Gyroid(
                ds, x=x, z=z, lx=lat_x, ly=lat_y, lz=lat_z, vf=vf)]:

            # lattice.convertToCylindrical()

            latticed = lattice_region / lattice

            latticed.findSurface()

            latticed.decimate_mesh(0.2)

            latticed.smooth_mesh(5, 0.33)

            latticed.save_mesh(
                f'{latticed.name+str(vf)}_cartesian')
