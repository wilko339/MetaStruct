
import sys
import timeit
import time
import pstats
import os
import math
import io
import cProfile
import copy
import perlin3d
from visvis.functions import gca, isosurface
from stl import mesh as msh
from skimage import measure
from profilehooks import profile
from numpy import linalg as LA
import visvis as vv
import skimage
import skfmm
import pymesh
import numpy as np
import numexpr as ne


class DesignSpace:

    def __init__(self, res=100, xBounds=[-2.1, 2.1], yBounds=[-2.1, 2.1], zBounds=[-2.1, 2.1]):

        self.xBounds = xBounds
        self.yBounds = yBounds
        self.zBounds = zBounds

        self.res = res

        self.xLower = min(self.xBounds)
        self.xUpper = max(self.xBounds)
        self.yLower = min(self.yBounds)
        self.yUpper = max(self.yBounds)
        self.zLower = min(self.zBounds)
        self.zUpper = max(self.zBounds)

        offset = 0.1

        X = np.linspace(self.xLower - offset, self.xUpper + offset, res)
        Y = np.linspace(self.yLower - offset, self.yUpper + offset, res)
        Z = np.linspace(self.zLower - offset, self.zUpper + offset, res)

        self.xStep = (self.xUpper - self.xLower) / (res - 1)
        self.yStep = (self.yUpper - self.yLower) / (res - 1)
        self.zStep = (self.zUpper - self.zLower) / (res - 1)

        print('Generating Sample Grid in Design Space')

        self.YY, self.ZZ, self.XX = np.meshgrid(X, Y, Z)


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

    def evaluateDistance(self, x, y, z):

        pass

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
                self.xStep, self.yStep, self.zStep), allow_degenerate=False)

            self.verts = np.fliplr(self.verts)

        except:

            raise ValueError(
                f'No isosurface found at specified level ({level})')

    def previewModel(self, clip=None, clipVal=0, flipClip=False):

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

        self.findSurface()

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

    def saveMesh(self, filename=None, fileFormat='obj', quality='normal'):

        res = self.designSpace.res
        self.quality = quality

        formats = {'obj': '.obj',
                   'stl': '.stl',
                   '.stl': '.stl',
                   '.obj': '.obj'}

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

    def wireLattice(self):

        pass

    def convertToCylindrical(self):

        XX = self.XX
        YY = self.YY
        ZZ = self.ZZ

        r = ne.evaluate('sqrt(XX**2 + YY**2 + ZZ**2)')
        az = ne.evaluate('arctan(YY/XX)')
        inc = ne.evaluate('arccos(ZZ/r)')

        self.XX = ne.evaluate('sqrt(XX**2 + YY**2)')
        self.YY = ne.evaluate('arctan(YY/XX)')
        #self.ZZ = ne.evaluate('arccos(ZZ/r)')

        self.evaluatedGrid = self.evaluatePoint(self.XX, self.YY, self.ZZ)


class Shape(Geometry):

    morph = 'Shape'

    def __init__(self, designSpace, x=0, y=0, z=0):

        self.designSpace = designSpace

        super().__init__(self.designSpace)

        self.name = self.__class__.__name__

        self.x = self.paramCheck(x)
        self.y = self.paramCheck(y)
        self.z = self.paramCheck(z)

        self.transform = None

        self.XX = self.designSpace.XX
        self.YY = self.designSpace.YY
        self.ZZ = self.designSpace.ZZ

    def setLims(self):

        self.xLims = self.yLims = self.zLims = [0, 0]

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z})'

    def __str__(self):

        return f'{self.name} {self.morph}\nCentre(x, y, z): ({self.x}, {self.y}, {self.z})'

    def __add__(self, other):

        return Union(self, other)

    def __sub__(self, other):

        return Difference(self, other)

    def __truediv__(self, other):

        return Intersection(self, other)

    def __mul__(self, other):

        return Multiply(self, other)

    def paramCheck(self, n):

        try:

            float(n)
            return n

        except:
            raise ValueError(f'{n} != a number.')

    def evaluatePoint(self, x, y, z):
        pass


class Line(Shape):

    def __init__(self, x1, y1, z1, x2, y2, z2):

        self.p1 = np.array(([x1, y1, z1]))
        self.p2 = np.array(([x2, y2, z2]))
        self.l = LA.norm(self.p1 - self.p2)
        self.dir = self.p2 - self.p1

    def evaluatePoint(self, x, y, z):

        NotImplemented

    def evaluateDistance(self, x, y, z):

        NotImplemented


class Spheroid(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, xr=1, yr=2, zr=1, ):
        super().__init__(designSpace, x, y, z)

        self.xr = self.paramCheck(xr)
        self.yr = self.paramCheck(yr)
        self.zr = self.paramCheck(zr)

        self.xLims = np.array(
            [self.x - self.xr, self.x + self.xr])
        self.yLims = np.array(
            [self.y - self.yr, self.y + self.yr])
        self.zLims = np.array(
            [self.z - self.zr, self.z + self.zr])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.xr}, {self.yr}, {self.zr})'

    def __str__(self):

        return super().__str__() + f'\nRadii(xr, yr, zr): ({self.xr}, {self.yr}, {self.zr})'

    def evaluatePoint(self, x, y, z):

        if self.transform is not None:

            x, y, z = self.transformInputs(x, y, z)

        x0 = self.x
        y0 = self.y
        z0 = self.y
        xr = self.xr
        yr = self.yr
        zr = self.zr

        expr = '((x-x0)**2)/(xr**2) + ((y-y0)**2)/(yr**2) + ((z-z0)**2)/(zr**2) - 1'

        return ne.evaluate(expr)
        '''
        return ((np.square(x - self.x) / (self.xr)**2 +
                 np.square(y - self.y) / (self.yr)**2 +
                 np.square(z - self.z) / (self.zr)**2)) - 1
        '''


