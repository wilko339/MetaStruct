import numexpr as ne


class Vector:

    def __init__(self, p):
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]

    @property
    def magnitude(self):

        return ne.evaluate('sqrt(x**2 + y**2 + z**2)', local_dict={'x': self.x,
                                                                   'y': self.y,
                                                                   'z': self.z})

    def __sub__(self, other):
        return subtract(self, other)

    def __mul__(self, other):
        return multiplication(self, other)


def subtract(a, b):

    array_x = ne.evaluate('a-b', local_dict={'a': a.x, 'b': b.x})
    array_y = ne.re_evaluate(local_dict={'a': a.y, 'b': b.y})
    array_z = ne.re_evaluate(local_dict={'a': a.z, 'b': b.z})

    return Vector([array_x, array_y, array_z])


def multiplication(a, b):

    return ne.evaluate('(ax*bx)+(ay*by)+(az*bz)', local_dict={'ax': a.x,
                                                              'bx': b.x,
                                                              'ay': a.y,
                                                              'by': b.y,
                                                              'az': a.z,
                                                              'bz': b.z})
