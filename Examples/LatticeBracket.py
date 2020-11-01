import trimesh
import mesh_to_sdf
from Objects.DesignSpace import DesignSpace
from Objects.Lattices.Gyroid import Gyroid
from Objects.Shapes.Shape import Shape


def lattice_bracket():

    ds = DesignSpace(100)

    mesh = trimesh.load_mesh('D:\\ImplicitCAD\\Engine_Bracket.STL')

    voxels = mesh_to_sdf.mesh_to_voxels(
        mesh, ds.res, surface_point_method='sample')

    shape = Shape(ds)

    shape.evaluatedGrid = voxels

    shape.xLims = shape.yLims = shape.zLims = [-1, 1]

    shape /= Gyroid(ds)

    shape.previewModel()