class Sphere(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, r=1):
        super().__init__(designSpace, x, y, z)

        self.r = self.paramCheck(r)

        self.setLims()
        # self.compareLims()

    def setLims(self):

        self.xLims = np.array(
            [self.x - self.r, self.x + self.r])
        self.yLims = np.array(
            [self.y - self.r, self.y + self.r])
        self.zLims = np.array(
            [self.z - self.r, self.z + self.r])

    def __repr__(self):

        return f'Sphere({self.x}, {self.y}, {self.z}, {self.r})'

    def evaluatePoint(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z
        r = self.r

        expr = '(x-x0)**2 + (y-y0)**2 + (z-z0)**2 - r**2'

        arr = ne.evaluate(expr)

        return arr

        '''
        return np.square(x - self.x) + np.square(y - self.y) + \
            np.square(z - self.z) - (self.r)** 2
        '''

    def evaluateDistance(self, x, y, z):
        '''
        return np.sqrt(np.square(x - self.x) + np.square(y - self.y) + \
            np.square(z-self.z)) - self.r
        '''

        x0 = self.x
        y0 = self.y
        z0 = self.z
        r = self.r

        expr = 'sqrt((x-x0)**2 + (y-y0)**2 + (y-y0)**2) + r'

        return ne.evaluate(expr)


class HollowSphere(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, r=1, t=0.3):

        self.designSpace = designSpace

        super().__init__(self.designSpace, x, y, z)

        self.r = self.paramCheck(r)
        self.t = self.paramCheck(t)
        self.setLims()

    def setLims(self):

        self.xLims = np.array(
            [self.x - self.r, self.x + self.r])
        self.yLims = np.array(
            [self.y - self.r, self.y + self.r])
        self.zLims = np.array(
            [self.z - self.r, self.z + self.r])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.r}, {self.t})'

    def __str__(self):

        return super().__str__() + f'\nRadius: {self.r}\nWall Thickness: {self.t}'

    def evaluatePoint(self, x, y, z):

        ball = Sphere(self.designSpace, self.x, self.y, self.z, self.r) - \
            Sphere(self.designSpace, self.x, self.y, self.z, self.r -
                   self.t)

        return ball.evaluatePoint(x, y, z)


class Cube(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, dim=1):
        super().__init__(designSpace, x, y, z)

        self.dim = self.paramCheck(dim)

        self.setLims()

    def setLims(self):

        self.xLims = np.array(
            [self.x - self.dim, self.x + self.dim])
        self.yLims = np.array(
            [self.y - self.dim, self.y + self.dim])
        self.zLims = np.array(
            [self.z - self.dim, self.z + self.dim])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.dim})'

    def __str__(self):

        return super().__str__() + f'\nCube Radius: {self.dim}'

    def evaluatePoint(self, x, y, z):

        if self.transform is not None:

            x, y, z = self.transformInputs(x, y, z)

        '''
        arr = [np.square(x - self.x) - (self.dim)**2, np.square(y - self.y) - (self.dim)**2,
               np.square(z - self.z) - (self.dim)**2]

        return np.maximum(np.maximum(arr[0], arr[1]), arr[2])
        '''

        x0 = self.x
        y0 = self.y
        z0 = self.z
        dim = self.dim

        arr1 = ne.evaluate('(x-x0)**2 - dim**2')
        arr2 = ne.evaluate('(y-y0)**2 - dim**2')
        arr3 = ne.evaluate('(z-z0)**2 - dim**2')

        max1 = ne.evaluate('where(arr1>arr2, arr1, arr2)')

        return ne.evaluate('where(max1>arr3, max1, arr3)')

    def evaluateDistance(self, x, y, z):

        # p = np.array(([x, y, z]))

        xmax = max(self.xLims)
        ymax = max(self.yLims)
        zmax = max(self.zLims)

        shape = np.shape(x)

        xmax = np.full(shape, xmax)
        ymax = np.full(shape, ymax)
        zmax = np.full(shape, zmax)

        b = np.array(([xmax, ymax, zmax]))

        q = np.absolute([x, y, z]) - b

        return LA.norm(np.maximum(q, 0)) + \
            np.minimum(np.maximum(q[0], np.maximum(q[1], q[2])), 0)


class HollowCube(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, dim=1, t=0.3):
        super().__init__(designSpace, x, y, z)

        self.dim = self.paramCheck(dim)
        self.t = self.paramCheck(t)
        self.setLims()

    def setLims(self):

        self.xLims = np.array(
            [self.x - self.dim, self.x + self.dim])
        self.yLims = np.array(
            [self.y - self.dim, self.y + self.dim])
        self.zLims = np.array(
            [self.z - self.dim, self.z + self.dim])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.dim}, {self.t})'

    def __str__(self):

        return super().__str__() + f'\nCube Radius: {self.dim}\nWall Thickness: {self.t}'

    def evaluatePoint(self, x, y, z):

        box = Cube(self.designSpace, self.x, self.y, self.z, self.dim) - \
            Cube(self.designSpace, self.x, self.y, self.z, self.dim - self.t)

        return box.evaluatePoint(x, y, z)


