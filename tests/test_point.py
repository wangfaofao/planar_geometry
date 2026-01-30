# -*- coding: utf-8 -*-
"""
tests/test_point.py

Point2D 单元测试

版本: 0.01
作者: wangheng <wangfaofao@gmail.com>
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from planar_geometry import Point2D


class TestPoint2DCreation(unittest.TestCase):
    """Point2D 创建测试"""

    def test_basic_creation(self):
        """测试基本创建"""
        p = Point2D(3.0, 4.0)
        self.assertEqual(p.x, 3.0)
        self.assertEqual(p.y, 4.0)

    def test_zero_creation(self):
        """测试创建零点"""
        p = Point2D(0.0, 0.0)
        self.assertEqual(p.x, 0.0)
        self.assertEqual(p.y, 0.0)

    def test_negative_coordinates(self):
        """测试负坐标"""
        p = Point2D(-1.5, -2.5)
        self.assertEqual(p.x, -1.5)
        self.assertEqual(p.y, -2.5)


class TestPoint2DLength(unittest.TestCase):
    """Point2D 长度测试"""

    def test_length_is_zero(self):
        """测试点长度为0"""
        p = Point2D(1.0, 2.0)
        self.assertEqual(p.length(), 0.0)


class TestPoint2DDistance(unittest.TestCase):
    """Point2D 距离测试"""

    def test_distance_to_origin(self):
        """测试到原点距离"""
        p = Point2D(3.0, 4.0)
        self.assertEqual(p.distance_to(Point2D(0.0, 0.0)), 5.0)

    def test_distance_to_self(self):
        """测试到自身距离"""
        p = Point2D(1.0, 2.0)
        self.assertEqual(p.distance_to(p), 0.0)

    def test_horizontal_distance(self):
        """测试水平距离"""
        p1 = Point2D(0.0, 0.0)
        p2 = Point2D(3.0, 0.0)
        self.assertEqual(p1.distance_to(p2), 3.0)

    def test_vertical_distance(self):
        """测试垂直距离"""
        p1 = Point2D(0.0, 0.0)
        p2 = Point2D(0.0, 4.0)
        self.assertEqual(p1.distance_to(p2), 4.0)

    def test_distance_squared(self):
        """测试距离平方"""
        p = Point2D(3.0, 4.0)
        self.assertEqual(p.distance_squared_to(Point2D(0.0, 0.0)), 25.0)


class TestPoint2DMidpoint(unittest.TestCase):
    """Point2D 中点测试"""

    def test_midpoint_basic(self):
        """测试基本中点"""
        p1 = Point2D(0.0, 0.0)
        p2 = Point2D(4.0, 4.0)
        mid = p1.midpoint_to(p2)
        self.assertEqual(mid.x, 2.0)
        self.assertEqual(mid.y, 2.0)

    def test_midpoint_symmetry(self):
        """测试中点对称性"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(5.0, 6.0)
        mid = p1.midpoint_to(p2)
        self.assertEqual(p1.midpoint_to(p2), p2.midpoint_to(p1))
        self.assertEqual(mid.x, 3.0)
        self.assertEqual(mid.y, 4.0)


