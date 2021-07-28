from Objects.DesignSpace import DesignSpace
from Objects.Lattices.Gyroid import Gyroid
from Objects.Shapes.Cuboid import Cuboid

def main():

    ds = DesignSpace(200, x_bounds=[0, 100], y_bounds=[0, 100], z_bounds=[0, 10])

    volume = Cuboid(ds, x=100,y=30,z=5,xd=50, yd=30, zd=5)

    volume.previewModel()

if __name__ == "__main__":

    main()

