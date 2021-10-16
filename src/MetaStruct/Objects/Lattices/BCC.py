import numexpr as ne

from MetaStruct.Objects.Lattices.Lattice import Lattice


class BCC(Lattice):
    """BCC Lattice Object:\n\n\
    (x, y, z)\t\t: Centre of Lattice. Adjust to Translate.\n\n\
    (nx, ny, nz)\t: Number of unit cells per length.\n\n\
    (lx, ly, lz)\t: Length of unit cell in each direction. """

    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6317040/pdf/materials-11-02411.pdf

    def __init__(self, design_space, x=0, y=0, z=0, nx=1, ny=1, nz=1, lx=1, ly=1, lz=1, vf=0.2):

        self.vf = vf

        super().__init__(design_space, x, y, z, nx, ny, nz, lx, ly, lz, vf)

    def evaluate_point(self, x, y, z):
        """Returns the function value at point (x, y, z)."""

        x0 = self.x
        y0 = self.y
        z0 = self.z
        kx = self.kx
        ky = self.ky
        kz = self.kz
        vf = self.vf
        vf = ne.evaluate('vf*100')

        t = ne.evaluate('-8.04119e-8*vf**4 + 1.71079e-5*vf**3 - \
            0.0014808*vf**2 - 0.0136365*vf + 2.96255414')

        expr = 'cos(2*kx*(x-x0)) + cos(2*ky*(y-y0)) + cos(2*kz*(z-z0)) - \
            2*(cos(kx*(x-x0))*cos(ky*(y-y0)) + cos(ky*(y-y0))*cos(kz*(z-z0)) + cos(kz*(z-z0))*cos(kx*(x-x0))) + t'

        return ne.evaluate(expr)
