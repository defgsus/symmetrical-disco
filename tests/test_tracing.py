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


class TestTracing(TestCase):

    def test_reflect(self):
        scene = Sphere()

        # hit a radius-1 sphere exactly at the sqrt(2)/2 diagonal
        dir = Vec3(1, 0, 0)
        pos, obj = scene.raymarch(Vec3(-3, .707, 0.), dir)
        self.assertEqual(scene, obj)
        self.assertEqual(Vec3(-.707, .707, 0), pos.rounded(3))

        norm = scene.normal(pos)
        self.assertEqual(Vec3(-.707, .707, 0), norm.rounded(3))

        refl = dir.reflected(norm)
        self.assertEqual(Vec3(0, 1, 0), refl.rounded(3))

    def test_reflect_translated(self):
        sphere = Sphere()
        scene = sphere.translate((0, 1, 0))

        # hit a radius-1 sphere exactly at the sqrt(2)/2 diagonal
        dir = Vec3(1, 0, 0)
        pos, obj = scene.raymarch(Vec3(-3, 1.707, 0.), dir)
        self.assertEqual(sphere, obj)
        self.assertEqual(Vec3(-.707, 1.707, 0), pos.rounded(3))

        norm = scene.normal(pos)
        self.assertEqual(Vec3(-.707, .707, 0), norm.rounded(3))

        refl = dir.reflected(norm)
        self.assertEqual(Vec3(0, 1, 0), refl.rounded(3))
