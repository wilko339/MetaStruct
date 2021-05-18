from Objects.Shapes.Shape import Shape
import numpy as np
import igl
import cProfile
import pstats
import io


def profile(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return wrapper


class ImportedMesh(Shape):
    def __init__(self, designSpace, filepath):
        super().__init__(designSpace, x=0, y=0, z=0)
        try:
            self.filepath = filepath
            self.vertices, self.faces = igl.read_triangle_mesh(filepath)
            print('Mesh Loaded')
        except ValueError:
            raise

        BV, BF = igl.bounding_box(self.vertices)

        self.x_limits = np.array([np.min(BV[:, 0]), np.max([BV[:, 0]])])
        self.y_limits = np.array([np.min(BV[:, 1]), np.max([BV[:, 1]])])
        self.z_limits = np.array([np.min(BV[:, 2]), np.max([BV[:, 2]])])

        print('Mesh Bounding Box:', self.x_limits,
              self.y_limits, self.z_limits)

        self.evaluated_grid = None

        self.calculate_signed_distances()

    @profile
    def calculate_signed_distances(self):

        print('Calculating Signed Distances...')

        S, _, _ = igl.signed_distance(
            self.designSpace.coordinate_list, self.vertices, self.faces)

        self.evaluated_grid = S.reshape(
            self.designSpace.resolution, self.designSpace.resolution, self.designSpace.resolution)

    def evaluatePoint(self, x, y, z):
        raise NotImplementedError