class Torus(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, r1=1, r2=0.5):
        super().__init__(designSpace, x, y, z)

        self.x = x
        self.y = y
        self.z = z
        self.r1 = r1
        self.r2 = r2

        self.setLims()

    def setLims(self):

        self.xLims = np.array(
            [self.x - self.r1 - self.r2, self.x + self.r1 + self.r2])
        self.yLims = np.array(
            [self.y - self.r1 - self.r2, self.y + self.r1 + self.r2])
        self.zLims = np.array(
            [self.z - self.r2, self.z + self.r2])

    def evaluatePoint(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z
        r1 = self.r1
        r2 = self.r2

        expr = '(sqrt((x-x0)**2 + (y-y0)**2) - r1)**2 + (z-z0)**2 - r2**2'

        return ne.evaluate(expr)
        '''
        return np.square(np.sqrt(np.square(x) + np.square(y)) - self.r1) + \
            np.square(z) - self.r2**2
        '''


class Cuboid(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, xd=1, yd=1.5, zd=1):
        super().__init__(designSpace, x, y, z)

        self.xd = self.paramCheck(xd)
        self.yd = self.paramCheck(yd)
        self.zd = self.paramCheck(zd)

        self.xLims = np.array(
            [self.x - self.xd, self.x + self.xd])
        self.yLims = np.array(
            [self.y - self.yd, self.y + self.yd])
        self.zLims = np.array(
            [self.z - self.zd, self.z + self.zd])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.xd}, {self.yd}, {self.zd})'

    def __str__(self):

        return super().__str__() + f'\nDimensions(x, y, z): ({self.xd}, {self.yd}, {self.zd})'

    def evaluatePoint(self, x, y, z):
        '''
        arr = [np.square(x - self.x) - (self.xd)**2, np.square(y - self.y) -
               (self.yd)**2, np.square(z - self.z) - (self.zd)**2]

        return np.maximum(np.maximum(arr[0], arr[1]), arr[2])
        '''

        x0 = self.x
        y0 = self.y
        z0 = self.z
        xd = self.xd
        yd = self.yd
        zd = self.zd

        arr1 = ne.evaluate('(x-x0)**2 - xd**2')
        arr2 = ne.evaluate('(y-y0)**2 - yd**2')
        arr3 = ne.evaluate('(z-z0)**2 - zd**2')

        max1 = ne.evaluate('where(arr1>arr2, arr1, arr2)')

        return ne.evaluate('where(max1>arr3, max1, arr3)')

    def evaluateDistance(self, x, y, z):

        p = np.array(([x, y, z]))

        xmax = max(self.xLims)
        ymax = max(self.yLims)
        zmax = max(self.zLims)

        b = np.array(([xmax, ymax, zmax]))

        q = np.absolute(p) - b

        return LA.norm(np.maximum(q, 0)) + \
            np.minimum(np.maximum(q[0], np.maximum(q[1], q[2])), 0)


class Cylinder(Shape):

    def __init__(self, designSpace, x=0, y=0, z=0, r1=1, r2=1, l=1, ax='z'):
        super().__init__(designSpace, x, y, z)

        self.r1 = self.paramCheck(r1)
        self.r2 = self.paramCheck(r2)
        self.l = self.paramCheck(l)
        self.ax = ax

        if self.ax == 'z':

            self.xLims = np.array(
                [self.x - self.r1, self.x + self.r1])
            self.yLims = np.array(
                [self.y - self.r2, self.y + self.r2])
            self.zLims = np.array(
                [self.z - self.l, self.z + self.l])

        if self.ax == 'x':

            self.xLims = np.array(
                [self.x - self.l, self.x + self.l])
            self.yLims = np.array(
                [self.y - self.r1, self.y + self.r1])
            self.zLims = np.array(
                [self.z - self.r2, self.z + self.r2])

        if self.ax == 'y':

            self.xLims = np.array(
                [self.x - self.r1, self.x + self.r1])
            self.yLims = np.array(
                [self.y - self.l, self.y + self.l])
            self.zLims = np.array(
                [self.z - self.r2, self.z + self.r2])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.r1}, {self.r2}, {self.l}, {self.ax})'

    def __str__(self):

        string = super().__str__() + \
            f'\nAxis: {self.ax}' + \
            f'\nLength: {self.l}'

        if self.ax == 'z':

            return string + f'\nRadii(x, y): ({self.r1}, {self.r2})'

        if self.ax == 'x':

            return string + f'\nRadii(y, z): ({self.r1}, {self.r2})'

        if self.ax == 'y':

            return string + f'\nRadii(x, z): ({self.r1}, {self.r2})'

    def evaluatePoint(self, x, y, z):

        if self.ax == 'z':

            arr = [np.square(x - self.x)/self.r1**2 + np.square(y - self.y) /
                   self.r2**2 - 1, np.square(z - self.z) - self.l**2]

            return np.maximum(arr[0], arr[1])

        if self.ax == 'x':

            arr = [np.square(y - self.y)/self.r1**2 + np.square(z - self.z) /
                   self.r2**2 - 1, np.square(x - self.x) - self.l**2]

            return np.maximum(arr[0], arr[1])

        if self.ax == 'y':

            arr = [np.square(x - self.x)/self.r1**2 + np.square(z - self.z) /
                   self.r2**2 - 1, np.square(y - self.y) - self.l**2]

            return np.maximum(arr[0], arr[1])

    # def evaluateDistance(self, x, y, z):

        # if self.ax == 'z':

            # return np.maximum(np.square(x) + np.square(y) - self.r)


