from .base import Base, INFINITY
from .surface import Surface
from ..vec import Vec3
from ..vec.types import *


class Container(Base):
    def __init__(
            self,
            objects: Sequence[Base] = None,
            **parameters
    ):
        super().__init__(**parameters)
        if objects:
            for o in objects:
                self.add_node(o)


class Union(Container):

    def distance(self, pos: Vec3):
        d = INFINITY
        for node in self.nodes:
            d = min(d, node.distance(pos))
        return d

    def distance_object(self, pos: Vec3):
        dist, obj = INFINITY, None
        for node in self.nodes:
            d, o = node.distance_object(pos)
            if d < dist:
                dist, obj = d, o
        return dist, obj


class Difference(Container):

    def distance(self, pos: Vec3):
        if not self.nodes:
            return INFINITY
        d = self.nodes[0].distance(pos)
        for node in self.nodes[1:]:
            d = max(d, -node.distance(pos))
        return d

    def distance_object(self, pos: Vec3):
        if not self.nodes:
            return INFINITY, None
        dist, obj = self.nodes[0].distance_object(pos)
        for node in self.nodes[1:]:
            d, o = node.distance_object(pos)
            d = -d
            if d > dist:
                dist, obj = d, o
        return dist, obj


class Intersection(Container):

    def distance(self, pos: Vec3):
        if not self.nodes:
            return INFINITY
        d = self.nodes[0].distance(pos)
        for node in self.nodes[1:]:
            d = max(d, node.distance(pos))
        return d

    def distance_object(self, pos: Vec3):
        if not self.nodes:
            return INFINITY, None
        dist, obj = self.nodes[0].distance_object(pos)
        for node in self.nodes[1:]:
            d, o = node.distance_object(pos)
            if d > dist:
                dist, obj = d, o
        return dist, obj
