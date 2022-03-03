import numexpr as ne
import numpy as np
import scipy
from sklearn.neighbors import NearestNeighbors

from MetaStruct.Objects.Shapes.Line import Line, SimpleLine
from MetaStruct.Objects.Shapes.Shape import Shape


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

    def generate_lattice(self):

        self.n_lines = len(self.lines)

        try:
            if type(self.r) is float:
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

        if type(self.r) is float:
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

            # ba_h_ = ba[i][:, None, None, None] * h

            ba_h = ne.evaluate('ba*h', local_dict={'ba': ba[i][:, None, None, None], 'h': h})

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
        super().__init__(design_space=design_space, r=r, point_cloud=point_cloud)

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


class RepeatingLattice(StrutLattice):

    def __init__(self, design_space, unit_cell=None, x=0, y=0, z=0, period=1, r=0.05):
        self.design_space = design_space
        self.period = period
        self.r = r
        self.x = x
        self.y = y
        self.z = z
        if unit_cell is None:
            self.unit_cell = BCCAxial(self.design_space, np.array([self.x, self.y, self.z]), self.r, self.period)
        else:
            self.unit_cell = unit_cell

        super().__init__(design_space, self.r)

        self.x_limits = [self.x - self.period / 2, self.x + self.period / 2]
        self.y_limits = [self.y - self.period / 2, self.y + self.period / 2]
        self.z_limits = [self.z - self.period / 2, self.z + self.period / 2]

    def evaluate_point(self, x, y, z):

        x = np.mod((x+0.5*self.period), self.period) - 0.5*self.period
        y = np.mod((y+0.5*self.period), self.period) - 0.5*self.period
        z = np.mod((z+0.5*self.period), self.period) - 0.5*self.period

        return self.unit_cell.evaluate_point(x, y, z)

    def evaluate_point_grid(self, x, y, z):

        x = ne.evaluate('((x+0.5*p) % p)-0.5*p', local_dict={'x': x, 'p': self.period})
        y = ne.re_evaluate(local_dict={'x': y, 'p': self.period})
        z = ne.re_evaluate(local_dict={'x': z, 'p': self.period})

        return self.unit_cell.evaluate_point_grid(x, y, z)


class UnitCell(Shape):
    def __init__(self, design_space):
        super().__init__(design_space)
        self.unit_cell = None

    def evaluate_point(self, x, y, z):

        self.unit_cell = Line(self.design_space, self.points[self.lines[0][0]], self.points[self.lines[0][1]], self.r)

        for idx, line in enumerate(self.lines[1:]):
            self.unit_cell += Line(self.design_space, self.points[line][0], self.points[line][1], self.r)

        return self.unit_cell.evaluate_point(x, y, z)

    def evaluate_point_grid(self, x, y, z):

        self.unit_cell = Line(self.design_space, self.points[self.lines[0][0]], self.points[self.lines[0][1]], self.r)

        for idx, line in enumerate(self.lines[1:]):
            self.unit_cell += Line(self.design_space, self.points[line][0], self.points[line][1], self.r)

        return self.unit_cell.evaluate_point_grid(x, y, z)


class AxialCentric(UnitCell):
    def __init__(self, design_space, centre=None, r=0.25, cell_size=1):
        if centre is None:
            centre = [0, 0, 0]
        self.centre = centre
        self.r = r
        self.cell_size = cell_size

        super().__init__(design_space)

        self.x_limits = [self.centre[0] - self.cell_size / 2, self.centre[0] + self.cell_size / 2]
        self.y_limits = [self.centre[1] - self.cell_size / 2, self.centre[1] + self.cell_size / 2]
        self.z_limits = [self.centre[2] - self.cell_size / 2, self.centre[2] + self.cell_size / 2]

        self.lines = []
        self.unit_cell = None

    def evaluate_point(self, x, y, z):

        for ax in ['x', 'y', 'z']:
            self.lines.append(SimpleLine(self.design_space, self.centre, self.cell_size, self.r, ax))

        self.unit_cell = self.lines[0] + self.lines[1] + self.lines[2]

        return self.unit_cell.evaluate_point(x, y, z)