class Boolean(Geometry):

    def __init__(self, shape1, shape2):

        if shape1.designSpace.XX is not shape2.designSpace.XX:
            if shape1.designSpace.YY is not shape2.designSpace.YY:
                if shape1.designSpace.ZZ is not shape2.designSpace.ZZ:
                    raise ValueError(
                        f'{shape1.name} and {shape2.name} are defined in different design spaces.')

        self.designSpace = shape1.designSpace

        self.XX = self.designSpace.XX
        self.YY = self.designSpace.YY
        self.ZZ = self.designSpace.ZZ

        self.xStep = self.designSpace.xStep
        self.yStep = self.designSpace.yStep
        self.zStep = self.designSpace.zStep

        if shape1.morph == 'Lattice' and shape2.morph != 'Lattice':

            raise TypeError('Please enter Lattice Object as 2nd Argument.')

        self.morph = 'Shape'

        self.transform = np.eye(3)

        self.shape1 = shape1
        self.shape2 = shape2
        self.shapes = [shape1, shape2]
        self.setLims()

        self.x = (shape1.x + shape2.x) / 2
        self.y = (shape1.z + shape2.y) / 2
        self.z = (shape1.x + shape2.z) / 2

        self.name = shape1.name + '_' + shape2.name
        '''
        for shape in self.shapes:

            if not hasattr(shape, 'evaluatedGrid'):

                shape.evaluateGrid()'''

    def setLims(self):

        self.xLims = [0., 0.]
        self.yLims = [0., 0.]
        self.zLims = [0., 0.]

        self.shapesXmins = []
        self.shapesXmaxs = []
        self.shapesYmins = []
        self.shapesYmaxs = []
        self.shapesZmins = []
        self.shapesZmaxs = []

        if self.shape2.morph != 'Lattice':

            for shape in self.shapes:

                self.shapesXmins.append(shape.xLims[0])
                self.shapesXmaxs.append(shape.xLims[1])
                self.shapesYmins.append(shape.yLims[0])
                self.shapesYmaxs.append(shape.yLims[1])
                self.shapesZmins.append(shape.zLims[0])
                self.shapesZmaxs.append(shape.zLims[1])

            self.xLims[0] = min(self.shapesXmins)
            self.xLims[1] = max(self.shapesXmaxs)
            self.yLims[0] = min(self.shapesYmins)
            self.yLims[1] = max(self.shapesYmaxs)
            self.zLims[0] = min(self.shapesZmins)
            self.zLims[1] = max(self.shapesZmaxs)

        if self.shape2.morph == 'Lattice':

            self.morph == 'Lattice'

            self.xLims = self.shape1.xLims
            self.yLims = self.shape1.yLims
            self.zLims = self.shape1.zLims

    def __repr__(self):

        return f'{self.__class__.__name__}({repr(self.shape1)}, {repr(self.shape2)})'

    def __add__(self, other):

        return Union(self, other)

    def __sub__(self, other):

        return Difference(self, other)

    def __truediv__(self, other):

        return Intersection(self, other)

    def checkShapeGrids(self):

        for shape in self.shapes:

            if not hasattr(shape, 'evaluatedGrid'):

                shape.evaluateGrid()

    def translate(self, x, y, z):

        for shape in self.shapes:

            shape.translate(x, y, z)

        self.setLims()


