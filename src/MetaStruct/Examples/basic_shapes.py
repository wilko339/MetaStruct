from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Booleans.Boolean import SmoothUnion
from MetaStruct.Objects.Lattices.Gyroid import Gyroid

"""
Welcome to MetaStruct! Here is a file that demonstrates some of the basic features of the library using examples.

A few primitive shapes will be generated and then combined using boolean operations. You will also see how to add a
TPMS lattice to a volume of space and even use libigl to clean up the mesh prior to saving.
"""


def main():
    """
    The main function will be used to contain all the code as per usual Python practice.
    """

    # First things first, create the 'design space'. This is essentially the region of 3D space that all shapes will
    # live in during evaluation. Let's create a 10x10x10 box with 200 sample points in each dimension:
    ds = DesignSpace(200, x_bounds=[-5, 5], y_bounds=[-5, 5], z_bounds=[-5, 5])

    # Now, lets create a sphere with a radius of 4 in this region:
    sphere = Sphere(ds, r=4)

    # Let's have a look at it using mayavi. Feel free to play with the settings in the viewer!
    sphere.preview_model()

    # Simple! Now let's create a rounded cube in a similar way, except we change the origin of the shape using
    # x, y and z, and we define a rounding radius of 0.5:
    cube = Cube(ds, dim=2.5, x=2, y=2, z=2, round_r=0.5)

    # We can use the python '+' operator to create a compound shape with a boolean union:
    compound_shape = sphere + cube

    # Let's have another look:
    compound_shape.preview_model()

    # Instead of using a basic boolean union, we can also use a smooth union, and blend the two objects together:
    smooth_compound_shape = SmoothUnion(cube, sphere, blend=1.5)
    smooth_compound_shape.preview_model()

    # Now, we can use this compound shape as a region to apply a TPMS lattice. Let's use a gyroid lattice in this case:
    lattice = Gyroid(ds, lx=3, ly=3, lz=3)
    latticed_shape = smooth_compound_shape / lattice
    latticed_shape.preview_model()

    # If we want to save this as a mesh, we can do so. However, it's best to clean up the shape and simplify it to
    # save on memory. Here, there are 5 smoothing iterations followed by a decimation that reduces the triangle count
    # by 80%.
    # Note, this bit might take a minute or so to run:
    latticed_shape.find_surface()
    latticed_shape.smooth_mesh(iterations=5)
    latticed_shape.decimate_mesh(0.2)
    latticed_shape.save_mesh('Gyroid_Union')

    # The final stl file is then saved to the current working directory as a binary stl.


if __name__ == "__main__":
    main()
