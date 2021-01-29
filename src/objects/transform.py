from .base import Base, INFINITY
from ..vec import Vec3
from ..vec.types import *


class TransformBase(Base):
    def __init__(
            self,
            object: Base = None,
            **parameters
    ):
        super().__init__(**parameters)
        if object:
            self.add_node(object)

    def to_local_position(self, outside_pos: Vec3):
        raise NotImplementedError

    def from_local_position(self, local_pos: Vec3):
        raise NotImplementedError


class Translate(TransformBase):

    def __init__(
            self,
            object: Base,
            translation: Vector3,
    ):
        self.translation = Vec3(translation)
        super().__init__(
            translation=self.translation,
            object=object,
        )

    def distance_object(self, pos: Vec3, ignore_objects=None):
        if not self.nodes or (ignore_objects and self.nodes[0] in ignore_objects):
            return INFINITY, None

        pos = pos - self.translation
        return self.nodes[0].distance(pos), self.nodes[0]

    def to_local_position(self, outside_pos: Vec3):
        return outside_pos - self.translation

    def from_local_position(self, local_pos: Vec3):
        return local_pos + self.translation


class Scale(TransformBase):

    def __init__(
            self,
            scale: Number,
            object: Base = None,
    ):
        self.scale = float(scale)
        super().__init__(
            scale=self.scale,
            object=object,
        )

    def distance_object(self, pos: Vec3, ignore_objects=None):
        if not self.nodes or (ignore_objects and self.nodes[0] in ignore_objects):
            return INFINITY, None

        pos = pos / self.scale
        return self.nodes[0].distance(pos) * self.scale, self.nodes[0]

    def to_local_position(self, outside_pos: Vec3):
        return outside_pos / self.scale

    def from_local_position(self, local_pos: Vec3):
        return local_pos * self.scale
