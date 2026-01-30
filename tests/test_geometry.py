# -*- coding: utf-8 -*-
"""
tests/test_point.py

Point2D 单元测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from planar_geometry import Point2D, Vector2D, Rectangle


class TestPoint2D(unittest.TestCase):
    """Point2D 测试类"""

    def test_creation(self):
        """测试点创建"""
        p = Point2D(3.0, 4.0)
        self.assertEqual(p.x, 3.0)
        self.assertEqual(p.y, 4.0)

    def test_length(self):
        """测试点长度（应为0）"""
        p = Point2D(1.0, 2.0)
        self.assertEqual(p.length(), 0.0)

    def test_distance_to(self):
        """测试两点距离"""
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        self.assertEqual(p1.distance_to(p2), 5.0)

    def test_scalar_multiplication(self):
        """测试标量乘法"""
        p = Point2D(1, 2)
        p2 = p * 2
        self.assertEqual(p2.x, 2)
        self.assertEqual(p2.y, 4)

    def test_equality(self):
        """测试相等判断"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(1.0, 2.0)
        self.assertEqual(p1, p2)

    def test_repr(self):
        """测试字符串表示"""
        p = Point2D(1.0, 2.0)
        self.assertEqual(repr(p), "Point2D(1.0, 2.0)")


class TestVector2D(unittest.TestCase):
    """Vector2D 测试类"""

    def test_creation(self):
        """测试向量创建"""
        v = Vector2D(3.0, 4.0)
        self.assertEqual(v.x, 3.0)
        self.assertEqual(v.y, 4.0)

    def test_length(self):
        """测试向量模长"""
        v = Vector2D(3.0, 4.0)
        self.assertEqual(v.length(), 5.0)

    def test_normalized(self):
        """测试向量归一化"""
        v = Vector2D(3.0, 4.0)
        v_norm = v.normalized()
        self.assertAlmostEqual(v_norm.length(), 1.0)

    def test_angle(self):
        """测试向量角度"""
        v = Vector2D(1.0, 0.0)
        self.assertEqual(v.angle(), 0.0)

        v = Vector2D(0.0, 1.0)
        self.assertEqual(v.angle(), 90.0)

    def test_dot_product(self):
        """测试点积"""
        v1 = Vector2D(1.0, 0.0)
        v2 = Vector2D(0.0, 1.0)
        self.assertEqual(v1.dot(v2), 0.0)

        v3 = Vector2D(2.0, 3.0)
        v4 = Vector2D(4.0, 5.0)
        self.assertEqual(v3.dot(v4), 23.0)

    def test_cross_product(self):
        """测试叉积"""
        v1 = Vector2D(1.0, 0.0)
        v2 = Vector2D(0.0, 1.0)
        self.assertEqual(v1.cross(v2), 1.0)

    def test_addition(self):
        """测试向量加法"""
        v1 = Vector2D(1.0, 2.0)
        v2 = Vector2D(3.0, 4.0)
        v3 = v1 + v2
        self.assertEqual(v3.x, 4.0)
        self.assertEqual(v3.y, 6.0)

    def test_repr(self):
        """测试字符串表示"""
        v = Vector2D(3.0, 4.0)
        self.assertEqual(repr(v), "Vector2D(3.0, 4.0)")


class TestRectangle(unittest.TestCase):
    """Rectangle 测试类"""

    def test_factory_method(self):
        """测试工厂方法"""
        center = Point2D(0, 0)
        size = 2.0
        direction = Vector2D(1, 0)
        rect = Rectangle.from_center_and_size(center, size, direction)

        self.assertEqual(len(rect.vertices), 4)

    def test_area(self):
        """测试面积计算"""
        rect = Rectangle.from_center_and_size(Point2D(0, 0), 2.0, Vector2D(1, 0))
        self.assertEqual(rect.area(), 4.0)

    def test_perimeter(self):
        """测试周长计算"""
        rect = Rectangle.from_center_and_size(Point2D(0, 0), 2.0, Vector2D(1, 0))
        self.assertEqual(rect.perimeter(), 8.0)

    def test_get_center(self):
        """测试获取中心点"""
        rect = Rectangle.from_center_and_size(Point2D(0, 0), 2.0, Vector2D(1, 0))
        center = rect.get_center()
        self.assertEqual(center.x, 0.0)
        self.assertEqual(center.y, 0.0)

    def test_get_bounds(self):
        """测试获取边界框"""
        rect = Rectangle.from_center_and_size(Point2D(0, 0), 2.0, Vector2D(1, 0))
        bounds = rect.get_bounds()
        self.assertEqual(len(bounds), 4)


if __name__ == "__main__":
    unittest.main()
