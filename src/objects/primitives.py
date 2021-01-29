from .base import Base, INFINITY
from .material import Material
from ..vec import Vec3
from ..vec.types import *


class Primitive(Base):
    def __init__(
            self,
            material: Material = None,
            **parameters,
    ):
        self.material = material
        super().__init__(
            material=self.material,
            **parameters,
        )
        self._can_have_nodes = False


class Sphere(Primitive):

    def __init__(
            self,
            radius: Number = 1.,
            material: Material = None
    ):
        self.radius = float(radius)
        super().__init__(
            radius=self.radius,
            material=material,
        )

    def distance_object(self, pos: Vec3, ignore_objects=None):
        if ignore_objects and self in ignore_objects:
            return INFINITY, None
        return pos.length() - self.radius, self


class Tube(Primitive):
    def __init__(
            self,
            radius: float = 1.,
            axis: int = 0,
            material: Material = None
    ):
        if axis < 0 or axis > 2:
            raise ValueError("Illegal axis argument %d" % axis)
        self.radius = float(radius)
        self.axis = int(axis)
        super().__init__(
            radius=self.radius,
            axis=self.axis,
            material=material,
        )

    def distance_object(self, pos: Vec3, ignore_objects=None):
        if ignore_objects and self in ignore_objects:
            return INFINITY, None
        pos = pos.copy()
        pos[self.axis] = 0.
        return pos.length() - self.radius, self


class Plane(Primitive):
    def __init__(
            self,
            normal: Vector3,
            material: Material = None
    ):
        self.normal = Vec3(normal)
        super().__init__(
            normal=self.normal,
            material=material,
        )

    def distance_object(self, pos: Vec3, ignore_objects=None):
        if ignore_objects and self in ignore_objects:
            return INFINITY, None
        return pos.dot(self.normal), self

