from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Line import SimpleLine, Line, LineZ
import numpy as np
from line_profiler_pycharm import profile


def line(x, y, z, length=1, r=0.25):
    clip = np.clip(z, -length / 2, length / 2)

    return np.linalg.norm(np.array([x, y, z - clip]), axis=0) - r


@profile
def main():
    ds = DesignSpace(resolution=500)

    quick_line = LineZ(ds)
    slow_line = Line(ds, p1=np.array([0, 0, -0.5]), p2=np.array([0, 0, 0.5]), r=0.25)

    x = ds.X[:, None, None]
    y = ds.Y[None, :, None]
    z = ds.Z[None, None, :]

    quick_line.evaluate_point(x, y, z)

    #quick_line.vector_rotation()

    slow_line.evaluate_grid()
    slow_line.evaluate_point_bc(x, y, z)

    #slow_line.preview_model()

    # line_z.preview_model()

if __name__ == '__main__':
    main()
