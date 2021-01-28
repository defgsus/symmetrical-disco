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
            translation: Vec3,
    ):
        super().__init__(
            translation=translation,
            object=object,
        )
        self.translation = translation

    def distance(self, pos: Vec3):
        pos = pos - self.translation
        return self.nodes[0].distance(pos)


class Scale(TransformBase):

    def __init__(
            self,
            scale: float,
            object: Base = None,
    ):
        super().__init__(
            scale=scale,
            object=object,
        )
        self.scale = scale

    def distance(self, pos: Vec3):
        pos = pos / self.scale
        return self.nodes[0].distance(pos) * self.scale

