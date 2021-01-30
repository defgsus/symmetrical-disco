import math
import random
from io import StringIO
from unittest import TestCase
import doctest

from src.vec import *
from src.vec.types import *
from src.objects import *
from src.raymarcher import Raymarcher
from src.image import Image


class TestPrimitives(TestCase):

    def render_isometric(
            self,
            scene: Base,
            origin: Vector3 = (0, 0, -5),
            direction: Vector3 = (0, 0, 1),
            width: int = 6,
            height: int = 6,
    ):
        origin = Vec3(origin)
        direction = Vec3(direction)

        raymarcher = Raymarcher(scene)
        image = Image(width, height)
        raymarcher.render(image, lambda p: (p + origin, direction), aa=4)

        file = StringIO()
        image.dump_bw(file=file, black=".", white="#", threshold=.3)
        file.seek(0)
        #image.dump()
        return file.read()

    def assertIsometric(
            self,
            scene: Base,
            expected: str,
            origin: Vector3 = (0, 0, -5),
            direction: Vector3 = (0, 0, 1),
            width: int = 6,
            height: int = 6,
    ):
        expected = "\n".join(l.strip() for l in expected.strip().splitlines())
        rendered = self.render_isometric(
            scene=scene, origin=origin, direction=direction,
            width=width, height=height,
        ).strip()

        if expected != rendered:
            expected_str = "\n".join(f"  [{line}]" for line in expected.splitlines())
            rendered_str = "\n".join(f"  [{line}]" for line in rendered.splitlines())
            raise AssertionError(
                f"\n\nExpected:\n{expected_str}\n\nGot:\n{rendered_str}"
            )

    def test_sphere(self):
        scene = Sphere()
        # print(self.render_isometric(scene))
        self.assertIsometric(scene, """
            ....####....
            ..########..
            ############
            ############
            ..########..
            ....####....
        """)

    def test_sphere_plane_intersection(self):
        scene = Intersection([
            Sphere(),
            Plane((-1, 0, 0)),
        ])
        # print(self.render_isometric(scene))
        self.assertIsometric(scene, """
            ......##....
            ......####..
            ......######
            ......######
            ......####..
            ......##....
        """)

