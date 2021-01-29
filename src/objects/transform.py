from .base import Base, INFINITY
from .surface import Surface
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

    def distance_object(self, pos: Vec3):
        pos = pos - self.translation
        return self.nodes[0].distance(pos), self.nodes[0]


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

    def distance_object(self, pos: Vec3):
        pos = pos / self.scale
        return self.nodes[0].distance(pos) * self.scale, self.nodes[0]

