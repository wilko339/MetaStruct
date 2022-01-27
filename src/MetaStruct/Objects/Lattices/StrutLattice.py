import cProfile
import io
import pstats
import time

import numexpr as ne
import numpy as np
import scipy
from sklearn.neighbors import NearestNeighbors
import pandas as pd

from MetaStruct.Objects.Shapes.Line import Line, SimpleLine
from MetaStruct.Objects.Shapes.Shape import Shape

from line_profiler_pycharm import profile
from numba import njit, prange


INDEXES = {
    0: 'x',
    1: 'y',
    2: 'z'
}


def old_norm(vector):
    return np.linalg.norm(vector, axis=0)


@njit(parallel=True, fastmath=True)
def pa_numba(vec, line):
    out = np.empty_like(vec)
    for i in prange(3):
        out[i, :, :, :] = vec[i, :, :, :] - line[i]

    return out

@njit(fastmath=True)
def pa_ba_h_numba(pa, ba_h):
    out = np.empty([3, ba_h.shape[0], ba_h.shape[1], ba_h.shape[2]])
    for i in prange(3):
        for j in range(ba_h.shape[0]):
            for k in range(ba_h.shape[0]):
                for l in range(ba_h.shape[0]):
                    out[i, j, k, l] = pa


class UnitCell(Shape):
    def __init__(self, design_space):
        super().__init__(design_space)


class AxialCentric(UnitCell):
    def __init__(self, design_space, centre=None, r1=0.25, r2=0.25, r3=0.25, cell_size=1):
        if centre is None:
            centre = [0, 0, 0]
        self.centre = centre
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.cell_size = cell_size

        super().__init__(design_space)

        self.x_limits = [self.centre[0]-self.cell_size/2, self.centre[0]+self.cell_size/2]
        self.y_limits = [self.centre[1]-self.cell_size/2, self.centre[1]+self.cell_size/2]
        self.z_limits = [self.centre[2]-self.cell_size/2, self.centre[2]+self.cell_size/2]

        self.lines = []

        for idx, r in enumerate([self.r1, self.r2, self.r3]):
            if r > 0:
                self.lines.append(SimpleLine(self.design_space, self.centre, self.cell_size, r, INDEXES[idx]))

        self.unit_cell = self.lines[0]

        if len(self.lines) > 1:
            for i in range(1, len(self.lines)):
                self.unit_cell += self.lines[i]

    def evaluate_point(self, x, y, z):
        return self.unit_cell.evaluate_point(x, y, z)