class Union(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        return np.minimum(self.shape1.evaluatePoint(x, y, z), self.shape2.evaluatePoint(x, y, z))

    @profile(immediate=True)
    def evaluateGrid(self):

        s1 = self.shape1.evaluatedGrid
        s2 = self.shape2.evaluatedGrid

        self.evaluatedGrid = ne.evaluate('where(s1<s2, s1, s2)')


class SmoothUnion(Boolean):

    def __init__(self, shape1, shape2, blend=4):
        super().__init__(shape1, shape2)

        self.blend = blend

    def evaluatePoint(self, x, y, z):

        res = np.exp(-self.blend * self.shape1.evaluatePoint(x, y, z)) + \
            np.exp(-self.blend * self.shape2.evaluatePoint(x, y, z))

        return -np.log(np.maximum(0.0001, res)) / self.blend

    def evaluateGrid(self):

        for shape in self.shapes:

            if not hasattr(shape, 'evaluatedGrid'):

                shape.evaluateGrid()

        res = np.exp(-self.blend * self.shape1.evaluatedGrid) + \
            np.exp(-self.blend * self.shape2.evaluatedGrid)

        self.evaluatedGrid = -np.log(np.maximum(0.0001, res)) / self.blend


class Intersection(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        return np.maximum(self.shape1.evaluatePoint(x, y, z), self.shape2.evaluatePoint(x, y, z))

    def evaluateGrid(self):
        for shape in self.shapes:

            if not hasattr(shape, 'evaluatedGrid'):

                shape.evaluateGrid()

        self.evaluatedGrid = np.maximum(
            self.shape1.evaluatedGrid, self.shape2.evaluatedGrid)


class Difference(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        for shape in self.shapes:

            if not hasattr(shape, 'evaluatedGrid'):

                shape.evaluateGrid()

        g1 = self.shape1.evaluatedGrid
        g2 = -self.shape2.evaluatedGrid

        expr = 'where(g1>g2, g1, g2)'

        return ne.evaluate(expr)

        # return np.maximum(self.shape1.evaluatedGrid, -self.shape2.evaluatedGrid)


class Add(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        outputs = [self.shape1.evaluatedGrid, self.shape2.evaluatedGrid]

        return sum(outputs)

    def evaluateGrid(self):

        self.checkShapeGrids()

        g1 = self.shape1.evaluatedGrid
        g2 = self.shape2.evaluatedGrid

        expr = 'g1 + g2'

        self.evaluatedGrid = ne.evaluate(expr)


class Subtract(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        outputs = [self.shape1.evaluatedGrid, -self.shape2.evaluatedGrid]

        return sum(outputs)

    def evaluateGrid(self):

        self.checkShapeGrids()

        g1 = self.shape1.evaluatedGrid
        g2 = self.shape2.evaluatedGrid

        expr = 'g1 - g2'

        self.evaluatedGrid = ne.evaluate(expr)


class Multiply(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        outputs = [self.shape1.evaluatedGrid, self.shape2.evaluatedGrid]

        return outputs[0] * outputs[1]

    def evaluateGrid(self):

        self.checkShapeGrids()

        g1 = self.shape1.evaluatedGrid
        g2 = self.shape2.evaluatedGrid

        expr = 'g1 * g2'

        self.evaluatedGrid = ne.evaluate(expr)


class Divide(Boolean):

    def __init__(self, shape1, shape2):
        super().__init__(shape1, shape2)

    def evaluatePoint(self, x, y, z):

        outputs = [self.shape1.evaluatedGrid, self.shape2.evaluatedGrid]

        return outputs[0] / outputs[1]

    def evaluateGrid(self):

        self.checkShapeGrids()

        g1 = self.shape1.evaluatedGrid
        g2 = self.shape2.evaluatedGrid

        expr = 'g1 / g2'

        self.evaluatedGrid = ne.evaluate(expr)


class Blend(Boolean):

    def __init__(self, shape1, shape2, blend=0.5):

        super().__init__(shape1, shape2)

        self.blend = blend

    def evaluatePoint(self, x, y, z):

        return self.blend * self.shape1.evaluatePoint(x, y, z) + \
            (1 - self.blend) * self.shape2.evaluatePoint(x, y, z)

    def evaluateGrid(self):

        self.checkShapeGrids()

        g1 = self.shape1.evaluatedGrid
        g2 = self.shape2.evaluatedGrid
        b = self.blend

        expr = 'b * g1 + (1 - b) * g2'

        self.evaluatedGrid = ne.evaluate(expr)


class Lattice(Geometry):

    morph = 'Lattice'

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=0):
        super().__init__(designSpace)

        self.transform = None

        self.name = self.__class__.__name__

        self.x = self.paramCheck(x)
        self.y = self.paramCheck(y)
        self.z = self.paramCheck(z)

        self.nx = nx
        self.ny = ny
        self.nz = nz

        self.lx = lx
        self.ly = ly
        self.lz = lz

        self.t = t

        self.kx = 2 * math.pi * (self.nx / self.lx)
        self.ky = 2 * math.pi * (self.ny / self.ly)
        self.kz = 2 * math.pi * (self.nz / self.lz)

        self.xLims = np.array([-self.lx, self.lx])
        self.yLims = np.array([-self.ly, self.ly])
        self.zLims = np.array([-self.lz, self.lz])

    def __repr__(self):

        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z}, {self.nx}, {self.ny}, {self.nz}, {self.lx}, {self.ly}, {self.lz}, {self.t})'

    def __str__(self):

        return f'{self.name} {self.morph}\n' + \
            f'Centre(x, y, z): ({self.x}, {self.y}, {self.z})\n' + \
            f'Number of Unit Cells per Unit Length(x, y, z): ({self.nx}, {self.ny}, {self.nz})\n' + \
            f'Unit Cell Size (x, y, z): ({self.lx}, {self.ly}, {self.lz})\n' + \
            f't Value: {self.t}'

    def __add__(self, other):

        return Union(self, other)

    def __sub__(self, other):

        return Difference(self, other)

    def __truediv__(self, other):

        return Intersection(self, other)

    def changeZ(self, value):

        self.lx = value
        self.ly = value
        self.lz = value
        self.kx = 2 * math.pi * (self.nx / self.lx)
        self.ky = 2 * math.pi * (self.ny / self.ly)
        self.kz = 2 * math.pi * (self.nz / self.lz)
        self.xLims = np.array([-self.lx, self.lx])
        self.yLims = np.array([-self.ly, self.ly])
        self.zLims = np.array([-self.lz, self.lz])

    def paramCheck(self, n):

        try:

            float(n)
            return n

        except:
            raise ValueError(f'{n} is not a number.')

    def convertToCylindrical(self):

        XX = self.XX
        YY = self.YY
        ZZ = self.ZZ

        self.XX = ne.evaluate('sqrt(XX**2 + YY**2)')
        self.YY = ne.evaluate('arctan2(YY,XX)')

        self.evaluatedGrid = self.evaluatePoint(self.XX, self.YY, self.ZZ)

    def convertToSpherical(self):

        XX = self.XX
        YY = self.YY
        ZZ = self.ZZ

        r = ne.evaluate('sqrt(XX**2 + YY**2 + ZZ**2)')
        az = ne.evaluate('arctan2(YY,XX)')
        inc = ne.evaluate('arccos(ZZ/r)')

        self.XX = ne.evaluate('sqrt(XX**2 + YY**2 + ZZ**2)')
        self.YY = ne.evaluate('arctan2(sqrt(XX**2 + YY**2),ZZ)')
        self.ZZ = ne.evaluate('arctan2(YY,XX)')

        self.evaluatedGrid = self.evaluatePoint(self.XX, self.YY, self.ZZ)


class GyroidSurface(Lattice):
    """Gyroid Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=0):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, t)

    def evaluatePoint(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        x0 = self.x
        y0 = self.y
        z0 = self.z
        kx = self.kx
        ky = self.ky
        kz = self.kz
        t = self.t

        expr = 'sin(kx*(x-x0))*cos(ky*(y-y0)) + \
                sin(ky * (y - y0)) * cos(kz * (z - z0)) + \
                sin(kz*(z-z0))*cos(kx*(x-x0)) - t '

        return ne.evaluate(expr)


class DiamondSurface(Lattice):

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=0):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, t)

    def evaluatePoint(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z
        kx = self.kx
        ky = self.ky
        kz = self.kz
        t = self.t

        expr = 'sin(kx * (x - x0)) * sin(ky * (y - y0)) * sin(kz * (z - z0)) + \
                sin(kx * (x - x0)) * cos(ky * (y - y0)) * cos(kz * (z - z0)) + \
                cos(kx * (x - x0)) * sin(ky * (y - y0)) * cos(kz * (z - z0)) + \
                cos(kx * (x - x0)) * cos(ky * (y - y0)) * cos(kz * (z - z0)) - t'

        return ne.evaluate(expr)

        '''
        return np.sin(self.kx*(x-self.x))*np.sin(self.ky*(y-self.y))*np.sin(self.kz*(z-self.z)) + \
            np.sin(self.kx*(x-self.x))*np.cos(self.ky*(y-self.y))*np.cos(self.kz*(z-self.z)) + \
            np.cos(self.kx*(x-self.x))*np.sin(self.ky*(y-self.y))*np.cos(self.kz*(z - self.z)) + \
            np.cos(self.kx*(x-self.x))*np.cos(self.ky*(y-self.y)) * np.cos(self.kz*(z-self.z)) - \
            self.t
        '''


class PrimitiveSurface(Lattice):

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=0):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, t)

    def evaluatePoint(self, x, y, z):

        x0 = self.x
        y0 = self.y
        z0 = self.z
        kx = self.kx
        ky = self.ky
        kz = self.kz
        t = self.t

        expr = '-(cos(kx*(x-x0)) + \
                 cos(ky*(y-y0)) + \
                 cos(kz * (z - z0)) - t) '

        return ne.evaluate(expr)


class CompositeLatticeSurface(Geometry):

    def __init__(self, lat1, lat2, blendMatrix=0.5):

        if lat1.designSpace.XX is not lat2.designSpace.XX:
            if lat1.designSpace.YY is not lat2.designSpace.YY:
                if lat1.designSpace.ZZ is not lat2.designSpace.ZZ:
                    raise ValueError(
                        f'{shape1.name} and {shape2.name} are defined in different design spaces.')

        super().__init__(lat1.designSpace)
        self.designSpace = lat1.designSpace
        self.lat1 = lat1
        self.lat2 = lat2
        self.lattices = [lat1, lat2]

        self.xLims = np.array([-1, 1])
        self.yLims = np.array([-1, 1])
        self.zLims = np.array([-1, 1])
        self.name = f'{lat1.name}_{lat2.name}'
        self.morph = self.lat1.morph

        self.blendMatrix = blendMatrix

    def evaluatePoint(self, x, y, z):

        for lat in self.lattices:

            if not hasattr(lat, 'evaluatedGrid'):

                lat.evaluateGrid()

        blend = self.blendMatrix
        l1 = self.lat1.evaluatedGrid
        l2 = self.lat2.evaluatedGrid

        return ne.evaluate('blend * l1 + (1- blend) * l2')


class Gyroid(Lattice):
    """Gyroid Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=0.6):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, t)

        self.coordSys = 'car'

    def evaluatePoint(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        if self.coordSys == 'car':

            if self.transform is not None:

                x, y, z = self.transformInputs(x, y, z)

        if self.coordSys == 'cyl':

            r = np.sqrt(np.square(x) + np.square(y))
            theta = np.arctan(y/z)

            x = r * np.cos(theta)
            y = r * np.sin(theta)

        lattice = GyroidSurface(self.designSpace, self.x, self.y, self.z, self.nx,
                                self.ny, self.nz, self.lx, self.ly, self.lz, self.t) - \
            GyroidSurface(self.designSpace, self.x, self.y, self.z, self.nx, self.ny,
                          self.nz, self.lx, self.ly, self.lz, -self.t)

        for shape in lattice.shapes:

            shape.XX = self.XX
            shape.YY = self.YY
            shape.ZZ = self.ZZ

        return lattice.evaluatePoint(x, y, z)


class DoubleGyroidNetwork(Lattice):
    """Double Network Gyroid Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=1.2):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, t)

        self.coordSys = 'car'

    def evaluatePoint(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        if self.coordSys == 'car':

            if self.transform is not None:

                x, y, z = self.transformInputs(x, y, z)

        if self.coordSys == 'cyl':

            r = np.sqrt(np.square(x) + np.square(y))
            theta = np.arctan(y/z)

            x = r * np.cos(theta)
            y = r * np.sin(theta)

        lattice = GyroidSurface(self.designSpace, self.x, self.y, self.z, self.nx, self.ny, self.nz, self.lx, self.ly, self.lz, self.t) - \
            GyroidSurface(self.designSpace, self.x, self.y, self.z, self.nx, self.ny,
                          self.nz, self.lx, self.ly, self.lz, -self.t)

        return -lattice.evaluatePoint(x, y, z)


class GyroidNetwork(Lattice):
    """Network Gyroid Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=0.9):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, t)

        self.coordSys = 'car'

    def evaluatePoint(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        if self.coordSys == 'car':

            if self.transform is not None:

                x, y, z = self.transformInputs(x, y, z)

        if self.coordSys == 'cyl':

            r = np.sqrt(np.square(x) + np.square(y))
            theta = np.arctan(y/z)

            x = r * np.cos(theta)
            y = r * np.sin(theta)

        lattice = GyroidSurface(self.designSpace, self.x, self.y, self.z, self.nx,
                                self.ny, self.nz, self.lx, self.ly, self.lz, self.t)

        return -lattice.evaluatePoint(x, y, z)


class Diamond(Lattice):
    """Diamond Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=0.4):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, t)

    def evaluatePoint(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        lattice = DiamondSurface(self.designSpace, self.x, self.y, self.z, self.nx,
                                 self.ny, self.nz, self.lx, self.ly, self.lz, self.t) - \
            DiamondSurface(self.designSpace, self.x, self.y, self.z, self.nx, self.ny,
                           self.nz, self.lx, self.ly, self.lz, -self.t)

        return lattice.evaluatePoint(x, y, z)


class DiamondNetwork(Lattice):
    """Diamond Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=0.4):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, t)

    def evaluatePoint(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        lattice = DiamondSurface(self.designSpace, self.x, self.y, self.z, self.nx, self.ny, self.nz, self.lx, self.ly, self.lz, self.t) - \
            DiamondSurface(self.designSpace, self.x, self.y, self.z, self.nx, self.ny,
                           self.nz, self.lx, self.ly, self.lz, -self.t)

        return -lattice.evaluatePoint(x, y, z)


class Primitive(Lattice):
    """Primitive Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=0.6):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, t)

    def evaluatePoint(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        lattice = PrimitiveSurface(self.designSpace, self.x, self.y, self.z, self.nx,
                                   self.ny, self.nz, self.lx, self.ly, self.lz, -self.t) - \
            PrimitiveSurface(self.designSpace, self.x, self.y, self.z, self.nx, self.ny,
                             self.nz, self.lx, self.ly, self.lz, self.t)

        return lattice.evaluatePoint(x, y, z)


class PrimitiveNetwork(Lattice):
    """Primitive Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction."""

    def __init__(self, designSpace, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, t=0.4):
        super().__init__(designSpace, x, y, z, nx, ny, nz, lx, ly, lz, t)

    def evaluatePoint(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        lattice = PrimitiveSurface(self.designSpace,
                                   self.x, self.y, self.z, self.nx, self.ny, self.nz, self.lx, self.ly, self.lz, -self.t)

        return -lattice.evaluatePoint(x, y, z)


class Pattern(Shape):

    def __init__(self, shape, nx=3, ny=2, nz=2, xd=0.5, yd=0.5, zd=0.5):

        self.x = shape.x
        self.y = shape.y
        self.z = shape.z

        super().__init__(self.x, self.y, self.z)

        self.nx = nx
        self.ny = ny
        self.nz = nz

        self.xd = xd
        self.yd = yd
        self.zd = zd

        self.sourceShape = shape

        self.shape = shape

        self.setLims(self.sourceShape)

        self.createPattern()

    def createPattern(self):

        for it in range(self.nx):

            it += 1

            new_shape = copy.deepcopy(self.sourceShape)

            new_shape.translate(it*self.xd, 0, 0)

            self.shape += new_shape

        self.setLims(self.shape)

        for it in range(self.ny):

            it += 1

            new_shape = copy.deepcopy(self.sourceShape)

            new_shape.translate(0, it*self.yd, 0)

            self.shape += new_shape

        self.setLims(self.shape)

        for it in range(self.nz):

            it += 1

            new_shape = copy.deepcopy(self.sourceShape)

            new_shape.translate(0, 0, it*self.zd)

            self.shape += new_shape

        self.setLims(self.shape)

    def setLims(self, obj):

        self.xLims = obj.xLims
        self.yLims = obj.yLims
        self.zLims = obj.zLims

    def evaluatePoint(self, x, y, z):

        return self.shape.evaluatePoint(x, y, z)

    def translate(self, x, y, z):

        self.sourceShape.translate(x, y, z)

        self.setLims(self.sourceShape)

        self.__init__(self.sourceShape, self.nx, self.ny,
                      self.nz, self.xd, self.yd, self.zd)


class Noise(Geometry):

    def __init__(self, designSpace, shape, intensity=1.5):
        super().__init__(designSpace)

        self.shape = shape
        self.designSpace = designSpace
        self.intensity = 10000/intensity

        self.xLims = self.shape.xLims
        self.yLims = self.shape.yLims
        self.zLims = self.shape.zLims

    def evaluateGrid(self):

        grid = np.random.randint(
            100, size=self.designSpace.XX.shape)
        intensity = self.intensity

        self.noiseGrid = ne.evaluate('grid / intensity')

        if not hasattr(self.shape, 'evaluatedGrid'):

            self.shape.evaluateGrid()

        shapeGrid = self.shape.evaluatedGrid
        noiseGrid = self.noiseGrid

        self.evaluatedGrid = ne.evaluate('shapeGrid + noiseGrid')


class PerlinNoise(Geometry):

    def __init__(self, designSpace, shape, freq=(8, 8, 8)):
        super().__init__(designSpace)

        self.morph = 'Shape'

        self.shape = shape
        self.designSpace = designSpace

        self.xLims = self.shape.xLims
        self.yLims = self.shape.yLims
        self.zLims = self.shape.zLims

        self.freq = freq

    def evaluateGrid(self):

        print('Generating Perlin Noise...')
        self.evaluatedGrid = perlin3d.generate_perlin_noise_3d(
            self.designSpace.XX.shape, self.freq)

    def noiseShape(self):

        if not hasattr(self, 'evaluatedGrid'):

            self.evaluateGrid()

        if not hasattr(self.shape, 'evaluatedGrid'):

            self.shape.evaluateGrid()

        g1 = self.shape.evaluatedGrid
        g2 = self.evaluatedGrid

        expr = 'g1 + (g2 * 1.5)'

        self.evaluatedGrid = ne.evaluate(expr)

    def noiseLattice(self):

        if not hasattr(self, 'evaluatedGrid'):

            self.evaluateGrid()

        g1 = self.evaluatedGrid
        g2 = -(self.evaluatedGrid + 0.1)

        expr = 'where(g1>g2, g1, g2)'

        self.evaluatedGrid = ne.evaluate(expr)


def latticedSphereExample(outerRad=2, outerSkinThickness=0.1, innerRad=1, innerSkinThickness=0.1):

    ds = DesignSpace(res=300)

    outerSkin = HollowSphere(designSpace=ds, r=outerRad, t=outerSkinThickness)

    latticeSection = HollowSphere(r=outerRad-outerSkinThickness,
                                  t=outerRad - outerSkinThickness - innerRad,
                                  designSpace=ds) / Gyroid(designSpace=ds)

    innerSkin = HollowSphere(r=innerRad, t=innerSkinThickness, designSpace=ds)

    s1 = Union(outerSkin, Union(latticeSection, innerSkin))

    s1.previewModel(clip='x')


def wireLattice():

    vertices = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1],
    ])

    edges = np.array([
        [0, 3],
        [0, 4],
        [0, 6],
        [1, 2],
        [1, 4],
        [1, 5],
        [2, 6],
        [2, 7],
        [3, 5],
        [3, 7],
        [4, 7],
        [5, 6]
    ])

    wireNetwork = pymesh.wires.WireNetwork.create_from_data(vertices, edges)

    tiler = pymesh.Tiler(wireNetwork)
    boxMin = np.zeros(3)
    boxMax = np.ones(3) * 15.
    reps = [3, 3, 3]
    tiler.tile_with_guide_bbox(boxMin, boxMax, reps)

    tiledNetwork = tiler.wire_network

    inflator = pymesh.wires.Inflator(tiledNetwork)

    inflator.set_profile(8)

    inflator.set_refinement(2, "loop")

    inflator.inflate(0.5)

    tiledMesh = inflator.mesh

    pymesh.save_mesh('tiledMesh.obj', tiledMesh)


def latticeRefinementExample():

    ds = DesignSpace(res=300)

    cuboid = Cuboid(ds, xd=2, yd=2, zd=0.5)

    refinedLattice = Gyroid(ds, nx=2, ny=2, nz=2, t=0.8)

    refinedLattice.evaluateGrid()

    refinedLattice.evaluatedGrid

    sphere = Sphere(ds, r=1.5)

    sphere.evaluateGrid()

    sphere.evaluatedGrid = np.where(
        sphere.evaluatedGrid > 0, 0, sphere.evaluatedGrid)

    refinedLattice.evaluatedGrid -= sphere.evaluatedGrid / 6

    shape = cuboid / refinedLattice

    shape.evaluateGrid()

    shape.saveMesh('refinedGyroid', fileFormat='obj', quality='high')


def main():

    ds = DesignSpace(res=200)

    lat1 = Gyroid(ds)

    xx = lat1.XX

    pi = math.pi

    minXX = xx.min()
    maxXX = xx.max()

    xxNorm = ne.evaluate('(xx-minXX)/(maxXX-minXX)')

    lat1.nx = xxNorm * 1.2

    lat1.t = ne.evaluate('(xxNorm + 1)/3')

    lat1 = Cube(ds, dim=2) / lat1

    lat1.previewModel()


def profile(func):

    def inner(*args, **kwargs):

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

    return inner


if __name__ == '__main__':

    main()
