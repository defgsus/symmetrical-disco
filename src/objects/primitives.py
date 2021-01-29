from .base import Base
from .surface import Surface
from ..vec import Vec3
from ..vec.types import *


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
            radius: Number = 1.,
            surface: Surface = None
    ):
        self.radius = float(radius)
        super().__init__(
            radius=self.radius,
            surface=surface,
        )

    def distance_object(self, pos: Vec3):
        return pos.length() - self.radius, self


class Tube(Primitive):
    def __init__(
            self,
            radius: float = 1.,
            axis: int = 0,
            surface: Surface = None
    ):
        if axis < 0 or axis > 2:
            raise ValueError("Illegal axis argument %d" % axis)
        self.radius = float(radius)
        self.axis = int(axis)
        super().__init__(
            radius=self.radius,
            axis=self.axis,
            surface=surface,
        )

    def distance_object(self, pos: Vec3):
        pos = pos.copy()
        pos[self.axis] = 0.
        return pos.length() - self.radius, self


class Plane(Primitive):
    def __init__(
            self,
            normal: Vector3,
            surface: Surface = None
    ):
        self.normal = Vec3(normal)
        super().__init__(
            normal=self.normal,
            surface=surface,
        )

    def distance_object(self, pos: Vec3):
        return pos.dot(self.normal), self

