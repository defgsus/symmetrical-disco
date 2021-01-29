from ..vec.types import *
from ..vec import Vec3


class Surface:

    def __init__(
            self,
            color: Vector3 = (1, 1, 1),
    ):
        self.color = Vec3(color)

    def __repr__(self):
        return f"{self.__class__.__name__}(color={self.color})"

