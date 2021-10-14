from Objects.Shapes.Cylinder import Cylinder
from Objects.DesignSpace import DesignSpace
from Objects.Lattices.Primitive import Primitive


def main():
    # Execute code here
    ds = DesignSpace()
    shape = Cylinder(ds)
    shape /= Primitive(ds)
    shape.previewModel()
    
if __name__ == '__main__':
    main()
