import unittest

from umath import *
from universe import *

class TestFeq(unittest.TestCase):
    def test_feq_zero(self):
        self.assertTrue(feq(0.0, 0.0))

    def test_feq_neq(self):
        self.assertFalse(feq(0.0, 10))
        self.assertFalse(feq(21.5, 22))

    def test_feq_exact(self):
        self.assertTrue(feq(1.12343, 1.12343))
        self.assertTrue(feq(23.15567, 23.15567))
        self.assertFalse(feq(23.15267, 23.15567))
        self.assertFalse(feq(23.15267, 23.15367))

    def test_feq_approx(self):
        self.assertTrue(feq(1.0000001, 1.0))
        self.assertTrue(feq(10.99999999901, 11))

class TestVec3(unittest.TestCase):
    def test_init(self):
        v1 = Vec3()
        self.assertTrue(v1.x == 0.0 and v1.y == 0.0 and v1.z == 0.0)

        v2 = Vec3(1, 2, 3)
        self.assertTrue(v2.x == 1.0 and v2.y == 2.0 and v2.z == 3.0)

        v3 = Vec3(x=1.1, y=12.3, z=5.99999)
        self.assertTrue(v3.x == 1.1 and v3.y == 12.3 and v3.z == 5.99999)

    def test_neg(self):
        v1 = -Vec3(1, 2, 3)
        self.assertTrue(v1.x == -1.0 and v1.y == -2.0 and v1.z == -3.0)

        v2 = -Vec3(-1, -2, 3)
        self.assertTrue(v2.x == 1.0 and v2.y == 2.0 and v2.z == -3.0)

    def test_add(self):
        v1 = Vec3(1, 2, 3)
        v2 = Vec3(3, 2, 1)
        sum = v1 + v2

        self.assertTrue(sum.x == 4.0 and sum.y == 4.0 and sum.z == 4.0)

    def test_sub(self):
        v1 = Vec3(1, 2, 3)
        v2 = Vec3(3, 2, 1)
        diff = v1 - v2

        self.assertTrue(diff.x == -2.0 and diff.y == 0.0 and diff.z == 2.0)

    def test_eq(self):
        v1 = Vec3(1, 2, 3)
        v2 = Vec3(0.999999, 2.0000001, 3.0000000003)
        self.assertTrue(v1 == v2)

        v1 = Vec3(1, 2, 3)
        v2 = Vec3(4, 5, 6)
        self.assertFalse(v1 == v2)

    def test_str(self):
        v = Vec3(1, 2, 3)
        self.assertEqual(str(v), '(1.0, 2.0, 3.0)')

class TestPointObject(unittest.TestCase):
    def test_init(self):
        po = PointObject()
        self.assertEqual(po._PointObject__pos, Vec3(0, 0, 0))
        self.assertEqual(po.vel, Vec3(0, 0, 0))
        self.assertEqual(po.mass, 1.0)
        self.assertEqual(po.X, [0.0])
        self.assertEqual(po.Y, [0.0])
        self.assertEqual(po.Z, [0.0])
        self.assertEqual(po.color, 'r')

        po = PointObject(pos=Vec3(1, 2, 3), vel=Vec3(4, 5, 6), mass=12, color='k')
        self.assertEqual(po._PointObject__pos, Vec3(1, 2, 3))
        self.assertEqual(po.vel, Vec3(4, 5, 6))
        self.assertEqual(po.mass, 12.0)
        self.assertEqual(po.X, [1.0])
        self.assertEqual(po.Y, [2.0])
        self.assertEqual(po.Z, [3.0])
        self.assertEqual(po.color, 'k')

    def test_get_pos(self):
        po = PointObject(pos=Vec3(12, 24, 48))
        self.assertEqual(po.get_pos(), Vec3(12, 24, 48))

        po = PointObject(pos=Vec3(1, 2, 3), vel=Vec3(1, 2, 3))
        self.assertEqual(po.get_pos(), Vec3(1, 2, 3))

    def test_set_pos(self):
        po = PointObject()
        po.set_pos(Vec3(12, 12, 12))
        self.assertEqual(po._PointObject__pos, Vec3(12, 12, 12))
        self.assertEqual(po.X, [0.0, 12.0])
        self.assertEqual(po.Y, [0.0, 12.0])
        self.assertEqual(po.Z, [0.0, 12.0])

        po.set_pos(Vec3(1, 2, 3))
        self.assertEqual(po._PointObject__pos, Vec3(1, 2, 3))
        self.assertEqual(po.X, [0.0, 12.0, 1.0])
        self.assertEqual(po.Y, [0.0, 12.0, 2.0])
        self.assertEqual(po.Z, [0.0, 12.0, 3.0])

    def test_str(self):
        po = PointObject(pos=Vec3(1, 2, 3), vel=Vec3(4, 5, 6), mass=21, color='k')
        self.assertEqual(str(po), f"PointObject(pos=(1.0, 2.0, 3.0), vel=(4.0, 5.0, 6.0), mass=21.0, color=k)")

# TODO: Test the NewtonianUniverse class

if __name__ == '__main__':
    unittest.main()
