from .treenode import TreeNode
from ..vec.types import *
from ..vec import Vec3


INFINITY = 1.e20


class Base(TreeNode):

    __instance_counter = 0

    def __init__(self, **parameters):
        self.__instance_counter += 1
        super().__init__(f"{self.__class__.__name__}-{self.__instance_counter}")

        self.__parameters = parameters
        for key, value in self.__parameters.items():
            setattr(self, key, value)

    @property
    def parameters(self):
        return {
            key: getattr(self, key)
            for key in self.__parameters.keys()
        }

    def __repr__(self):
        s = f"{self.__class__.__name__}("
        s += ", ".join(
            f"{key}={repr(value)}"
            for key, value in self.parameters.items()
        )
        s += ")"
        return s

    __str__ = __repr__

    def distance(self, pos: Vec3):
        raise NotImplementedError
