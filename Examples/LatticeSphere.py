from Objects.Booleans.Boolean import Union
from Objects.DesignSpace import DesignSpace
from Objects.Lattices.Gyroid import Gyroid
from Objects.Shapes.HollowSphere import HollowSphere


def latticedSphereExample(outerRad=2, outerSkinThickness=0.1, innerRad=1, innerSkinThickness=0.1):

    ds = DesignSpace(resolution=300)

    outerSkin = HollowSphere(design_space=ds, r=outerRad, t=outerSkinThickness)

    latticeSection = HollowSphere(r=outerRad-outerSkinThickness,
                                  t=outerRad - outerSkinThickness - innerRad,
                                  design_space=ds) / Gyroid(designSpace=ds)

    innerSkin = HollowSphere(r=innerRad, t=innerSkinThickness, design_space=ds)

    s1 = Union(outerSkin, Union(latticeSection, innerSkin))

    s1.previewModel(clip='x')
