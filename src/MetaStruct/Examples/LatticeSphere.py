from MetaStruct.Objects.Booleans.Boolean import Union
from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.HollowSphere import HollowSphere


def latticed_sphere_example(outer_radius=2, outer_skin_thickness=0.1, inner_radius=1, inner_skin_thickness=0.1):

    ds = DesignSpace(resolution=200, x_bounds=[-2, 0], y_bounds=[-2, 2], z_bounds=[-2, 2])

    outer_skin = HollowSphere(design_space=ds, r=outer_radius, t=outer_skin_thickness)

    lattice_section = HollowSphere(r=outer_radius - outer_skin_thickness,
                                  t=outer_radius - outer_skin_thickness - inner_radius,
                                  design_space=ds) / Gyroid(design_space=ds)

    inner_skin = HollowSphere(r=inner_radius, t=inner_skin_thickness, design_space=ds)

    s1 = Union(outer_skin, Union(lattice_section, inner_skin))

    s1.preview_model(clip='x')

if __name__ == '__main__':
    latticed_sphere_example()
