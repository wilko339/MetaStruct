import time
from Objects.DesignSpace import DesignSpace
from Objects.Lattices.Gyroid import Gyroid
from Objects.Shapes.Sphere import Sphere
from Objects.Shapes.Cube import Cube
from Objects.Shapes.Shape import Shape
from Objects.Shapes.Cylinder import Cylinder
from stl import mesh


def main():

    t = time.time()

    ds = DesignSpace(100)

    print(time.time() - t)


if __name__ == '__main__':

    main()