class StrutLattice(Shape):
    def __init__(self, design_space, r=0.02, point_cloud=None, blend=0):
        super().__init__(design_space)
        self.r = r
        self.n_lines = 0
        self.lines = []
        self.blend = blend

        if point_cloud is not None:
            if len(point_cloud.points)==0:
                raise ValueError('Point cloud has no points.')
            self.point_cloud = point_cloud
            self.points = self.point_cloud.points

    @profile
    def generate_lattice(self):

        self.n_lines = len(self.lines)

        try:
            if len(self.r) == 1:
                initial_line = Line(self.design_space, self.lines[0][0], self.lines[0][1], r=self.r)
            else:
                initial_line = Line(self.design_space, self.lines[0][0], self.lines[0][1], r=self.r[0])

        except IndexError:

            print('No line points found.')

            raise

        print(f'Generating Lattice with {self.n_lines} lines...')

        initial_line.evaluate_grid(verbose=False)

        self.evaluated_grid = initial_line.evaluated_grid

        for i in range(1, len(self.lines)):
            self.evaluated_grid = next(self.new_grid(self.lines[i], i))

    def new_grid(self, line, idx):

        if len(self.r) == 1:
            line = Line(self.design_space, line[0], line[1], r=self.r)

        else:
            line = Line(self.design_space, line[0], line[1], r=self.r[idx])

        line.evaluate_grid(verbose=False)

        line_grid = line.evaluated_grid

        grid = self.evaluated_grid

        if self.blend == 0:

            yield ne.evaluate('where(grid<line_grid, grid, line_grid)')

        else:
            b = self.blend
            yield ne.evaluate(
                '-log(where((exp(-b*line_grid) + exp(-b*grid))>0.000, exp(-b*line_grid) + exp(-b*grid), 0.000))/b')

    @profile
    def generate_lattice_test(self):
        """
        This function is used to avoid instantiating many lines and doing boolean ops as its super slow.
        Want to vectorise using numpy ideally...
        """

        data_type = self.design_space.DATA_TYPE

        self.n_lines = len(self.lines)

        print(f'Generating {self.n_lines} Struts...')

        self.lines = np.array(self.lines, dtype=data_type)

        vec = np.array([self.x_grid, self.y_grid, self.z_grid], dtype=data_type)

        # Is there a way to avoid the ragged nested sequences error?
        vec_bc = np.array([self.design_space.X[:, None, None], self.design_space.Y[None, :, None],
                           self.design_space.Z[None, None, :]])

        ba = self.lines[:, 1, :] - self.lines[:, 0, :]

        baba = np.einsum('ij,ij->i', ba, ba, optimize='greedy')

        grid = np.full_like(self.x_grid, np.inf, dtype=data_type)

        for i, line in enumerate(self.lines[:, 0, :]):

            # Wanna avoid this line (slow)
            pa = vec - line[:, None, None, None]

            # Need to find a way to use this
            pa_bc = vec_bc - line

            paba_bc = pa_bc * ba[i]

            paba = np.dot(pa_bc, ba[i])

            h = np.empty_like(paba, dtype=data_type)

            np.clip(paba / baba[i], 0, 1, out=h)

            #ba_h_ = ba[i][:, None, None, None] * h

            ba_h = ne.evaluate('ba*h', local_dict={'ba':ba[i][:, None, None, None], 'h': h})

            pa_ba_h = np.empty_like(vec, dtype=data_type)

            print(pa_bc, ba_h)

            raise

            # Need to replace this implementation to use 'pa_bc' instead...
            ne.evaluate('pa-ba_h', local_dict={'pa': pa, 'ba_h': ba_h}, out=pa_ba_h)

            # Can this norm be made faster?
            if len(self.r) == 1:
                out = old_norm(pa_ba_h) - self.r
            else:
                out = old_norm(pa_ba_h) - self.r[i]

            if self.blend == 0:

                grid = ne.evaluate('where(grid<out, grid, out)', casting='same_kind')

            else:

                grid = ne.evaluate(
                    '-log(where((exp(-b*out) + exp(-b*grid))>0.000, exp(-b*out) + exp(-b*grid), 0.000))/b',
                    local_dict={'b': self.blend, 'grid': grid, 'out': out}, casting='same_kind')

        self.evaluated_grid = grid

        return


class RandomLattice(StrutLattice):

    def __init__(self, design_space, point_cloud, num_neighbours=4, radius=None, r=0.02):
        super().__init__(design_space, r, point_cloud)

        self.num_neighbours = num_neighbours
        self.radius = radius

        self.x_limits = [min(self.points[:, 0]), max(self.points[:, 0])]
        self.y_limits = [min(self.points[:, 1]), max(self.points[:, 1])]
        self.z_limits = [min(self.points[:, 2]), max(self.points[:, 2])]

        if self.num_neighbours is not None:

            self.neighbours = NearestNeighbors(n_neighbors=self.num_neighbours).fit(self.points)

            _, self.node_list = self.neighbours.kneighbors(self.points)

            self.node_list = np.array(self.node_list)

        else:

            self.neighbours = NearestNeighbors(radius=self.radius).fit(self.points)

            _, self.node_list = self.neighbours.radius_neighbors(self.points)

        nodes_dict = {i: [] for i in range(len(self.node_list))}

        for i in range(len(self.node_list)):

            for other_node in range(1, len(self.node_list[i])):
                nodes_dict[i].append(self.node_list[i][other_node])

        for node in nodes_dict.keys():

            for element in nodes_dict[node]:

                if node in nodes_dict[element]:
                    nodes_dict[element].remove(node)

        for node in nodes_dict.keys():

            p1 = self.points[node]

            for other_node in nodes_dict[node]:

                p2 = self.points[other_node]

                if (p1 != p2).any():
                    self.lines.append([p1, p2])

        self.generate_lattice()


