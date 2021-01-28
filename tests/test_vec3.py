import math
import random
from unittest import TestCase

from src.vec import Vec3


class TestVec2(TestCase):

    def test_0010_assignment(self):
        self.assertEqual("Vec3(0, 0, 0)", str(Vec3()))
        self.assertEqual("Vec3(1, 1, 1)", str(Vec3(1)))
        self.assertEqual("Vec3(1, 2, 3)", str(Vec3(1, 2, 3)))
        self.assertEqual("Vec3(1, 2, 3)", str(Vec3((1, 2, 3))))

        #with self.assertRaises(TypeError):
        #    Vec3()

    def test_0020_equality(self):
        self.assertTrue(Vec3() == (0, 0, 0))
        self.assertTrue(Vec3(1, 2, 3) == (1, 2, 3))

        self.assertTrue(Vec3() != 0)
        self.assertTrue(Vec3() != 0)

    def test_0100_binary_op(self):
        self.assertEqual((1, 1, 1), Vec3() + 1)
        self.assertEqual((-1, -1, -1), Vec3() - 1)
        self.assertEqual((1, 2, 3), Vec3() + (1, 2, 3))
        self.assertEqual((-1, -2, -3), Vec3() - (1, 2, 3))

        self.assertEqual((1, 1, 1), 1 + Vec3())
        self.assertEqual((-1, -1, -1), 1 - Vec3(2))
        self.assertEqual((1, 2, 3), (1, 2, 3) + Vec3())
        self.assertEqual((0, 1, 2), (1, 2, 3) - Vec3(1))

    def test_0100_binary_op_inplace(self):
        v = Vec3()
        v += 1
        self.assertEqual((1, 1, 1), v)
