# -*- coding: utf-8 -*-
"""
tests/test_curve.py

Curve 模块单元测试

版本: 0.01
作者: wangheng <wangfaofao@gmail.com>
"""

import unittest
import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from planar_geometry import Point2D, Vector2D, LineSegment, Line


class TestVector2DCreation(unittest.TestCase):
    """Vector2D 创建测试"""

    def test_basic_creation(self):
        """测试基本创建"""
        v = Vector2D(3.0, 4.0)
        self.assertEqual(v.x, 3.0)
        self.assertEqual(v.y, 4.0)

    def test_zero_creation(self):
        """测试创建零向量"""
        v = Vector2D(0.0, 0.0)
        self.assertEqual(v.x, 0.0)
        self.assertEqual(v.y, 0.0)


class TestVector2DLength(unittest.TestCase):
    """Vector2D 长度测试"""

    def test_length_3_4(self):
        """测试3-4-5三角形"""
        v = Vector2D(3.0, 4.0)
        self.assertEqual(v.length(), 5.0)

    def test_length_unit(self):
        """测试单位向量长度"""
        v = Vector2D(1.0, 0.0)
        self.assertEqual(v.length(), 1.0)

    def test_length_squared(self):
        """测试长度平方"""
        v = Vector2D(3.0, 4.0)
        self.assertEqual(v.length_squared(), 25.0)


class TestVector2DAngle(unittest.TestCase):
    """Vector2D 角度测试"""

    def test_angle_unit_x(self):
        """测试X轴单位向量角度"""
        v = Vector2D(1.0, 0.0)
        self.assertEqual(v.angle(), 0.0)

    def test_angle_unit_y(self):
        """测试Y轴单位向量角度"""
        v = Vector2D(0.0, 1.0)
        self.assertEqual(v.angle(), 90.0)

    def test_angle_negative_x(self):
        """测试负X轴方向角度"""
        v = Vector2D(-1.0, 0.0)
        self.assertEqual(v.angle(), 180.0)

    def test_angle_negative_y(self):
        """测试负Y轴方向角度"""
        v = Vector2D(0.0, -1.0)
        self.assertEqual(v.angle(), 270.0)

    def test_angle_diagonal(self):
        """测试对角线角度"""
        v = Vector2D(1.0, 1.0)
        self.assertAlmostEqual(v.angle(), 45.0)

    def test_angle_rad(self):
        """测试弧度"""
        v = Vector2D(1.0, 0.0)
        self.assertAlmostEqual(v.angle_rad(), 0.0)


class TestVector2DNormalized(unittest.TestCase):
    """Vector2D 归一化测试"""

    def test_normalized(self):
        """测试归一化"""
        v = Vector2D(3.0, 4.0)
        v_norm = v.normalized()
        self.assertAlmostEqual(v_norm.length(), 1.0)
        self.assertAlmostEqual(v_norm.x, 0.6)
        self.assertAlmostEqual(v_norm.y, 0.8)

    def test_normalized_zero(self):
        """测试零向量归一化"""
        v = Vector2D(0.0, 0.0)
        v_norm = v.normalized()
        self.assertEqual(v_norm.x, 0.0)
        self.assertEqual(v_norm.y, 0.0)


class TestVector2DOperations(unittest.TestCase):
    """Vector2D 运算测试"""

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

        v3 = Vector2D(2.0, 3.0)
        v4 = Vector2D(4.0, 5.0)
        self.assertEqual(v3.cross(v4), -2.0)

    def test_perpendicular(self):
        """测试垂直向量"""
        v = Vector2D(1.0, 0.0)
        perp = v.perpendicular()
        self.assertEqual(perp.x, 0.0)
        self.assertEqual(perp.y, 1.0)

    def test_rotated_90(self):
        """测试旋转90度"""
        v = Vector2D(1.0, 0.0)
        rotated = v.rotated(90)
        self.assertAlmostEqual(rotated.x, 0.0)
        self.assertAlmostEqual(rotated.y, 1.0)

    def test_rotated_45(self):
        """测试旋转45度"""
        v = Vector2D(1.0, 0.0)
        rotated = v.rotated(45)
        self.assertAlmostEqual(rotated.x, math.sqrt(2) / 2)
        self.assertAlmostEqual(rotated.y, math.sqrt(2) / 2)

    def test_projection(self):
        """测试投影：v1投影到v2方向"""
        v1 = Vector2D(4.0, 0.0)
        v2 = Vector2D(2.0, 2.0)
        proj = v1.projection(v2)
        # v1 在 v2 方向上的投影
        # v2_normalized = (1/sqrt(2), 1/sqrt(2))
        # proj = (v1 · v2_normalized) * v2_normalized
        #      = 4/sqrt(2) * (1/sqrt(2), 1/sqrt(2))
        #      = (2, 2)
        self.assertAlmostEqual(proj.x, 2.0)
        self.assertAlmostEqual(proj.y, 2.0)

    def test_component(self):
        """测试分量"""
        v = Vector2D(3.0, 4.0)
        comp = v.component(Vector2D(1.0, 0.0))
        self.assertEqual(comp, 3.0)


