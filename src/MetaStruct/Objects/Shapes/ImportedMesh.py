import igl
import numpy as np
from scipy.interpolate import RegularGridInterpolator

from MetaStruct.Objects.Shapes.Shape import Shape


class ImportedMesh(Shape):
    def __init__(self, design_space, filepath):
        super().__init__(design_space, x=0, y=0, z=0)

        try:
            vertices, faces = igl.read_triangle_mesh(filepath)
            print('Mesh Loaded')
        except ValueError:
            raise

        BV, _ = igl.bounding_box(vertices)

        self.x_limits = np.array([np.min(BV[:, 0]), np.max([BV[:, 0]])])
        self.y_limits = np.array([np.min(BV[:, 1]), np.max([BV[:, 1]])])
        self.z_limits = np.array([np.min(BV[:, 2]), np.max([BV[:, 2]])])

        print('Mesh Bounding Box:', self.x_limits,
              self.y_limits, self.z_limits)

        self.evaluated_grid = None

        self.calculate_signed_distances(vertices, faces)

    def calculate_signed_distances(self, vertices, faces):

        print('Calculating Signed Distances...')

        S, _, _ = igl.signed_distance(
            self.design_space.coordinate_list, vertices, faces)

        self.evaluated_grid = S.reshape(
            self.design_space.resolution, self.design_space.resolution, self.design_space.resolution)

    def evaluate_point(self, x, y, z):

        interp = RegularGridInterpolator((self.design_space.X, self.design_space.Y, self.design_space.Z),
                                         self.evaluated_grid)
        pts = np.empty(([len(x), 3]))
        pts[:, 0] = x
        pts[:, 1] = y
        pts[:, 2] = z

        return interp(pts)

