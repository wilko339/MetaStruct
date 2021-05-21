
import numexpr as ne
import numpy as np
import numpy.linalg as LA
#import skfmm
import visvis as vv
from skimage import measure
from stl import Mode
from stl import mesh as msh
import igl
from wildmeshing import Tetrahedralizer


class Geometry:

    def __init__(self, design_space):

        self.design_space = design_space

        if self.design_space is None:
            raise ValueError('No specified design space.')

        self.x = 0
        self.y = 0
        self.z = 0

        self.mesh = None

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

    def evaluateDistance(self):

        if self.evaluated_grid is None:
            self.evaluate_grid()

        print(f'Evaluating distance field for {self.name}...')
        try:
            self.evaluated_distance = skfmm.distance(
                self.evaluated_grid, dx=np.array(
                    [self.design_space.x_step, self.design_space.y_step, self.design_space.z_step], dtype=np.double))
        except ValueError:
            print(self.evaluated_grid)
            raise

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

    def findSurface(self, level=0):

        print(f'Extracting Isosurface (level = {level})...')

        if self.evaluated_grid is None:
            self.evaluate_grid()

        try:

            self.verts, self.faces, self.normals, self.values = measure.marching_cubes(self.evaluated_grid, level=level,
                                                                                       spacing=(
                                                                                           self.x_step, self.y_step,
                                                                                           self.z_step),
                                                                                       allow_degenerate=False)

        except ValueError:
            print(f'No isosurface found at specified level ({level})')
            raise

    def save_tet_mesh(self, filename):

        if filename is None:
            self.filename = self.name + '.msh'

        if filename is not None:
            if filename[:-4] != '.msh':
                self.filename = filename + '.msh'

        tetra = Tetrahedralizer(max_its=10)

        tetra.set_mesh(self.verts, self.faces)

        tetra.tetrahedralize()

        tetra.save(self.filename)

    def previewModel(self, clip=None, clip_value=0, flip_clip=False, level=0):

        self.compare_limits()

        if self.evaluated_grid is None:
            self.evaluate_grid()

        if clip != None:

            if clip == 'x':

                if flip_clip == False:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, self.x_grid - clip_value)

                if flip_clip == True:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, clip_value - self.x_grid)

            if clip == 'y':

                if flip_clip == False:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, self.z_grid - clip_value)

                if flip_clip == True:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, clip_value - self.z_grid)

            if clip == 'z':

                if flip_clip == False:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, self.y_grid - clip_value)

                if flip_clip == True:
                    self.evaluated_grid = np.maximum(
                        self.evaluated_grid, clip_value - self.y_grid)

        if self.verts is None or self.faces is None:

            self.findSurface(level=level)

        vv.figure(1)

        vv.mesh(self.verts, faces=self.faces, normals=self.normals)

        a = vv.gca()

        a.axis.xLabel = 'y'

        a.axis.yLabel = 'z'

        a.axis.zLabel = 'x'

        a.bgcolor = 'w'
        a.axis.axisColor = 'k'

        vv.use().Run()

    def decimate_mesh(self, factor=0.8):
        if self.verts is None or self.faces is None:
            raise ValueError('No mesh, please use find_surface()')

        assert (factor < 1 and factor > 0), 'Factor must be between 0 and 1'

        target = round(len(self.faces)*factor)

        print('Decimating mesh...')

        success, self.verts, self.faces, _, _ = igl.qslim(
            self.verts, self.faces, target)

        c = igl.orientable_patches(self.faces)

        self.faces, I = igl.orient_outward(self.verts, self.faces, c[0])

        if success:
            print('Mesh decimated')
        if not success:
            print('Decimation did not reach target factor')

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

        if self.faces is None or self.verts is None:

            print('Executing Marching Cubes Algorithm...')
            self.findSurface()

        print('Saving Mesh...')

        igl.write_triangle_mesh(self.filename, self.verts, self.faces)

        try:
            f = open(self.filename)
            f.close()
        except FileNotFoundError:
            print(f'Cannot find "{self.filename}" in folder.')
            raise

        print(f'"{self.filename}" successfully exported.')

    def convertToCylindrical(self):

        XX = self.x_grid
        YY = self.y_grid
        ZZ = self.z_grid

        r = ne.evaluate('sqrt(x_grid**2 + y_grid**2)')
        az = ne.evaluate('arctan2(y_grid, x_grid)')

        self.x_grid = r
        self.y_grid = az

        self.evaluated_grid = self.evaluate_point(
            self.x_grid, self.y_grid, self.z_grid)

    def convertToSpherical(self):

        XX = self.x_grid
        YY = self.y_grid
        ZZ = self.z_grid

        self.x_grid = ne.evaluate('sqrt(x_grid**2 + y_grid**2 + z_grid**2)')
        self.y_grid = ne.evaluate(
            'arctan2(sqrt(x_grid**2 + y_grid**2),z_grid)')
        self.z_grid = ne.evaluate('arctan2(y_grid,x_grid)')

        self.evaluated_grid = self.evaluate_point(
            self.x_grid, self.y_grid, self.z_grid)
