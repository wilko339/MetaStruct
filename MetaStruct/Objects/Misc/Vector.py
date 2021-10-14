import numexpr as ne


class Vector:

    def __init__(self, p):
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]

    @property
    def magnitude(self):
        x = self.x
        y = self.y
        z = self.z
        return ne.evaluate('sqrt(x**2 + y**2 + z**2)')

    def __sub__(self, other):
        return subtract(self, other)

    def __mul__(self, other):
        return mult(self, other)


def subtract(a, b):
    ax = a.x
    ay = a.y
    az = a.z

    bx = b.x
    by = b.y
    bz = b.z

    arrx = ne.evaluate('ax-bx')
    arry = ne.evaluate('ay-by')
    arrz = ne.evaluate('az-bz')

    return Vector([arrx, arry, arrz])


def mult(a, b):
    ax = a.x
    ay = a.y
    az = a.z

    bx = b.x
    by = b.y
    bz = b.z

    return ne.evaluate('(ax*bx)+(ay*by)+(az*bz)')
