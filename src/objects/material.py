from .param_space import ParameterizedSpaceNode
from ..vec.types import *
from ..vec import Vec3


class Material(ParameterizedSpaceNode):

    def materials(self, pos: Vec3):
        """
        Generator for all contained Materials
        :param pos: Vec3 point in local space
        :return: generator
        """
        yield self, 1.


class Color(Material):

    def __init__(
            self,
            color: Vector3 = (1, 1, 1),
            reflective: float = 0.,
    ):
        self.color = Vec3(color)
        self.reflective = float(reflective)
        super().__init__(
            color=self.color,
            reflective=self.reflective,
        )


class Checker(Material):

    def __init__(
            self,
            material1: Material,
            material2: Material,
            scale: Union[float, Vector3] = 1.,
    ):
        super().__init__()
        self.material1 = material1
        self.material2 = material2
        self.scale = Vec3(scale)

    def materials(self, pos: Vec3):
        pos = (pos % self.scale) / self.scale
        s = False
        if pos.x >= .5:
            s = not s
        if pos.y >= .5:
            s = not s
        if pos.z >= .5:
            s = not s
        yield self.material1 if s else self.material2, 1.
