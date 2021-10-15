import cProfile
import io
import pstats
from pathlib import Path
from importlib import resources

import igl
import numpy as np

from MetaStruct.Objects.Shapes.Shape import Shape

class ImportedMesh(Shape):
    def __init__(self, design_space, filepath):

        working_dir = Path.cwd()

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
            self.designSpace.coordinate_list, vertices, faces)

        self.evaluated_grid = S.reshape(
            self.designSpace.resolution, self.designSpace.resolution, self.designSpace.resolution)

    def evaluatePoint(self, x, y, z):
        raise NotImplementedError
