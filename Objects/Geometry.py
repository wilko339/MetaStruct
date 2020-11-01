import numpy as np
import numexpr as ne
import skfmm
import math
import visvis as vv
import pymesh
import numpy.linalg as LA
from stl import mesh as msh
from stl import Mode
from skimage import measure


class Geometry:

    def __init__(self, designSpace):

        self.designSpace = designSpace

        if self.designSpace == None:

            raise ValueError('No specified design space.')

        self.x = 0
        self.y = 0
        self.z = 0

        self.transform = None

        self.mesh = []

        self.XX = self.designSpace.XX
        self.YY = self.designSpace.YY
        self.ZZ = self.designSpace.ZZ

        self.xStep = self.designSpace.xStep
        self.yStep = self.designSpace.yStep
        self.zStep = self.designSpace.zStep

        self.res = self.designSpace.res

        self.name = self.__class__.__name__

    def compareLims(self):

        if min(self.xLims) < self.designSpace.xLower or max(self.xLims) > self.designSpace.xUpper:

            print(
                '\n------------------------------------------------------------------\n')

            print('Warning: Design Space does not fully enclose shape in x dimension.\n')

            print('------------------------------------------------------------------\n')

        if min(self.yLims) < self.designSpace.yLower or max(self.yLims) > self.designSpace.yUpper:

            print(
                '\n------------------------------------------------------------------\n')

            print('Warning: Design Space does not fully enclose shape in y dimension.\n')

            print('------------------------------------------------------------------\n')

        if min(self.zLims) < self.designSpace.zLower or max(self.zLims) > self.designSpace.zUpper:

            print(
                '\n------------------------------------------------------------------\n')

            print('Warning: Design Space does not fully enclose shape in z dimension.\n')

            print('------------------------------------------------------------------\n')

    def setLims(self):

        pass

    def evaluatePoint(self, x, y, z):

        pass

    def evaluateDistance(self):

        if not hasattr(self, 'evaluatedGrid'):

            self.evaluateGrid()

        print(f'Evaluating distance field for {self.name}...')

        self.distanceGrid = skfmm.distance(
            self.evaluatedGrid, dx=self.designSpace.xStep)

    def translate(self, x, y, z):

        self.x += x
        self.y += y
        self.z += z
        self.setLims()

    def rotateAxis(self, ax='x', theta=45.):

        self.rotationAxis = ax
        theta = theta
        rads = theta * (math.pi/180)

        if ax == 'x':

            self.transform[:, 0] = [1, 0, 0]
            self.transform[:, 1] = [0, math.cos(
                rads), -math.sin(rads)]
            self.transform[:, 2] = [0, math.sin(
                rads), math.cos(rads)]

        if ax == 'y':

            self.transform[:, 0] = [math.cos(
                rads), 0, math.sin(rads)]
            self.transform[:, 1] = [0, 1, 0]
            self.transform[:, 2] = [-math.sin(
                rads), 0, math.cos(rads)]

        if ax == 'z':

            self.transform[:, 0] = [math.cos(
                rads), -math.sin(rads), 0]
            self.transform[:, 1] = [math.sin(
                rads), math.cos(rads), 0]
            self.transform[:, 2] = [0, 0, 1]

    def rotateCustomAxis(self, ax=[1, 1, 1], theta=45.):

        l = ax[0]
        m = ax[1]
        n = ax[2]
        theta = theta
        rads = theta * (math.pi/180)
        var = 1 - math.cos(theta)

        self.transform = [[l*l*var + math.cos(theta), m*l*var - n*math.sin(theta), n*l*var + m*math.sin(theta)],
                          [l*m*var + n*math.sin(theta), m*m*var +
                           math.cos(theta), n*m*var - l*math.sin(theta)],
                          [l*n*var - m*math.sin(theta), m*n*var + l *
                           math.sin(theta), n*n*var + math.cos(theta)]
                          ]

    def transformInputs(self, x, y, z):

        coords = np.array([x, y, z])

        coords = np.dot(coords.T, self.transform).T

        x = coords[0]
        y = coords[1]
        z = coords[2]

        return x, y, z

    def evaluateGrid(self):

        print(f'Evaluating grid points for {self.name}...')

        self.evaluatedGrid = self.evaluatePoint(self.XX, self.YY, self.ZZ)

    def findSurface(self, level=0):

        print(f'Extracting Isosurface (level = {level})...')

        try:

            self.verts, self.faces, self.normals, self.values = measure.marching_cubes(self.evaluatedGrid, level=level, spacing=(
                self.yStep, self.zStep, self.xStep), allow_degenerate=False)

            self.verts = np.fliplr(self.verts)

        except:

            raise ValueError(
                f'No isosurface found at specified level ({level})')

    def previewModel(self, clip=None, clipVal=0, flipClip=False, level=0):

        self.compareLims()

        if not hasattr(self, 'evaluatedGrid'):

            self.evaluateGrid()

        if clip != None:

            if clip == 'x':

                if flipClip == False:

                    self.evaluatedGrid = np.maximum(
                        self.evaluatedGrid, self.XX - clipVal)

                if flipClip == True:

                    self.evaluatedGrid = np.maximum(
                        self.evaluatedGrid, clipVal - self.XX)

            if clip == 'y':

                if flipClip == False:

                    self.evaluatedGrid = np.maximum(
                        self.evaluatedGrid, self.ZZ - clipVal)

                if flipClip == True:

                    self.evaluatedGrid = np.maximum(
                        self.evaluatedGrid, clipVal - self.ZZ)

            if clip == 'z':

                if flipClip == False:

                    self.evaluatedGrid = np.maximum(
                        self.evaluatedGrid, self.YY - clipVal)

                if flipClip == True:

                    self.evaluatedGrid = np.maximum(
                        self.evaluatedGrid, clipVal - self.YY)

        self.findSurface(level=level)

        vv.figure(1)

        shapeMesh = vv.mesh(self.verts, faces=self.faces, normals=self.normals)

        a = vv.gca()

        a.axis.xLabel = 'x'

        a.axis.yLabel = 'y'

        a.axis.zLabel = 'z'

        a.bgcolor = 'w'
        a.axis.axisColor = 'k'

        vv.use().Run()

    def meshClean(self, mesh):

        out_mesh = mesh

        print('Detecting Self Intersections...')

        self_intersections = pymesh.detect_self_intersection(out_mesh).shape[0]

        if self_intersections > 0:

            print(f'{self_intersections} detected, fixing...')

            out_mesh = pymesh.resolve_self_intersection(out_mesh)

            self_intersections = pymesh.detect_self_intersection(
                out_mesh).shape[0]

            print(f'{self_intersections} self intersections remaining in mesh.')

        out_mesh, info = pymesh.remove_isolated_vertices(out_mesh)

        verts_removed = info['num_vertex_removed']

        print(f'{verts_removed} isolated vertices removed...')

        print('Detecting Duplicate Vertices...')

        out_mesh, info = pymesh.remove_duplicated_vertices(out_mesh)

        merged_vertices = info['num_vertex_merged']

        print(f'{merged_vertices} merged vertices removed...')

        print('Detecting short edges...')

        out_mesh, info = pymesh.collapse_short_edges(out_mesh)

        collapsed_edges = info['num_edge_collapsed']

        print(f'{collapsed_edges} short edged collapsed...')

        print('Removing Duplicate Faces...')

        out_mesh, info = pymesh.remove_duplicated_faces(out_mesh)

        print('Removing obtuse triangles...')

        out_mesh, info = pymesh.remove_obtuse_triangles(out_mesh)

        split_tris = info['num_triangle_split']

        print(f'{split_tris} triangles split...')

        print('Removing degenerate triangles...')

        out_mesh, info = pymesh.remove_degenerated_triangles(out_mesh)

        return out_mesh

    def fix_mesh(self, mesh, detail="normal"):
        bbox_min, bbox_max = mesh.bbox
        diag_len = LA.norm(bbox_max - bbox_min)
        if detail == "normal":
            target_len = diag_len * 5e-3
        elif detail == "high":
            target_len = diag_len * 2.5e-3
        elif detail == "low":
            target_len = diag_len * 2e-2
        print("Target resolution: {} mm".format(target_len))

        count = 0
        mesh, __ = pymesh.remove_degenerated_triangles(mesh, 100)
        mesh, __ = pymesh.split_long_edges(mesh, target_len)
        num_vertices = mesh.num_vertices
        while True:
            mesh, __ = pymesh.collapse_short_edges(mesh, 1e-6)
            mesh, __ = pymesh.collapse_short_edges(mesh, target_len,
                                                   preserve_feature=True)
            mesh, __ = pymesh.remove_obtuse_triangles(mesh, 150.0, 100)
            if mesh.num_vertices == num_vertices:
                break

            num_vertices = mesh.num_vertices
            print("Number of Vertices: {}".format(num_vertices))
            count += 1
            if count > 10:
                break

        mesh = pymesh.resolve_self_intersection(mesh)
        mesh, __ = pymesh.remove_duplicated_faces(mesh)
        mesh = pymesh.compute_outer_hull(mesh)
        mesh, __ = pymesh.remove_duplicated_faces(mesh)
        mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5)
        mesh, __ = pymesh.remove_isolated_vertices(mesh)

        return mesh

    def saveMesh(self, filename=None, fileFormat='obj', quality='normal', package='numpy-stl'):

        res = self.designSpace.res
        self.quality = quality

        formats = {'obj': '.obj',
                   'stl': '.stl',
                   '.stl': '.stl',
                   '.obj': '.obj'}

        packages = ['pymesh', 'numpy-stl']

        if package not in packages:

            raise ValueError('Unrecognised mesh package defined.')

        if fileFormat not in formats:

            raise ValueError(f'"{fileFormat}" is not a supported file format.')

        if filename == None:

            self.filename = self.name + formats[fileFormat]

        if filename is not None:

            self.filename = filename + formats[fileFormat]

        if not hasattr(self, 'evaluatedGrid'):

            print('Evaluating Sample Points...')

            arr = self.evaluateGrid()

        print('Executing Marching Cubes Algorithm...')

        self.findSurface()

        print('Generating Mesh...')

        if package == 'pymesh':

            self.mesh = pymesh.meshio.form_mesh(self.verts, self.faces)

            self.mesh = self.fix_mesh(self.mesh, detail=self.quality)

            print(f'Exporting "{self.filename}" mesh file...\n')

            pymesh.save_mesh(self.filename, self.mesh, ascii=True)

            try:
                f = open(filename)
                f.close()
            except:
                FileNotFoundError(f'Cannot find "{self.filename}" in folder.')

            print(f'"{self.filename}" successfully exported.\n')

        if package == 'numpy-stl':

            self.mesh = msh.Mesh(
                np.zeros(self.faces.shape[0], dtype=msh.Mesh.dtype))

            self.verts = np.fliplr(self.verts)

            for i, f in enumerate(self.faces):
                for j in range(3):
                    self.mesh.vectors[i][j] = self.verts[f[j], :]

            self.mesh.save(f'{self.filename}', mode=Mode.ASCII)

            try:
                f = open(filename)
                f.close()
            except:
                FileNotFoundError(f'Cannot find "{self.filename}" in folder.')

            print(f'"{self.filename}" successfully exported.\n')

    def wireLattice(self):

        pass

    def convertToCylindrical(self):

        XX = self.XX
        YY = self.YY
        ZZ = self.ZZ

        r = ne.evaluate('sqrt(XX**2 + YY**2)')
        az = ne.evaluate('arctan2(YY, XX)')

        self.XX = r
        self.YY = az

        self.evaluatedGrid = self.evaluatePoint(self.XX, self.YY, self.ZZ)

    def convertToSpherical(self):

        XX = self.XX
        YY = self.YY
        ZZ = self.ZZ

        self.XX = ne.evaluate('sqrt(XX**2 + YY**2 + ZZ**2)')
        self.YY = ne.evaluate('arctan2(sqrt(XX**2 + YY**2),ZZ)')
        self.ZZ = ne.evaluate('arctan2(YY,XX)')

        self.evaluatedGrid = self.evaluatePoint(self.XX, self.YY, self.ZZ)