class DelaunayLattice(StrutLattice):

    def __init__(self, design_space, point_cloud=None, r=0.02):
        super().__init__(design_space, r, point_cloud)

        self.designSpace = design_space
        self.point_cloud = point_cloud
        self.delaunay = scipy.spatial.Delaunay(self.point_cloud.points, qhull_options='Qbb Qc Qx QJ')

        self.x_limits = self.point_cloud.shape.x_limits
        self.y_limits = self.point_cloud.shape.y_limits
        self.z_limits = self.point_cloud.shape.z_limits

        for simplex in self.delaunay.simplices:
            line1 = tuple([simplex[0], simplex[1]])
            line2 = tuple([simplex[1], simplex[2]])
            line3 = tuple([simplex[2], simplex[3]])
            line4 = tuple([simplex[3], simplex[0]])
            self.lines.append(line1)
            self.lines.append(line2)
            self.lines.append(line3)
            self.lines.append(line4)

        self.lines = [list(line) for line in set(self.lines)]
        self.lines = [[self.delaunay.points[line[0]], self.delaunay.points[line[1]]] for line in self.lines]

        self.generate_lattice()


class ConvexHullLattice(StrutLattice):

    def __init__(self, design_space, point_cloud=None, r=0.02):
        super().__init__(design_space, r, point_cloud)

        self.designSpace = design_space
        self.point_cloud = point_cloud
        self.convex_hull = scipy.spatial.ConvexHull(self.point_cloud.points)

        self.x_limits = self.point_cloud.shape.x_limits
        self.y_limits = self.point_cloud.shape.y_limits
        self.z_limits = self.point_cloud.shape.z_limits

        self.flat_simplices = [item for simplex in self.convex_hull.simplices for item in simplex]

        for simplex in self.convex_hull.simplices:
            line1 = tuple([simplex[0], simplex[1]])
            line2 = tuple([simplex[1], simplex[2]])
            line3 = tuple([simplex[2], simplex[0]])
            self.lines.append(line1)
            self.lines.append(line2)
            self.lines.append(line3)

        self.lines = [list(line) for line in set(self.lines)]
        self.lines = [[self.convex_hull.points[line[0]], self.convex_hull.points[line[1]]] for line in self.lines]

        self.generate_lattice()


class VoronoiLattice(StrutLattice):

    def __init__(self, design_space, point_cloud=None, r=0.02, blend=0):
        super().__init__(design_space, r, point_cloud, blend)

        self.voronoi = scipy.spatial.Voronoi(self.point_cloud.points, qhull_options='Qbb Qc Qx')

        self.x_limits = self.point_cloud.shape.x_limits
        self.y_limits = self.point_cloud.shape.y_limits
        self.z_limits = self.point_cloud.shape.z_limits

        for region in self.voronoi.regions:

            try:
                region.remove(-1)

            except ValueError:
                pass

            for i, point in enumerate(region):

                if i == len(region)-1:

                    self.lines.append(tuple([point, region[0]]))

                else:

                    self.lines.append(tuple([point, region[i+1]]))

        self.lines = [list(line) for line in set(self.lines)]
        self.lines = [[self.voronoi.vertices[line[0]], self.voronoi.vertices[line[1]]] for line in self.lines]

        self.generate_lattice()


