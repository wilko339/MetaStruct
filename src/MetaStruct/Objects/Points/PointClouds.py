import math

import numpy as np
from smt.sampling_methods import LHS, FullFactorial


class PointCloud:

    def __init__(self, n_points, shape=None, points=None):
        self.n_points = n_points
        self.points = points

        self.shape = shape

        self.xScale = max(self.shape.x_limits) - min(self.shape.x_limits)
        self.yScale = max(self.shape.y_limits) - min(self.shape.y_limits)
        self.zScale = max(self.shape.z_limits) - min(self.shape.z_limits)

    def generate_points(self, n_points):
        self.points[:, 0] = self.points[:, 0] * self.xScale + min(self.shape.x_limits)
        self.points[:, 1] = self.points[:, 1] * self.yScale + min(self.shape.y_limits)
        self.points[:, 2] = self.points[:, 2] * self.zScale + min(self.shape.z_limits)

        if self.shape is not None:
            point_values = self.shape.evaluate_point(self.points[:, 0], self.points[:, 1], self.points[:, 2])
            mask = np.ma.masked_array(point_values <= 0)
            self.points = self.points[mask, :]

    def __add__(self, other):
        points = np.append(self.points, other.points, axis=0)
        return PointCloud(self.n_points, points=points)


class RandomPoints(PointCloud):

    def __init__(self, n_points=50, shape=None, points=None, seed=None):
        super().__init__(n_points, shape, points)
        if seed is not None:
            np.random.seed(seed)
        self.points = np.random.rand(n_points, 3)
        self.generate_points(self.n_points)


class LHSPoints(PointCloud):

    def __init__(self, n_points=50, shape=None, points=None):
        super().__init__(n_points, shape, points)
        self.points = LHS(xlimits=np.array([[0, 1], [0, 1], [0, 1]]))(n_points)
        self.generate_points(self.n_points)


class FFPoints(PointCloud):

    def __init__(self, n_points=100, shape=None, points=None):
        super().__init__(n_points, shape, points)
        self.points = FullFactorial(xlimits=np.array([[0, 1], [0, 1], [0, 1]]), clip=True) \
            (n_points)
        self.generate_points(self.n_points)


class PointsOnSphere(PointCloud):

    def __init__(self, n_points=50, sphere=None):
        super().__init__(n_points, shape=sphere, points=None)
        self.radius = self.shape.r

        self.xBounds = self.shape.design_space.x_bounds
        self.yBounds = self.shape.design_space.y_bounds
        self.zBounds = self.shape.design_space.z_bounds

        self.points = []

        self.generate_points()

    def generate_points(self):
        self.points = fibonacci_sphere(self.n_points, self.shape)

    def __add__(self, other):
        points = np.append(self.points, other.points, axis=0)
        return PointCloud(self.n_points, shape=self.shape, points=points)


def fibonacci_sphere(samples=20, sphere=None):
    'https://stackoverflow.com/questions/57123194/how-to-distribute-points-evenly-on-the-surface-of-hyperspheres-in-higher-dimensi'
    cen_x = sphere.x
    cen_y = sphere.y
    cen_z = sphere.z
    rad = sphere.r

    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians

    for i in range(samples):
        y = ((1 - (i / float(samples - 1)) * 2) + cen_y)  # y goes from 1 to -1
        radius = math.sqrt(1 - y * y) * rad # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius + cen_x
        z = math.sin(theta) * radius + cen_z

        points.append((x, y*rad, z))

    return np.array(points)
