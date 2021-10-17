import igl
import numexpr as ne
import numpy as np
from scipy.spatial.transform import Rotation as R
from skimage import measure

from MetaStruct.Functions.Remap import remap


class Geometry:

    def __init__(self, design_space):

        self.design_space = design_space

        if self.design_space is None:
            raise ValueError('No specified design space.')

        self.x = 0
        self.y = 0
        self.z = 0

        self.vertices = self.faces = None

        self.x_grid = self.design_space.x_grid
        self.y_grid = self.design_space.y_grid
        self.z_grid = self.design_space.z_grid

        self.x_step = self.design_space.x_step
        self.y_step = self.design_space.y_step
        self.z_step = self.design_space.z_step

        self.name = self.__class__.__name__

        self.x_limits = self.y_limits = self.z_limits = None
        self.evaluated_grid = self.evaluated_distance = None
        self.filename = None

    def compare_limits(self):

        if min(self.x_limits) < self.design_space.x_lower or max(self.x_limits) > self.design_space.x_upper:
            print(
                '\n------------------------------------------------------------------\n')

            print('Warning: Design Space does not fully enclose shape in x dimension.\n')

            print('------------------------------------------------------------------\n')

        if min(self.y_limits) < self.design_space.y_lower or max(self.y_limits) > self.design_space.y_upper:
            print(
                '\n------------------------------------------------------------------\n')

            print('Warning: Design Space does not fully enclose shape in y dimension.\n')

            print('------------------------------------------------------------------\n')

        if min(self.z_limits) < self.design_space.z_lower or max(self.z_limits) > self.design_space.z_upper:
            print(
                '\n------------------------------------------------------------------\n')

            print('Warning: Design Space does not fully enclose shape in z dimension.\n')

            print('------------------------------------------------------------------\n')

    def set_limits(self):

        pass

    def evaluate_point(self, x, y, z):

        pass

    def translate(self, x, y, z):

        self.x += x
        self.y += y
        self.z += z
        self.set_limits()

    def evaluate_grid(self, verbose=True, gradients=False):
        if verbose is True:
            print(f'Evaluating grid points for {self.name}...')

        self.evaluated_grid = np.array(
            self.evaluate_point(self.x_grid, self.y_grid, self.z_grid))
        if gradients is True:
            self.gradient_grid = np.gradient(
                self.evaluated_grid, self.design_space.resolution)

    def find_surface(self, level=0):

        print(f'Extracting Isosurface (level = {level})...')

        if self.evaluated_grid is None:
            self.evaluate_grid()

        try:

            self.vertices, self.faces, self.normals, self.values = measure.marching_cubes(self.evaluated_grid, level=level,
                                                                                          spacing=(
                                                                                           self.x_step, self.y_step,
                                                                                           self.z_step),
                                                                                          allow_degenerate=False)

        except ValueError:
            print(f'No isosurface found at specified level ({level})')
            raise

    def preview_model(self, clip=None, clip_value=0, flip_clip=False, mode='surface', level=0, rgb=(22, 94, 111)):

        import mayavi.mlab as ml

        assert mode in [
            'volume', 'surface'], 'Invalid mode selected, use either "volume" or "surface".'

        self.compare_limits()

        if self.evaluated_grid is None:
            self.evaluate_grid()

        if clip is not None:

            if clip == 'x':

                if not flip_clip:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, self.x_grid - clip_value)

                if flip_clip:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, clip_value - self.x_grid)

            if clip == 'y':

                if not flip_clip:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, self.z_grid - clip_value)

                if flip_clip:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, clip_value - self.z_grid)

            if clip == 'z':

                if not flip_clip:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, self.y_grid - clip_value)

                if flip_clip:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, clip_value - self.y_grid)

        # ml.figure(bgcolor=(0, 0, 0))

        if mode == 'volume':
            scalar_field = ml.pipeline.scalar_field(
                self.evaluated_grid)

            scalar_field.spacing = [self.x_step, self.y_step, self.z_step]

            ml.pipeline.volume(scalar_field)

        if mode == 'surface':

            if self.vertices is None or self.faces is None:
                self.find_surface(level=level)

            ml.triangular_mesh(
                self.vertices[:, 0], self.vertices[:, 1], self.vertices[:, 2], self.faces, color=tuple(c / 255 for c in rgb))

        ml.show()

    def decimate_mesh(self, factor=0.8):
        if self.vertices is None or self.faces is None:
            raise ValueError('No mesh, please use find_surface()')

        assert (1 > factor > 0), 'Factor must be between 0 and 1'

        target = round(len(self.faces) * factor)

        print('Decimating mesh...')

        success, self.vertices, self.faces, _, _ = igl.qslim(
            self.vertices, self.faces, target)

        assert len(self.faces) > 0, "QSlim failure, input mesh may be too large."

        c = igl.orientable_patches(self.faces)

        self.faces, _ = igl.orient_outward(self.vertices, self.faces, c[0])

        if success:
            print('Mesh decimated')
        if not success:
            print('Decimation did not reach target factor')

    def subdivide_mesh(self, divs=1):
        if self.vertices is None or self.faces is None:
            raise ValueError('No mesh, please use find_surface()')

        print('Subdividing mesh...')

        self.vertices, self.faces = igl.loop(self.vertices, self.faces, divs)

    def smooth_mesh(self, iterations=3, factor=0.25):

        if self.vertices is None or self.faces is None:
            raise ValueError('No mesh, please use find_surface()')

        print('Smoothing mesh...')

        for iteration in range(iterations):
            print(f'Iteration {iteration}...')
            self.subdivide_mesh()
            self.decimate_mesh(factor)
        print('Finished smoothing')

    def save_mesh(self, filename: str = None, file_format: str = 'stl') -> None:

        formats = {'obj': '.obj',
                   'stl': '.stl',
                   '.stl': '.stl',
                   '.obj': '.obj'}

        if file_format not in formats:
            raise ValueError(
                f'"{file_format}" is not a supported file format.')

        if filename is None:
            self.filename = self.name + formats[file_format]

        if filename is not None:
            self.filename = filename + formats[file_format]

        if self.faces is None or self.vertices is None:
            print('Executing Marching Cubes Algorithm...')
            self.find_surface()

        print('Saving Mesh...')

        igl.write_triangle_mesh(self.filename, self.vertices, self.faces)

        try:
            f = open(self.filename)
            f.close()
        except FileNotFoundError:
            print(f'Cannot find "{self.filename}" in folder.')
            raise

        print(f'"{self.filename}" successfully exported.')

    def convert_to_cylindrical(self):

        x_grid = self.x_grid
        y_grid = self.y_grid
        z_grid = self.z_grid

        r = ne.evaluate('sqrt(x_grid**2 + y_grid**2)')
        az = ne.evaluate('arctan2(y_grid, x_grid)')

        self.x_grid = r
        self.y_grid = az

        self.evaluated_grid = self.evaluate_point(
            self.x_grid, self.y_grid, self.z_grid)

    def convert_to_spherical(self):

        x_grid = self.x_grid
        y_grid = self.y_grid
        z_grid = self.z_grid

        self.x_grid = ne.evaluate('sqrt(x_grid**2 + y_grid**2 + z_grid**2)')
        self.y_grid = ne.evaluate(
            'arctan2(sqrt(x_grid**2 + y_grid**2),z_grid)')
        self.z_grid = ne.evaluate('arctan2(y_grid,x_grid)')

        self.evaluated_grid = self.evaluate_point(
            self.x_grid, self.y_grid, self.z_grid)

    def transform_test(self, fac=10):

        pi = np.pi
        x = remap(self.x_grid)
        y = remap(self.y_grid)
        z = remap(self.z_grid)
        k = fac

        r = R.from_quat([1, -1, 1, 1])

        self.x_grid = r.apply(x)

        self.evaluated_grid = self.evaluate_point(
            self.x_grid, self.y_grid, self.z_grid)

    def pringle(self, pringle_factor=0.1):

        x = self.x_grid
        y = self.y_grid
        z = self.z_grid
        pi = np.pi
        fac = pringle_factor

        self.z_grid = ne.evaluate('z + 0.1*(x**2 - y**2)')

        self.evaluated_grid = self.evaluate_point(
            self.x_grid, self.y_grid, self.z_grid)
