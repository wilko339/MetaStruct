from Objects.Geometry import Geometry

import numexpr as ne
import numpy as np


class CompositeLatticeSurface(Geometry):

    def __init__(self, lat1, lat2, blendMatrix=0.5):
        if lat1.designSpace is not lat2.designSpace:
            raise ValueError('Mismatching Design Spaces')

        super().__init__(lat1.designSpace)
        self.designSpace = lat1.designSpace
        self.lat1 = lat1
        self.lat2 = lat2
        self.lattices = [lat1, lat2]

        self.xLims = np.array([-1, 1])
        self.yLims = np.array([-1, 1])
        self.zLims = np.array([-1, 1])
        self.name = f'{lat1.name}_{lat2.name}'
        self.morph = self.lat1.morph

        self.blendMatrix = blendMatrix

    def evaluatePoint(self, x, y, z):

        for lat in self.lattices:

            if not hasattr(lat, 'evaluatedGrid'):

                lat.evaluateGrid()

        blend = self.blendMatrix
        l1 = self.lat1.evaluatedGrid
        l2 = self.lat2.evaluatedGrid

        return ne.evaluate('blend * l1 + (1- blend) * l2')
