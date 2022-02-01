from MetaStruct.Objects.Lattices.StrutLattice import StrutLattice, BCCAxial
import pandas as pd

"""
This code was written to import strut lattice optimisation data and generate the lattice structure.
The unit cell 'BCCAxial' is no longer able to be used, since it now only accepts a single radius
argument. If individual strut radii are required to be changed, then the unit cell needs to be
re-implemented (under a different name!).
"""

class OptimisationLattice(StrutLattice):

    def __init__(self, design_space, data, cell_size=1, scale=20):
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
            r4 = row['r4']
            r5 = row['r5']
            r6 = row['r6']
            r7 = row['r7']

            uc_list.append([[x, y, z], [r1, r2, r3, r4, r5, r6, r7]])

        self.uc_list = uc_list
        self.generate_lattice()

    def generate_lattice(self):

        self.n_cells = len(self.uc_list)

        try:
            initial_uc = BCCAxial(self.design_space, self.uc_list[0][0], self.uc_list[0][1][0], self.uc_list[0][1][1],
                                  self.uc_list[0][1][2], self.uc_list[0][1][3], self.uc_list[0][1][4],
                                  self.uc_list[0][1][5], self.uc_list[0][1][6], self.cell_size)

        except IndexError:

            print('No unit cells found.')

            raise

        print(f'Generating Lattice with {self.n_cells} unit cells...')

        initial_uc.evaluate_grid(verbose=False)

        self.evaluated_grid = initial_uc.evaluated_grid

        for i in range(1, len(self.uc_list)):
            self.evaluated_grid = next(self.new_grid(self.uc_list[i], i))

    def new_grid(self, uc, idx):

        uc = BCCAxial(self.design_space, self.uc_list[idx][0], self.uc_list[idx][1][0], self.uc_list[idx][1][1],
                      self.uc_list[idx][1][2], self.uc_list[idx][1][3], self.uc_list[idx][1][4],
                      self.uc_list[idx][1][5], self.uc_list[idx][1][6], self.cell_size)

        uc.evaluate_grid(verbose=False)

        uc_grid = uc.evaluated_grid

        grid = self.evaluated_grid

        yield ne.evaluate('where(grid<uc_grid, grid, uc_grid)')


def import_optimisation_data(path):
    data = pd.read_csv(path, header=None)
    data.columns = ['x', 'y', 'z', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
    data = data.drop(data[(data.r1 == 0) & (data.r2 == 0) & (data.r3 == 0) & (data.r4 == 0) & (data.r5 == 0) &
                          (data.r6 == 0) & (data.r7 == 0)].index)

    # data = data.drop(data[(data.x > 0.25) & (data.y > 0.25) & (data.z > 0.25)].index)

    return data

