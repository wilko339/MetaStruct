import trimesh
import mesh_to_sdf
from Objects.DesignSpace import DesignSpace
from Objects.Lattices.Gyroid import Gyroid
from Objects.Shapes.Shape import Shape


def lattice_bracket():

    ds = DesignSpace(100)

    mesh = trimesh.load_mesh('D:\\ImplicitCAD\\Engine_Bracket.STL')

    voxels = mesh_to_sdf.mesh_to_voxels(
        mesh, ds.resolution, surface_point_method='sample')

    shape = Shape(ds)

    shape.evaluated_grid = voxels

    shape.x_limits = shape.y_limits = shape.z_limits = [-1, 1]

    shape /= Gyroid(ds)

    shape.previewModel()