class RegularStrutLattice(StrutLattice):

    def __init__(self, design_space, n_cells=None, shape=None, r=0.05):
        super().__init__(design_space, r)
        if n_cells is None:
            n_cells = [1, 1, 1]
        self.shape = shape
        self.origin = np.array((min(self.shape.x_limits), min(self.shape.y_limits), min(self.shape.z_limits)))
        self.n_cells = n_cells

        self.x_limits = self.shape.x_limits
        self.y_limits = self.shape.y_limits
        self.z_limits = self.shape.z_limits

        self.xScale = max(self.shape.x_limits) - min(self.shape.x_limits)
        self.yScale = max(self.shape.y_limits) - min(self.shape.y_limits)
        self.zScale = max(self.shape.z_limits) - min(self.shape.z_limits)

        self.generate_points()

    def generate_points(self):
        origin = self.origin
        dx = self.xScale / self.n_cells[0]
        dy = self.yScale / self.n_cells[1]
        dz = self.zScale / self.n_cells[2]

        cell = [
            origin,
            origin + np.array([dx, 0, 0]),
            origin + np.array([dx, dy, 0]),
            origin + np.array([0, dy, 0]),
            origin + np.array([0, 0, dz]),
            origin + np.array([dx, 0, dz]),
            origin + np.array([dx, dy, dz]),
            origin + np.array([0, dy, dz]),
            origin + np.array([dx / 2, dy / 2, dz / 2])
        ]

        p2 = cell[len(cell) - 1]

        for i in range(len(cell) - 1):
            p1 = cell[i]
            self.lines.append([p1, p2])

        self.generate_lattice()


class OptimisationLattice(StrutLattice):

    def __init__(self, design_space, data, cell_size=1, scale=10):
        super().__init__(design_space)
        self.scale = scale
        self.cell_size = cell_size
        self.data = import_optimisation_data(data)

        self.x_limits = [-1, 1]
        self.y_limits = [-1, 1]
        self.z_limits = [-1, 1]

        self.create_struts()

    def create_struts(self):

        uc_list = []

        for idx, row in self.data.iterrows():
            x = row['x'] * self.scale
            y = row['y'] * self.scale
            z = row['z'] * self.scale
            r1 = row['r1']
            r2 = row['r2']
            r3 = row['r3']
            # r4 = row['r4'] * self.size
            # r5 = row['r5'] * self.size
            # r6 = row['r6'] * self.size
            # r7 = row['r7'] * self.size

            uc_list.append([[x, y, z], [r1, r2, r3]])

        self.uc_list = uc_list
        self.generate_lattice()

    def generate_lattice(self):

        self.n_cells = len(self.uc_list)

        try:
            initial_uc = AxialCentric(self.design_space, self.uc_list[0][0], self.uc_list[0][1][0], self.uc_list[0][1][1],
                                      self.uc_list[0][1][2], self.cell_size)

        except IndexError:

            print('No unit cells found.')

            raise

        print(f'Generating Lattice with {self.n_cells} unit cells...')

        initial_uc.evaluate_grid(verbose=False)

        self.evaluated_grid = initial_uc.evaluated_grid

        for i in range(1, len(self.uc_list)):
            self.evaluated_grid = next(self.new_grid(self.uc_list[i], i))

    def new_grid(self, uc, idx):

        uc = AxialCentric(self.design_space, self.uc_list[idx][0], self.uc_list[idx][1][0], self.uc_list[idx][1][1],
                                  self.uc_list[idx][1][2], self.cell_size)

        uc.evaluate_grid(verbose=False)

        uc_grid = uc.evaluated_grid

        grid = self.evaluated_grid

        yield ne.evaluate('where(grid<uc_grid, grid, uc_grid)')


def import_optimisation_data(path):
    data = pd.read_csv(path, nrows=2000, header=None)
    data.columns = ['x', 'y', 'z', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
    data = data.drop(data[(data.r1 == 0) & (data.r2 == 0) & (data.r3 == 0) & (data.r4 == 0) & (data.r5 == 0) &
                          (data.r6 == 0) & (data.r7 == 0)].index)

    data = data.drop(data[(data.r1 == 0) & (data.r2 == 0) & (data.r3 == 0)].index)

    return data


def clamp(n, a, b):
    if n < a:
        return a
    elif n > b:
        return b
    else:
        return n