class TestVector2DArithmetic(unittest.TestCase):
    """Vector2D 算术测试"""

    def test_addition(self):
        """测试加法"""
        v1 = Vector2D(1.0, 2.0)
        v2 = Vector2D(3.0, 4.0)
        v3 = v1 + v2
        self.assertEqual(v3.x, 4.0)
        self.assertEqual(v3.y, 6.0)

    def test_subtraction(self):
        """测试减法"""
        v1 = Vector2D(5.0, 6.0)
        v2 = Vector2D(2.0, 3.0)
        v3 = v1 - v2
        self.assertEqual(v3.x, 3.0)
        self.assertEqual(v3.y, 3.0)

    def test_multiplication(self):
        """测试乘法"""
        v = Vector2D(1.0, 2.0)
        v2 = v * 2.0
        self.assertEqual(v2.x, 2.0)
        self.assertEqual(v2.y, 4.0)

    def test_right_multiplication(self):
        """测试右乘"""
        v = Vector2D(1.0, 2.0)
        v2 = 2.0 * v
        self.assertEqual(v2.x, 2.0)
        self.assertEqual(v2.y, 4.0)

    def test_division(self):
        """测试除法"""
        v = Vector2D(4.0, 6.0)
        v2 = v / 2.0
        self.assertEqual(v2.x, 2.0)
        self.assertEqual(v2.y, 3.0)

    def test_division_by_zero(self):
        """测试除零异常"""
        v = Vector2D(1.0, 2.0)
        with self.assertRaises(ValueError):
            v / 0.0

    def test_negate(self):
        """测试取负"""
        v = Vector2D(1.0, -2.0)
        neg = v.negate()
        self.assertEqual(neg.x, -1.0)
        self.assertEqual(neg.y, 2.0)


class TestVector2DUtility(unittest.TestCase):
    """Vector2D 工具测试"""

    def test_is_zero(self):
        """测试是否为零向量"""
        self.assertTrue(Vector2D(0.0, 0.0).is_zero())
        self.assertFalse(Vector2D(1.0, 0.0).is_zero())

    def test_equals(self):
        """测试相等"""
        v1 = Vector2D(1.0, 2.0)
        v2 = Vector2D(1.0, 2.0)
        self.assertTrue(v1.equals(v2))

    def test_to_tuple(self):
        """测试转换为元组"""
        v = Vector2D(1.0, 2.0)
        self.assertEqual(v.to_tuple(), (1.0, 2.0))

    def test_from_tuple(self):
        """测试从元组创建"""
        v = Vector2D.from_tuple((3.0, 4.0))
        self.assertEqual(v.x, 3.0)
        self.assertEqual(v.y, 4.0)

    def test_zero(self):
        """测试零向量工厂方法"""
        v = Vector2D.zero()
        self.assertEqual(v.x, 0.0)
        self.assertEqual(v.y, 0.0)

    def test_unit_x(self):
        """测试X轴单位向量"""
        v = Vector2D.unit_x()
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 0.0)

    def test_unit_y(self):
        """测试Y轴单位向量"""
        v = Vector2D.unit_y()
        self.assertEqual(v.x, 0.0)
        self.assertEqual(v.y, 1.0)

    def test_repr(self):
        """测试repr"""
        v = Vector2D(3.0, 4.0)
        self.assertEqual(repr(v), "Vector2D(3.0, 4.0)")


class TestLineSegmentCreation(unittest.TestCase):
    """LineSegment 创建测试"""

    def test_creation(self):
        """测试创建"""
        s = LineSegment(Point2D(0, 0), Point2D(3, 4))
        self.assertEqual(s.start.x, 0.0)
        self.assertEqual(s.start.y, 0.0)
        self.assertEqual(s.end.x, 3.0)
        self.assertEqual(s.end.y, 4.0)


class TestLineSegmentLength(unittest.TestCase):
    """LineSegment 长度测试"""

    def test_length(self):
        """测试长度"""
        s = LineSegment(Point2D(0, 0), Point2D(3, 4))
        self.assertEqual(s.length(), 5.0)


class TestLineSegmentMidpoint(unittest.TestCase):
    """LineSegment 中点测试"""

    def test_midpoint(self):
        """测试中点"""
        s = LineSegment(Point2D(0, 0), Point2D(4, 4))
        mid = s.midpoint()
        self.assertEqual(mid.x, 2.0)
        self.assertEqual(mid.y, 2.0)


