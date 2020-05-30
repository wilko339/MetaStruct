# ImplicitCAD
Python project dedicated to creating an open-source CAD designer using implicit equations.

For the function evaluations, some have a numexpr implementation where possible. If numexpr is not installed, for now just comment out the numexpr stuff and uncomment the numpy stuff. 

The meshing functions currently use PyMesh, but if this is not available then numpy-stl can also be used ('from stl import mesh as msh' - in imports)
