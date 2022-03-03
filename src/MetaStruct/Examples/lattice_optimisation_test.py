from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Sphere import Sphere
from MetaStruct.Objects.Shapes.Cube import Cube
from MetaStruct.Objects.Lattices.StrutLattice import RepeatingLattice, AxialCentric, BCCAxial, OctetTruss, \
    RhombicDodecahedron
from MetaStruct.Objects.Lattices.Gyroid import Gyroid
from MetaStruct.Objects.Lattices.Diamond import Diamond
from MetaStruct.Objects.Lattices.Primitive import Primitive
from MetaStruct.Objects.Booleans.Boolean import Subtract, Add
from MetaStruct.Functions.ModifierArray import create_modifier_array
import numpy as np
import numexpr as ne
from line_profiler_pycharm import profile

@profile
def main():
    ds = DesignSpace(resolution=200, x_bounds=[-1, 1], y_bounds=[-1, 1], z_bounds=[-1, 1])

    cell = RhombicDodecahedron(ds, cell_size=2, r=0.15)

    uc = RepeatingLattice(ds, unit_cell=cell, period=2, r=0) / Cube(ds, dim=4)

    lat1 = Gyroid(ds, nx=1.5, ny=1.5, nz=1.5, vf=0.35)
    lat2 = Primitive(ds, nx=1.5, ny=1.5, nz=1.5, vf=0.35)
    lat3 = Diamond(ds, nx=1.5, ny=1.5, nz=1.5, vf=0.35)

    lat1.evaluate_grid()
    lat2.evaluate_grid()
    lat3.evaluate_grid()

    # lat1.vector_rotation()
    # lat2.vector_rotation([-1,1,1])
    # lat3.vector_rotation([1,2,1])

    cube = Cube(ds, dim=1)

    shape1 = lat1
    shape2 = lat2
    shape3 = lat3

    p1 = np.linalg.norm(np.array([ds.X, ds.Y, ds.Z]) - np.array([-0.5, 0, 0]))
    p2 = np.linalg.norm(np.array([ds.X, ds.Y, ds.Z]) - np.array([0.5, 0, 0]))
    p3 = np.linalg.norm(np.array([ds.X, ds.Y, ds.Z]) - np.array([0, 0.5, 0]))

    k = 20

    w1 = ne.evaluate('1+exp(k*g1)', local_dict={'k': k, 'g1': p1})
    w2 = ne.evaluate('1+exp(k*g2)', local_dict={'k': k, 'g2': p2})
    w3 = ne.evaluate('1+exp(k*g3)', local_dict={'k': k, 'g3': p3})

    sum_ = ne.evaluate('w1 + w2 + w3')

    w1 = ne.evaluate('w1 / sum_')
    w2 = ne.evaluate('w2 / sum_')
    w3 = ne.evaluate('w3 / sum_')

    shape1.evaluated_grid *= w1
    shape2.evaluated_grid *= w2
    shape3.evaluated_grid *= w3

    new_shape = Add(Add(shape1, shape2), shape3) / cube

    new_shape.evaluate_grid()

    new_shape.preview_model()

    return

    uc.transform()

    uc.preview_model()

if __name__ == '__main__':
    main()