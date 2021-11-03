import cProfile
import io
import pstats
import time

import numba
import numexpr as ne
import numpy as np
import scipy
from sklearn.neighbors import NearestNeighbors
from numba import jit, njit

from MetaStruct.Objects.Shapes.Shape import Shape

from line_profiler_pycharm import profile


# def profile(func):
#     def wrapper(*args, **kwargs):
#         pr = cProfile.Profile()
#         pr.enable()
#         retval = func(*args, **kwargs)
#         pr.disable()
#         s = io.StringIO()
#         sortby = 'tottime'
#         ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#         ps.print_stats()
#         print(s.getvalue())
#         return retval
#
#     return wrapper

def old_norm(vector):
    return np.linalg.norm(vector, axis=0)


class StrutLattice(Shape):
    def __init__(self, design_space, r=0.02, point_cloud=None, blend=0):
        super().__init__(design_space)
        self.r = r
        self.n_lines = 0
        self.lines = []
        self.blend = blend

        if point_cloud is not None:
            if len(point_cloud.points) == 0:
                raise ValueError('Point cloud has no points.')
            self.point_cloud = point_cloud
            self.points = self.point_cloud.points

    @profile
    def generate_lattice(self):
        """
        This function is used to avoid instantiating many lines and doing boolean ops as its super slow.
        Want to vectorise using numpy ideally...
        """

        assert self.design_space.create_grids is True, 'create_grids must be true in the design space'

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
            start = time.time()

            # Wanna avoid this line (slow)
            pa = vec - line[:, None, None, None]

            # Need to find a way to use this
            pa_bc = vec_bc - line

            paba = np.dot(pa_bc, ba[i])

            h = np.clip(paba/baba[i], 0, 1)

            ba_h = ba[i][:, None, None, None] * h

            # Need to replace this implementation to use 'pa_bc' instead...
            pa_ba_h = ne.evaluate('pa-ba_h', local_dict={'pa': pa, 'ba_h': ba_h})

            # Can this norm be made faster?
            out = old_norm(pa_ba_h) - self.r

            if self.blend == 0:

                grid = ne.evaluate('where(grid<out, grid, out)', casting='same_kind')

            else:

                grid = ne.evaluate(
                    '-log(where((exp(-b*out) + exp(-b*grid))>0.000, exp(-b*out) + exp(-b*grid), 0.000))/b',
                    local_dict={'b': self.blend, 'grid': grid, 'out': out}, casting='same_kind')

        self.evaluated_grid = grid

        return


class RandomLattice(StrutLattice):

    def __init__(self, design_space, point_cloud, num_neighbours=4, radius=None, r=0.02, blend=0):
        super().__init__(design_space, r, point_cloud, blend)

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

    def __init__(self, design_space, point_cloud=None, r=0.02, blend=0):
        super().__init__(design_space, r, point_cloud, blend)

        self.designSpace = design_space
        self.point_cloud = point_cloud
        self.delaunay = scipy.spatial.Delaunay(self.point_cloud.points, qhull_options='Qbb Qc Qx')

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

    def __init__(self, design_space, point_cloud=None, r=0.02, blend=0):
        super().__init__(design_space, r, point_cloud, blend)

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

                if i == len(region) - 1:

                    self.lines.append(tuple([point, region[0]]))

                else:

                    self.lines.append(tuple([point, region[i + 1]]))

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


def clamp(n, a, b):
    if n < a:
        return a
    elif n > b:
        return b
    else:
        return n