class OctetTruss(UnitCell):
    def __init__(self, design_space, centre=None, r=0.25, cell_size=1):
        if centre is None:
            centre = [0, 0, 0]
        self.centre = centre
        self.r = r
        self.cell_size = cell_size

        super().__init__(design_space)

        self.x_limits = [self.centre[0] - self.cell_size / 2, self.centre[0] + self.cell_size / 2]
        self.y_limits = [self.centre[1] - self.cell_size / 2, self.centre[1] + self.cell_size / 2]
        self.z_limits = [self.centre[2] - self.cell_size / 2, self.centre[2] + self.cell_size / 2]

        self.lines = []
        self.unit_cell = None

        self.points = (np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1],
            [1, 1, 1],
            [0.5, 0.5, 0],
            [0.5, 0, 0.5],
            [0, 0.5, 0.5],
            [1, 0.5, 0.5],
            [0.5, 1, 0.5],
            [0.5, 0.5, 1],
        ]) - 0.5) * self.cell_size + self.centre

        self.lines = [
            [0, 3],
            [0, 5],
            [0, 6],
            [1, 2],
            [1, 4],
            [1, 7],
            [2, 4],
            [2, 7],
            [3, 5],
            [3, 6],
            [4, 7],
            [5, 6],
            [8, 9],
            [8, 10],
            [8, 11],
            [8, 12],
            [9, 10],
            [9, 11],
            [10, 12],
            [11, 12],
            [13, 9],
            [13, 10],
            [13, 11],
            [13, 12],
        ]

class BCCAxial(UnitCell):

    def __init__(self, design_space, centre=None, r=0.25, cell_size=1):
        super().__init__(design_space)

        if centre is None:
            centre = np.array([0, 0, 0])
        self.centre = np.array(centre)
        self.r = r
        self.cell_size = cell_size

        super().__init__(design_space)

        self.x_limits = [self.centre[0] - self.cell_size / 2, self.centre[0] + self.cell_size / 2]
        self.y_limits = [self.centre[1] - self.cell_size / 2, self.centre[1] + self.cell_size / 2]
        self.z_limits = [self.centre[2] - self.cell_size / 2, self.centre[2] + self.cell_size / 2]

        self.lines = []
        self.unit_cell = None

        self.points = (np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1],
            [1, 1, 1]
        ]) - 0.5) * self.cell_size + self.centre

        self.lines = [
            [0, 7],
            [1, 6],
            [2, 5],
            [3, 4]
        ]


class RhombicDodecahedron(UnitCell):

    def __init__(self, design_space, centre=None, r=0.25, cell_size=1):
        super().__init__(design_space)

        if centre is None:
            centre = np.array([0, 0, 0])
        self.centre = np.array(centre)
        self.r = r
        self.cell_size = cell_size

        super().__init__(design_space)

        self.x_limits = [self.centre[0] - self.cell_size / 2, self.centre[0] + self.cell_size / 2]
        self.y_limits = [self.centre[1] - self.cell_size / 2, self.centre[1] + self.cell_size / 2]
        self.z_limits = [self.centre[2] - self.cell_size / 2, self.centre[2] + self.cell_size / 2]

        self.lines = []
        self.unit_cell = None

        self.points = (np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1],
            [1, 1, 1],
            [0.5, 0.5, 0],
            [0.5, 0, 0.5],
            [0, 0.5, 0.5],
            [1, 0.5, 0.5],
            [0.5, 1, 0.5],
            [0.5, 0.5, 1],
            [0.25, 0.25, 0.25],
            [0.75, 0.25, 0.25],
            [0.25, 0.75, 0.25],
            [0.75, 0.75, 0.25],
            [0.25, 0.25, 0.75],
            [0.75, 0.25, 0.75],
            [0.25, 0.75, 0.75],
            [0.75, 0.75, 0.75]
        ]) - 0.5) * self.cell_size + self.centre

        self.lines = [
            [0, 14],
            [1, 15],
            [2, 16],
            [3, 17],
            [4, 18],
            [5, 19],
            [6, 20],
            [7, 21],
            [8, 14],
            [8, 15],
            [8, 16],
            [8, 17],
            [9, 14],
            [9, 15],
            [9, 18],
            [9, 19],
            [10, 14],
            [10, 16],
            [10, 18],
            [10, 20],
            [11, 15],
            [11, 17],
            [11, 19],
            [11, 21],
            [12, 16],
            [12, 17],
            [12, 20],
            [12, 21],
            [13, 18],
            [13, 19],
            [13, 20],
            [13, 21],
        ]

