import math
import random
from unittest import TestCase
import doctest

from src.vec import Vec2, vec2


class TestVec2(TestCase):

    def test_0000_doctest(self):
        result = doctest.testmod(vec2)
        if result.failed:
            raise AssertionError(f"{result.failed} failures in doctest")

    def test_0010_assignment(self):
        self.assertEqual("Vec2(0, 0)", str(Vec2()))
        self.assertEqual("Vec2(1, 1)", str(Vec2(1)))
        self.assertEqual("Vec2(1, 2)", str(Vec2(1, 2)))
        self.assertEqual("Vec2(1, 2)", str(Vec2((1, 2))))

    def test_0020_equality(self):
        self.assertTrue(Vec2() == (0, 0))
        self.assertTrue(Vec2(1, 2) == (1, 2))

        self.assertTrue(Vec2() != 0)

    def test_0100_binary_op(self):
        self.assertEqual((1, 1), Vec2() + 1)
        self.assertEqual((-1, -1), Vec2() - 1)
        self.assertEqual((1, 2), Vec2() + (1, 2))
        self.assertEqual((-1, -2), Vec2() - (1, 2))

        self.assertEqual((1, 1), 1 + Vec2())
        self.assertEqual((-1, -1), 1 - Vec2(2))
        self.assertEqual((1, 2), (1, 2) + Vec2())
        self.assertEqual((0, 1), (1, 2) - Vec2(1))

    def test_0100_binary_op_inplace(self):
        v = Vec2()
        v += 1
        self.assertEqual((1, 1), v)