class TestLineSegmentDirection(unittest.TestCase):
    """LineSegment 方向测试"""

    def test_direction(self):
        """测试方向"""
        s = LineSegment(Point2D(0, 0), Point2D(3, 4))
        direction = s.direction()
        self.assertAlmostEqual(direction.x, 0.6)
        self.assertAlmostEqual(direction.y, 0.8)


class TestLineSegmentContains(unittest.TestCase):
    """LineSegment 点包含测试"""

    def test_contains_endpoint(self):
        """测试端点"""
        s = LineSegment(Point2D(0, 0), Point2D(4, 0))
        self.assertTrue(s.contains_point(Point2D(0, 0)))
        self.assertTrue(s.contains_point(Point2D(4, 0)))

    def test_contains_middle(self):
        """测试中点"""
        s = LineSegment(Point2D(0, 0), Point2D(4, 0))
        self.assertTrue(s.contains_point(Point2D(2, 0)))

    def test_not_contains_outside(self):
        """测试外部点"""
        s = LineSegment(Point2D(0, 0), Point2D(4, 0))
        self.assertFalse(s.contains_point(Point2D(5, 0)))
        self.assertFalse(s.contains_point(Point2D(2, 1)))


class TestLineSegmentClosest(unittest.TestCase):
    """LineSegment 最近点测试"""

    def test_closest_point_on_segment(self):
        """测试线段上的最近点"""
        s = LineSegment(Point2D(0, 0), Point2D(4, 0))
        closest = s.get_closest_point(Point2D(2, 1))
        self.assertEqual(closest.x, 2.0)
        self.assertEqual(closest.y, 0.0)

    def test_closest_point_extension(self):
        """测试延长线上的最近点"""
        s = LineSegment(Point2D(0, 0), Point2D(4, 0))
        closest = s.get_closest_point(Point2D(5, 1))
        self.assertEqual(closest.x, 4.0)
        self.assertEqual(closest.y, 0.0)

    def test_distance_to_point(self):
        """测试点到线段距离"""
        s = LineSegment(Point2D(0, 0), Point2D(4, 0))
        distance = s.get_distance_to_point(Point2D(2, 1))
        self.assertEqual(distance, 1.0)


class TestLineSegmentParameter(unittest.TestCase):
    """LineSegment 参数测试"""

    def test_parameter_at_start(self):
        """测试起点参数"""
        s = LineSegment(Point2D(0, 0), Point2D(4, 0))
        t = s.get_parameter(Point2D(0, 0))
        self.assertEqual(t, 0.0)

    def test_parameter_at_end(self):
        """测试终点参数"""
        s = LineSegment(Point2D(0, 0), Point2D(4, 0))
        t = s.get_parameter(Point2D(4, 0))
        self.assertEqual(t, 1.0)

    def test_parameter_at_middle(self):
        """测试中点参数"""
        s = LineSegment(Point2D(0, 0), Point2D(4, 0))
        t = s.get_parameter(Point2D(2, 0))
        self.assertEqual(t, 0.5)


class TestLineCreation(unittest.TestCase):
    """Line 创建测试"""

    def test_creation(self):
        """测试创建"""
        l = Line(Point2D(0, 0), Vector2D(1, 1))
        self.assertEqual(l.point.x, 0.0)
        self.assertEqual(l.point.y, 0.0)


class TestLineLength(unittest.TestCase):
    """Line 长度测试"""

    def test_length_is_inf(self):
        """测试长度为无穷大"""
        l = Line(Point2D(0, 0), Vector2D(1, 1))
        self.assertEqual(l.length(), float("inf"))


class TestLineIntersection(unittest.TestCase):
    """Line 交点测试"""

    def test_intersection(self):
        """测试交点"""
        l1 = Line(Point2D(0, 0), Vector2D(1, 1))
        l2 = Line(Point2D(0, 2), Vector2D(1, -1))
        intersection = l1.get_intersection(l2)
        self.assertEqual(intersection.x, 1.0)
        self.assertEqual(intersection.y, 1.0)

    def test_parallel_lines(self):
        """测试平行线异常"""
        l1 = Line(Point2D(0, 0), Vector2D(1, 0))
        l2 = Line(Point2D(0, 1), Vector2D(1, 0))
        with self.assertRaises(ValueError):
            l1.get_intersection(l2)


class TestLineDistance(unittest.TestCase):
    """Line 距离测试"""

    def test_distance_to_point(self):
        """测试点到直线距离"""
        l = Line(Point2D(0, 0), Vector2D(1, 0))
        distance = l.get_distance_to_point(Point2D(0, 1))
        self.assertEqual(distance, 1.0)

    def test_closest_point(self):
        """测试最近点（垂足）"""
        l = Line(Point2D(0, 0), Vector2D(1, 0))
        closest = l.get_closest_point(Point2D(2, 1))
        self.assertEqual(closest.x, 2.0)
        self.assertEqual(closest.y, 0.0)


if __name__ == "__main__":
    unittest.main()
