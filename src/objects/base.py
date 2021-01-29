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
        if self.nodes:
            if self.parameters:
                s += ", "
            s += "nodes=["
            s += ", ".join(repr(n) for n in self.nodes)
            s += "]"
        s += ")"
        return s

    __str__ = __repr__

    # ----- ray-marching -----

    def distance(self, pos: Vec3):
        return self.distance_object(pos)[0]

    def distance_object(self, pos: Vec3):
        raise NotImplementedError

    def raymarch(self, origin: Vec3, direction: Vec3, max_iter=1000):
        pos = origin.copy()
        for it in range(max_iter):

            d, o = self.distance_object(pos)

            if d <= 0.0001:
                return pos, o

            pos += d * direction

        return pos, None

    # ---- deformations ----

    def translate(self, translation: Vector3):
        """
        Returns a translated object.

        :param translation: a float sequence of length 3
        :return: a ``Translate`` object
        """
        from .transform import Translate
        return Translate(
            object=self,
            translation=Vec3(translation),
        )

    def scale(self, scale: float):
        """
        Returns a scaled object.

        :param scale: a float
        :return: a ``Scale`` object
        """
        from .transform import Scale
        return Scale(
            object=self,
            scale=float(scale),
        )
