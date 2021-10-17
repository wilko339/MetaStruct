import cProfile
import io
import pstats

import numexpr as ne
import numpy as np
import progressbar
import pyvoro
from scipy.spatial import Delaunay, ConvexHull
from sklearn.neighbors import NearestNeighbors

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
            if not point_cloud.points:
                raise ValueError('Point cloud has no points.')
            self.point_cloud = point_cloud
            self.points = self.point_cloud.points

    def generate_lattice(self):

        self.n_lines = len(self.lines)

        try:

            initial_line = Line(self.design_space, self.lines[0][0], self.lines[0][1], r=self.r)

        except IndexError:

            print('No line points found.')

            raise

        print(f'Generating Lattice with {self.n_lines} lines...')

        initial_line.evaluate_grid(verbose=False)

        self.evaluated_grid = initial_line.evaluated_grid

        widgets = [' [',
                   progressbar.Timer(format='elapsed time: %(elapsed)s'),
                   '] ',
                   progressbar.Bar('*'), ' (',
                   progressbar.ETA(), ') '
                   ]

        bar = progressbar.ProgressBar(max_value=len(self.lines),
                                      widgets=widgets).start()

        for i in range(1, len(self.lines)):
            self.evaluated_grid = next(self.new_grid(self.lines[i]))
            bar.update(i)
        bar.finish()

    def new_grid(self, line):

        line = Line(self.design_space, line[0], line[1], r=self.r)

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
        self.delaunay = Delaunay(self.point_cloud.points, qhull_options='Qbb Qc Qx QJ')

        self.xLims = self.point_cloud.shape.x_limits
        self.yLims = self.point_cloud.shape.y_limits
        self.zLims = self.point_cloud.shape.z_limits

        for simplex in self.delaunay.simplices:
            line1 = [self.delaunay.points[simplex[0]], self.delaunay.points[simplex[1]]]
            line2 = [self.delaunay.points[simplex[1]], self.delaunay.points[simplex[2]]]
            line3 = [self.delaunay.points[simplex[2]], self.delaunay.points[simplex[3]]]
            line4 = [self.delaunay.points[simplex[3]], self.delaunay.points[simplex[0]]]
            self.lines.append(line1)
            self.lines.append(line2)
            self.lines.append(line3)
            self.lines.append(line4)

        self.generate_lattice()


class ConvexHullLattice(StrutLattice):

    def __init__(self, design_space, point_cloud=None, r=0.02):
        super().__init__(design_space, r, point_cloud)

        self.designSpace = design_space
        self.point_cloud = point_cloud
        self.convex_hull = ConvexHull(self.point_cloud.points)

        self.xLims = self.point_cloud.shape.x_limits
        self.yLims = self.point_cloud.shape.y_limits
        self.zLims = self.point_cloud.shape.z_limits

        self.flat_simplices = [item for simplex in self.convex_hull.simplices for item in simplex]

        for simplex in self.convex_hull.simplices:
            line1 = [self.convex_hull.points[simplex[0]], self.convex_hull.points[simplex[1]]]
            line2 = [self.convex_hull.points[simplex[1]], self.convex_hull.points[simplex[2]]]
            line3 = [self.convex_hull.points[simplex[2]], self.convex_hull.points[simplex[0]]]
            self.lines.append(line1)
            self.lines.append(line2)
            self.lines.append(line3)

        # TODO: Remove duplicate lines from self.lines

        self.generate_lattice()


class VoronoiLattice(StrutLattice):

    def __init__(self, design_space, point_cloud=None, r=0.02):
        super().__init__(design_space, r, point_cloud)

        # self.voronoi = Voronoi(self.point_cloud.points, qhull_options='Qbb Qc Qx')

        self.x_limits = self.point_cloud.shape.x_limits
        self.y_limits = self.point_cloud.shape.y_limits
        self.z_limits = self.point_cloud.shape.z_limits

        self.voronoi = pyvoro.compute_voronoi(points=point_cloud.points, limits=[self.x_limits, self.y_limits,
                                                                                 self.z_limits], dispersion=2)

        cells = []

        for cell in self.voronoi:
            cell_vertices = cell['vertices']
            faces = cell['faces']

            for face in faces:
                vertices = face['vertices']
                for i in range(len(vertices)):
                    if i < len(vertices) - 1:
                        self.lines.append(
                            tuple([tuple(cell_vertices[vertices[i]]), tuple(cell_vertices[vertices[i + 1]])]))
                    else:
                        self.lines.append(tuple([tuple(cell_vertices[vertices[i]]), tuple(cell_vertices[vertices[0]])]))

        # TODO Remove duplicated lines from self.lines

        self.lines = list(set(self.lines))

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