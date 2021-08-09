from Objects.DesignSpace import DesignSpace
from Objects.Lattices.Gyroid import Gyroid
from Objects.Shapes.Cuboid import Cuboid


def lattice_slabs():

    skin_thicks = [2.0, 1.5, 1.0]
    vfs = [0.5, 0.25, 0.1]

    ds = DesignSpace(x_resolution=350, y_resolution=210, z_resolution=70, x_bounds=[0, 50], y_bounds=[
                     0, 30], z_bounds=[0, 10])

    for vf_idx, vf in enumerate(vfs):

        volume = Cuboid(ds, x=25, y=15, z=5, xd=24.99, yd=14.99, zd=4.9)

        lattice = Gyroid(ds, x=25, y=15, z=5, lx=5, ly=5, lz=5, vf=vf)

        volume /= lattice

        for sk_idx, skin in enumerate(skin_thicks):

            skins = Cuboid(ds, x=25, y=15, z=skin/2, xd=25, yd=15, zd=skin/2) + \
                Cuboid(ds, x=25, y=15, z=10-(skin/2), xd=25, yd=15, zd=skin/2)

            volume += skins

            volume.findSurface()

            # volume.previewModel()

            volume.decimate_mesh(0.15)

            volume.save_mesh(f'slab_{int(vf*100)}_{skin}_quarter')

            volume.save_tet_mesh(filename=f'slab_{int(vf*100)}_{skin}_quarter')


def lattice_coupons(vf=0.5, skin=1.0):

    ds = DesignSpace(resolution=100, x_bounds=[-5, 5],
                     y_bounds=[-5, 5], z_bounds=[-5, 5])

    lattice_volume = Cuboid(ds, xd=5, yd=5, zd=4.9)

    lattice = Gyroid(ds, lx=5, ly=5, lz=5, vf=vf)

    lattice_volume /= lattice

    skins = Cuboid(ds, z=(skin/2)-5, xd=5, yd=5, zd=skin/2) + \
        Cuboid(ds, z=5-(skin/2), xd=5, yd=5, zd=skin/2)

    lattice_volume += skins

    lattice_volume.findSurface()

    lattice_volume.decimate_mesh(0.5)

    lattice_volume.save_mesh('test_coupon')


def main():

    lattice_coupons()


if __name__ == "__main__":

    main()
