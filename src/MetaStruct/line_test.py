from MetaStruct.Objects.designspace import DesignSpace
from MetaStruct.Objects.Shapes.Line import Line


def main():
    ds = DesignSpace(500)
    line = Line(ds, p1=[-1, 1, -1], p2=[1, -1, 1], r=0.2)

    line.preview_model()


if __name__ == "__main__":
    main()