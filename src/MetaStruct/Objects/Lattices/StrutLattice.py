import cProfile
import io
import pstats

import numexpr as ne
import numpy as np
import scipy
from sklearn.neighbors import NearestNeighbors
import pandas as pd

from MetaStruct.Objects.Shapes.Line import Line
from MetaStruct.Objects.Shapes.Shape import Shape


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

    def __init__(self, design_space, data, cell_size=10, scale_factor=0.5):
        super().__init__(design_space)
        self.size = scale_factor
        self.cell_size = cell_size
        self.data = import_optimisation_data(data)

        self.x_limits = [-1, 1]
        self.y_limits = [-1, 1]
        self.z_limits = [-1, 1]

        self.create_struts()

    def create_struts(self):

        struts = []
        strut_radii = []

        for idx, row in self.data.iterrows():
            x = row['x'] * self.cell_size
            y = row['y'] * self.cell_size
            z = row['z'] * self.cell_size
            r1 = row['r1'] * self.size
            r2 = row['r2'] * self.size
            r3 = row['r3'] * self.size
            r4 = row['r4'] * self.size
            r5 = row['r5'] * self.size
            r6 = row['r6'] * self.size
            r7 = row['r7'] * self.size

            line1 = [[x - self.size / 2, y - self.size / 2, z + self.size / 2],
                     [x + self.size / 2, y + self.size / 2, z - self.size / 2], r1]

            line2 = [[x - self.size / 2, y + self.size / 2, z + self.size / 2],
                     [x + self.size / 2, y - self.size / 2, z - self.size / 2], r2]

            line3 = [[x - self.size / 2, y + self.size / 2, z - self.size / 2],
                     [x + self.size / 2, y - self.size / 2, z + self.size / 2], r3]

            line4 = [[x - self.size / 2, y - self.size / 2, z - self.size / 2],
                     [x + self.size / 2, y + self.size / 2, z + self.size / 2], r4]

            line5 = [[x - self.size / 2, y, z],
                     [x + self.size / 2, y, z], r5]

            line6 = [[x, y - self.size / 2, z],
                     [x, y + self.size / 2, z], r6]

            line7 = [[x, y, z - self.size / 2],
                     [x, y, z + self.size / 2], r7]

            for line in [line1, line2, line3, line4, line5, line6, line7]:
                if line[2] > 0:
                    struts.append([line[0], line[1]])
                    strut_radii.append(line[2])

        self.lines = struts
        self.r = strut_radii
        self.generate_lattice()


def import_optimisation_data(path):
    data = pd.read_csv(path, nrows=100, header=None)
    data.columns = ['x', 'y', 'z', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
    data = data.drop(data[(data.r1 == 0) & (data.r2 == 0) & (data.r3 == 0) & (data.r4 == 0) & (data.r5 == 0) &
                          (data.r6 == 0) & (data.r7 == 0)].index)

    return data


def clamp(n, a, b):
    if n < a:
        return a
    elif n > b:
        return b
    else:
        return n
