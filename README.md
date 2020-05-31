# ImplicitCAD
Python project dedicated to creating an open-source CAD designer using implicit equations.

# Required External Packages

1. NumPy - Certain array functions
2. NumExpr - Implicit function evaluations
3. Visvis - Preview model
4. Scikit-image - Marching Cubes
5. PyMesh - Exporting and cleaning meshes
6. Numpy-stl - Can be used instead of PyMesh to save a mesh, but no cleaning
7. perlin3d - For Perlin noise (clone from GitHub Repository)

# Architecture

ImplicitCAD defines all shapes and operations as objects, each with specific attributes and methods. All objects inherit from the "Geometry" class, which is where the "previewModel()" and "saveMesh()" methods (among others) are located.

# Workflow

1. Define a design space using in instance of "DesignSpace":
The design space contains the x, y, z points where all subsequent functions will be evaluated. This is where the resolution of the model is determined using the "res" argument. This determines the number of sample points in all 3 axes. Use the "xBounds", "yBounds" and "zBounds" arguments to set the size of the bounding box containing the model. 

2. Define shapes:
All shapes are declared in the standard way, ie "sphere = Sphere(args)" where args are the arguments. The design space MUST ALWAYS be passed into primitive shapes and lattices (boolean ops inherit the design space from the given shapes) as the first argument. All shapes have default values for the sizing (eg a Sphere has a radius of 1 by default). These can be set by passing in the arguments when calling the object. 

3. Previewing a Model:
All shapes will use the "previewModel()" method to generate a 3D view using Visvis. Simply call this method on an object (ie Sphere(designSpace).previewModel()) to see a render of the object. A clipping plane can be provided by passing the axis as a string into the "clip" argument (ie previewModel(clip='x'). The coordinate of that clipping plane can also be specified with the "clipVal" argument. The side of the plane that is clipped can be switched by using the "flipClip" argument and passing a boolean True or False. This is where the implicit calculations for the shapes will normally be evaluated. Marching Cubes is used to generate the mesh which is passed to Visvis.

# Lattices

Currently, the following lattices are supported:

1. Gyroid Surface (defines a single surface and fills the negative side)
2. Gyroid (essentially a boolean subtraction between a gyroid surface and its negative to give thick surface)
2. Gyroid Network
3. Double Gyroid Network
4. Primitive Surface (like the gyroid surface, filled on the negative side)
5. Primitive (similar to Gyroid, subtraction of 2 surfaces)
6. Primitive Network
7. Diamond Surface
8. Diamond
9. Diamond Network

# Boolean Operations
