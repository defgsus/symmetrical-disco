from .param_space import ParameterizedSpaceNode
from ..vec.types import *
from ..vec import Vec3


INFINITY = 1.e20


class Base(ParameterizedSpaceNode):

    # ----- ray-marching -----

    def distance(self, pos: Vec3):
        return self.distance_object(pos)[0]

    def distance_object(self, pos: Vec3, ignore_objects=None):
        raise NotImplementedError

    def normal(self, pos: Vec3, e: float = 0.001):
        return Vec3(
            self.distance(pos + (e, 0, 0)) - self.distance(pos - (e, 0, 0)),
            self.distance(pos + (0, e, 0)) - self.distance(pos - (0, e, 0)),
            self.distance(pos + (0, 0, e)) - self.distance(pos - (0, 0, e)),
        ).normalize_safe()

    def raymarch(
            self,
            origin: Vec3,
            direction: Vec3,
            max_iter: int = 1000,
            ignore_objects = None,
    ):
        pos = origin.copy()
        for it in range(max_iter):

            d, o = self.distance_object(pos, ignore_objects=ignore_objects)

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
