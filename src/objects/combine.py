from .base import Base, INFINITY
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

    def distance_object(self, pos: Vec3, ignore_objects=None):
        dist, obj = INFINITY, None
        for node in self.nodes:
            if ignore_objects and node in ignore_objects:
                continue
            d, o = node.distance_object(pos, ignore_objects=ignore_objects)
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

    def distance_object(self, pos: Vec3, ignore_objects=None):
        dist, obj = INFINITY, None
        if not self.nodes:
            return dist, obj

        for node in self.nodes:
            if ignore_objects and self in ignore_objects:
                continue

            if obj is None:
                dist, obj = node.distance_object(pos, ignore_objects=ignore_objects)
            else:
                d, o = node.distance_object(pos, ignore_objects=ignore_objects)
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

    def distance_object(self, pos: Vec3, ignore_objects=None):
        dist, obj = INFINITY, None
        if not self.nodes:
            return dist, obj

        for node in self.nodes:
            if ignore_objects and self in ignore_objects:
                continue

            if obj is None:
                dist, obj = node.distance_object(pos, ignore_objects=ignore_objects)
            else:
                d, o = node.distance_object(pos, ignore_objects=ignore_objects)
                if d > dist:
                    dist, obj = d, o
        return dist, obj
