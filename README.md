# MetaStruct

A Python project for open-source CAD design using implicit equations (or FREP, volumetric geometry).

# License

This project is licensed under the MIT license. 

# Installation

Ensure you are using Python 3.7 or above.

Clone the code into a local folder:

    git clone https://github.com/wilko339/MetaStruct.git

Navigate into the root directory of the repository and pip install locally in dev mode using:
    
    pip install -e .

Use conda to install libigl python bindings:

    conda install igl

There are a few quick ways to check if things are working (until proper tests are written...)

    import MetaStruct as mt
    mt.latticed_sphere_example()

Or...

    import MetaStruct as mt
    mt.voro_test()

If all works, mayavi windows will open for each example with the geometry in.

# Architecture

MetaStruct uses object-oriented programming and defines all shapes and operations as objects, each with certain attributes and methods. All objects inherit from the "Geometry" class, which is where the "previewModel()" and "save_mesh()" methods (among others) are located. Everything requires a "DesignSpace" object, containing the arrays of X, Y and Z coordinates to evaluate the functions at. Marching cubes is then used to extract a triangular mesh from the distance field which can be previewed or cleaned with libigl and exported.

# Workflow

1. Define a design space using an instance of "DesignSpace":
The design space contains the x, y, z points where all subsequent functions will be evaluated. This is where the resolution of the model is determined using the "res" argument. This determines the number of sample points in all 3 axes. Use the "x_bounds", "y_bounds" and "z_bounds" arguments to set the size of the bounding box containing the model. There are individual resolution options available for the three axes (x_resolution etc) if required. This is a more efficient way if your bounding box has significantly different x, y and z sizes.

2. Define shapes:
All shapes are declared in the standard OOP way, ie "sphere = Sphere(ds, args)" where ds is a DesignSpace instance args are the arguments. The design space MUST ALWAYS be passed into primitive shapes and lattices (boolean ops inherit the design space from the given shapes) as the first argument. All shapes should have default values for the sizing (eg a Sphere has a radius of 1 by default). These can be set by passing in the arguments when calling the object. The x, y and z arguments for lattices and shapes are the coordinates of the centre point for the shape and all default to 0. Change these to move the object.

3. Previewing a Model:
All shapes use the "preview_model()" method to generate a 3D view using Mayavi. Simply call this method on an object (ie Sphere(designSpace).previewModel()) to see a render of the object. A clipping plane can be provided by passing the axis as a string into the "clip" argument (ie previewModel(clip='x'). The coordinate of that clipping plane can also be specified with the "clipVal" argument. The side of the plane that is clipped can be switched by using the "flipClip" argument and passing a boolean True or False. This is where the implicit calculations for the shapes will normally be evaluated. Marching Cubes is used to generate the mesh to be rendered or saved to a file.

# Lattices

Currently, the following TPMS lattices are supported:

1. Gyroid
2. Double Gyroid Network
3. Primitive 
4. Diamond
5. BCC (TPMS Approximation)
6. Composite Lattice (a mix of the above)

All of these TPMS lattices have the same input arguments.

lx, ly, lz : Define the length of the lattice unit cell in the 3 dimensions
nx, ny, nz : Define the number of unit cells per unit cell length
vf : The volume fraction (as a decimal, ie 0.5 = 50%)

The SDFs of these lattices are not euclidean distances, so a value of 1 will not necessarily mean the point is 1 unit from the surface. 

Various strut-based lattices are also available:

1. Voronoi
2. Delaunay
3. Convex Hull
4. Random (nearest neighbours)
5. Regular Strut

Some of these rely on a Point Cloud. There are some point clouds built in to assist with this process. 

# Shapes

There are a range of primitive shapes available:

1. Cuboid
2. Cube (special case of a cuboid, has a filleting argument as well)
3. Spheroid
4. Sphere (special case of a sphere)
5. Cylinder
6. Torus (why not)
7. Line (or finite capsule)

These inherit from the generic "Shape" class, and have different arguments to define lengths. Note, for the cube and cuboid, the dimensions in each axis (xd, yd and zd) are radii, so the distance from the centre point to the centre of each face. Effectively, the dimension you input is half the length of each side. Maybe this will be changed in the future if its not intuitive.

# Boolean Operations

There are a number of boolean operations available:

1. Union (can use the "+" operator)
2. Difference (can use the "-" operator)
3. Intersection (can use the "/" operator)
4. Blend
5. Smooth Union

For readability, some of the most commonly used booleans have been mapped to the mathematical operators +, - and / using magic (or dunder) methods. For example, the union between a Sphere and a Cube could be defined in two ways:

    ds = DesignSpace()
    shape_short = Sphere(ds) + Cube(ds)

    shape_long = Union(Sphere(ds), Cube(ds))

There are also some mathematical operators if required:

1. Add
2. Subtract
3. Multiply
4. Divide

# Future Improvements

There are lots of places where this project needs improvement! Here is a non-exhaustive list with some ideas:
    
1. Some documentation
2. PEP stuff
3. More speed, especially for the strut lattices
4. Simpler dependencies (mayavi is useful, but possibly a bit heavy to list as a requirement..)
5. More lattices & primitive shapes
6. Faster / more efficient mesh to sdf conversion process (for importing stls)
7. Better implicit mesher (dual contouring etc)
8. Tests

# Contributing

Contributions to this project are very welcome! This started as a learning exercise, so there are plenty of examples of bad coding practice and things written to just work. I welcome all contributions from spell checking and variable renaming to more substantial changes in architecture, if these are beneficial!

I would also really appreciate comments / explanations for how the proposed change works so that I can continue learning better Python and more advanced methods. 

# About the Project

This project started out as an exercise in learning what implicit geometry is and how it can be used to make 3D objects. Development began in March 2020 and is ongoing. 

Credit goes to Added Scientific Ltd (addedscientific.com) for providing resources for the kick-off and early development of the project and for allowing the public release of this code for ongoing development.