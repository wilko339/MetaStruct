from Objects.Shapes.Shape import Shape
import numpy as np
import igl


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

        self.xLims = np.array([np.min(BV[:, 0]), np.max([BV[:, 0]])])
        self.yLims = np.array([np.min(BV[:, 1]), np.max([BV[:, 1]])])
        self.zLims = np.array([np.min(BV[:, 2]), np.max([BV[:, 2]])])

        print('Mesh Bounding Box:', self.xLims, self.yLims, self.zLims)

        self.evaluatedGrid = None

        self.calculate_signed_distances()

    def calculate_signed_distances(self):

        print('Calculating Signed Distances...')

        S, _, _ = igl.signed_distance(
            self.designSpace.coordinate_list, self.vertices, self.faces)

        self.evaluatedGrid = S.reshape(
            self.designSpace.res, self.designSpace.res, self.designSpace.res)

    def evaluatePoint(self, x, y, z):
        raise NotImplementedError
