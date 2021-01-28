from .base import Base
from .surface import Surface
from ..vec import Vec3


class Primitive(Base):
    def __init__(
            self,
            surface: Surface = None,
            **parameters,
    ):
        surface = surface or Surface()
        super().__init__(
            surface=surface,
            **parameters,
        )
        self.surface = surface
        self._can_have_nodes = False


class Sphere(Primitive):

    def __init__(
            self,
            radius: float = 1.,
            surface: Surface = None
    ):
        super().__init__(
            radius=radius,
            surface=surface,
        )
        self.radius = radius

    def distance(self, pos: Vec3):
        return pos.length() - self.radius


class Tube(Primitive):
    def __init__(
            self,
            radius: float = 1.,
            axis: int = 0,
            surface: Surface = None
    ):
        if axis < 0 or axis > 2:
            raise ValueError("Illegal axis argument %d" % axis)
        super().__init__(
            radius=radius,
            axis=axis,
            surface=surface,
        )
        self.radius = radius
        self.axis = axis

    def distance(self, pos: Vec3):
        pos = pos.copy()
        pos[self.axis] = 0.
        return pos.length() - self.radius


class Plane(Primitive):
    def __init__(
            self,
            normal: Vec3,
            surface: Surface = None
    ):
        super().__init__(
            normal=normal,
            surface=surface,
        )
        self.normal = normal

    def distance(self, pos: Vec3):
        return pos.dot(self.normal)

