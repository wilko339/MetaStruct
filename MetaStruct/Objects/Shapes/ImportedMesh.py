from MetaStruct.Objects.Shapes.Shape import Shape
import numpy as np
import igl
import cProfile
import pstats
import io

from pathlib import Path

MESHES_FOLDER_NAME = 'meshes'
SAVED_MESHES_FOLDER = Path(
    str(Path(__file__).parent.parent.parent) + f'/{MESHES_FOLDER_NAME}')
print(SAVED_MESHES_FOLDER)


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
    def __init__(self, designSpace, filepath, save_field=True):

        working_dir = Path.cwd()

        self.save_field = save_field
        self.filepath = working_dir / MESHES_FOLDER_NAME / filepath

        super().__init__(designSpace, x=0, y=0, z=0)

        files = [f.stem for f in SAVED_MESHES_FOLDER.iterdir()
                 if f.is_file()]

        if self.filepath.stem in files:
            self.evaluated_grid = np.load(
                f'{self.filepath.with_suffix(".npy")}')

        try:
            self.vertices, self.faces = igl.read_triangle_mesh(filepath)
            print('Mesh Loaded')
        except ValueError:
            raise

        BV, _ = igl.bounding_box(self.vertices)

        self.x_limits = np.array([np.min(BV[:, 0]), np.max([BV[:, 0]])])
        self.y_limits = np.array([np.min(BV[:, 1]), np.max([BV[:, 1]])])
        self.z_limits = np.array([np.min(BV[:, 2]), np.max([BV[:, 2]])])

        print('Mesh Bounding Box:', self.x_limits,
              self.y_limits, self.z_limits)

        self.evaluated_grid = None

        self.calculate_signed_distances()

    @ profile
    def calculate_signed_distances(self):

        print('Calculating Signed Distances...')

        S, _, _ = igl.signed_distance(
            self.designSpace.coordinate_list, self.vertices, self.faces)

        self.evaluated_grid = S.reshape(
            self.designSpace.resolution, self.designSpace.resolution, self.designSpace.resolution)

        if self.save_field is True:

            filename = (SAVED_MESHES_FOLDER /
                        self.filepath.stem).with_suffix('.npy')

            try:
                print('Saving sdf...')
                np.save(filename, self.evaluated_grid)

            except:
                raise

    def evaluatePoint(self, x, y, z):
        raise NotImplementedError