class TestPoint2DArithmetic(unittest.TestCase):
    """Point2D 算术运算测试"""

    def test_add(self):
        """测试加法"""
        p = Point2D(1.0, 2.0)
        result = p + (3.0, 4.0)
        self.assertEqual(result.x, 4.0)
        self.assertEqual(result.y, 6.0)

    def test_subtract(self):
        """测试减法"""
        p1 = Point2D(5.0, 6.0)
        p2 = Point2D(2.0, 3.0)
        result = p1 - p2
        self.assertEqual(result, (3.0, 3.0))

    def test_scalar_multiplication(self):
        """测试标量乘法"""
        p = Point2D(1.0, 2.0)
        result = p * 2.0
        self.assertEqual(result.x, 2.0)
        self.assertEqual(result.y, 4.0)

    def test_right_scalar_multiplication(self):
        """测试右乘标量"""
        p = Point2D(1.0, 2.0)
        result = 2.0 * p
        self.assertEqual(result.x, 2.0)
        self.assertEqual(result.y, 4.0)

    def test_division(self):
        """测试除法"""
        p = Point2D(4.0, 6.0)
        result = p / 2.0
        self.assertEqual(result.x, 2.0)
        self.assertEqual(result.y, 3.0)

    def test_division_by_zero(self):
        """测试除零异常"""
        p = Point2D(1.0, 2.0)
        with self.assertRaises(ZeroDivisionError):
            p / 0.0

    def test_negate(self):
        """测试取负"""
        p = Point2D(1.0, -2.0)
        neg = p.negate()
        self.assertEqual(neg.x, -1.0)
        self.assertEqual(neg.y, 2.0)

    def test_add_method(self):
        """测试add方法"""
        p = Point2D(1.0, 2.0)
        result = p.add(3.0, 4.0)
        self.assertEqual(result.x, 4.0)
        self.assertEqual(result.y, 6.0)


class TestPoint2DEquality(unittest.TestCase):
    """Point2D 相等测试"""

    def test_equality(self):
        """测试相等"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(1.0, 2.0)
        self.assertEqual(p1, p2)

    def test_inequality(self):
        """测试不等"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(3.0, 4.0)
        self.assertNotEqual(p1, p2)

    def test_floating_point_equality(self):
        """测试浮点相等"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(1.0 + 1e-10, 2.0 - 1e-10)
        self.assertEqual(p1, p2)

    def test_equals_with_tolerance(self):
        """测试带容差相等"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(1.0 + 1e-8, 2.0)
        self.assertTrue(p1.equals(p2, tolerance=1e-6))
        self.assertFalse(p1.equals(p2, tolerance=1e-10))


class TestPoint2DUtility(unittest.TestCase):
    """Point2D 工具方法测试"""

    def test_is_zero(self):
        """测试是否为零点"""
        self.assertTrue(Point2D(0.0, 0.0).is_zero())
        self.assertFalse(Point2D(1.0, 0.0).is_zero())

    def test_to_tuple(self):
        """测试转换为元组"""
        p = Point2D(1.0, 2.0)
        self.assertEqual(p.to_tuple(), (1.0, 2.0))

    def test_from_tuple(self):
        """测试从元组创建"""
        p = Point2D.from_tuple((3.0, 4.0))
        self.assertEqual(p.x, 3.0)
        self.assertEqual(p.y, 4.0)

    def test_origin(self):
        """测试原点"""
        origin = Point2D.origin()
        self.assertEqual(origin.x, 0.0)
        self.assertEqual(origin.y, 0.0)

    def test_hash(self):
        """测试哈希"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(1.0, 2.0)
        self.assertEqual(hash(p1), hash(p2))

    def test_hash_uniqueness(self):
        """测试哈希唯一性"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(2.0, 1.0)
        self.assertNotEqual(hash(p1), hash(p2))

    def test_repr(self):
        """测试repr"""
        p = Point2D(1.0, 2.0)
        self.assertEqual(repr(p), "Point2D(1.0, 2.0)")

    def test_str(self):
        """测试str"""
        p = Point2D(1.5, 2.5)
        self.assertEqual(str(p), "(1.5, 2.5)")


class TestPoint2DInCollection(unittest.TestCase):
    """Point2D 集合测试"""

    def test_point_in_set(self):
        """测试点存在于集合"""
        s = {Point2D(1.0, 2.0), Point2D(3.0, 4.0)}
        self.assertIn(Point2D(1.0, 2.0), s)

    def test_point_as_dict_key(self):
        """测试点作为字典键"""
        d = {Point2D(1.0, 2.0): "test"}
        self.assertEqual(d[Point2D(1.0, 2.0)], "test")


if __name__ == "__main__":
    unittest.main()
