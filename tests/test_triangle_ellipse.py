# -*- coding: utf-8 -*-
"""
tests/test_triangle_ellipse.py

Triangle 和 Ellipse 单元测试

版本: 0.01
作者: wangheng <wangfaofao@gmail.com>
"""

import unittest
import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from planar_geometry import Point2D, Triangle, Ellipse, Circle


class TestTriangleCreation(unittest.TestCase):
    """Triangle 创建测试"""

    def test_from_points(self):
        """测试从点创建"""
        tri = Triangle.from_points([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertEqual(len(tri.vertices), 3)

    def test_from_sides(self):
        """测试从边长创建"""
        tri = Triangle.from_sides(3.0, 4.0, 5.0)
        self.assertIsNotNone(tri)

    def test_invalid_sides(self):
        """测试无效边长"""
        with self.assertRaises(ValueError):
            Triangle.from_sides(1.0, 1.0, 3.0)

    def test_invalid_vertex_count(self):
        """测试无效顶点数"""
        with self.assertRaises(ValueError):
            Triangle([Point2D(0, 0), Point2D(1, 0)])


class TestTriangleArea(unittest.TestCase):
    """Triangle 面积测试"""

    def test_right_triangle_area(self):
        """测试直角三角形面积"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertEqual(tri.area(), 6.0)

    def test_from_sides_area(self):
        """测试从边长创建的三角形面积"""
        tri = Triangle.from_sides(3.0, 4.0, 5.0)
        self.assertAlmostEqual(tri.area(), 6.0)


class TestTriangleSideLengths(unittest.TestCase):
    """Triangle 边长测试"""

    def test_get_side_lengths(self):
        """测试获取边长"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        a, b, c = tri.get_side_lengths()
        self.assertEqual(a, 3.0)
        self.assertEqual(b, 5.0)
        self.assertEqual(c, 4.0)


class TestTriangleAngles(unittest.TestCase):
    """Triangle 角度测试"""

    def test_right_triangle_angles(self):
        """测试直角三角形角度"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        angles = tri.get_angles()
        self.assertAlmostEqual(angles[0], 36.87, places=1)
        self.assertAlmostEqual(angles[1], 90.0, places=1)
        self.assertAlmostEqual(angles[2], 53.13, places=1)

    def test_angles_sum(self):
        """测试角度和为180"""
        tri = Triangle([Point2D(0, 0), Point2D(4, 0), Point2D(1, 3)])
        angles = tri.get_angles()
        self.assertAlmostEqual(sum(angles), 180.0)


class TestTriangleCenters(unittest.TestCase):
    """Triangle 中心点测试"""

    def test_circumcenter(self):
        """测试外心"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        circum = tri.circumcenter()
        self.assertIsInstance(circum, Point2D)

    def test_incenter(self):
        """测试内心"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        incenter = tri.incenter()
        self.assertIsInstance(incenter, Point2D)

    def test_orthocenter(self):
        """测试垂心"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        ortho = tri.orthocenter()
        self.assertIsInstance(ortho, Point2D)

    def test_centroid(self):
        """测试重心"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        centroid = tri.centroid()
        self.assertIsInstance(centroid, Point2D)


class TestTriangleRadius(unittest.TestCase):
    """Triangle 半径测试"""

    def test_circumradius(self):
        """测试外接圆半径"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertAlmostEqual(tri.circumradius(), 2.5)

    def test_inradius(self):
        """测试内切圆半径"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertEqual(tri.inradius(), 1.0)


class TestTriangleType(unittest.TestCase):
    """Triangle 类型判断测试"""

    def test_right_angled(self):
        """测试直角三角形判断"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertTrue(tri.is_right_angled())

    def test_not_right_angled(self):
        """测试非直角三角形"""
        tri = Triangle([Point2D(0, 0), Point2D(4, 0), Point2D(1, 3)])
        self.assertFalse(tri.is_right_angled())

    def test_equilateral(self):
        """测试等边三角形"""
        tri = Triangle([Point2D(0, 0), Point2D(1, 0), Point2D(0.5, math.sqrt(3) / 2)])
        self.assertTrue(tri.is_equilateral())

    def test_isosceles(self):
        """测试等腰三角形"""
        tri = Triangle([Point2D(0, 0), Point2D(2, 0), Point2D(1, 1)])
        self.assertTrue(tri.is_isosceles())


class TestTriangleCircle(unittest.TestCase):
    """Triangle 圆形测试"""

    def test_circumcircle(self):
        """测试外接圆"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        circle = tri.get_circumcircle()
        self.assertIsInstance(circle, Circle)
        self.assertAlmostEqual(circle.radius, 2.5)

    def test_incircle(self):
        """测试内切圆"""
        tri = Triangle([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        circle = tri.get_incicle()
        self.assertIsInstance(circle, Circle)
        self.assertEqual(circle.radius, 1.0)


class TestEllipseCreation(unittest.TestCase):
    """Ellipse 创建测试"""

    def test_basic_creation(self):
        """测试基本创建"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        self.assertEqual(ellipse.center.x, 0.0)
        self.assertEqual(ellipse.semi_major, 5.0)
        self.assertEqual(ellipse.semi_minor, 3.0)

    def test_from_center_and_axes(self):
        """测试工厂方法"""
        ellipse = Ellipse.from_center_and_axes(Point2D(0, 0), 10.0, 6.0)
        self.assertEqual(ellipse.semi_major, 5.0)
        self.assertEqual(ellipse.semi_minor, 3.0)

    def test_from_foci_and_point(self):
        """测试从焦点创建"""
        ellipse = Ellipse.from_foci_and_point(
            Point2D(-4, 0), Point2D(4, 0), Point2D(0, 3)
        )
        self.assertIsNotNone(ellipse)

    def test_invalid_semi_axis(self):
        """测试无效半轴"""
        with self.assertRaises(ValueError):
            Ellipse(Point2D(0, 0), -1.0, 1.0)

    def test_semi_major_less_than_minor(self):
        """测试semi_major < semi_minor"""
        with self.assertRaises(ValueError):
            Ellipse(Point2D(0, 0), 3.0, 5.0)


class TestEllipseArea(unittest.TestCase):
    """Ellipse 面积测试"""

    def test_area(self):
        """测试面积计算"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        self.assertAlmostEqual(ellipse.area(), 15 * math.pi)

    def test_circle_as_ellipse(self):
        """测试圆作为特殊椭圆"""
        circle = Ellipse(Point2D(0, 0), 5.0, 5.0)
        self.assertAlmostEqual(circle.area(), 25 * math.pi)


class TestEllipsePerimeter(unittest.TestCase):
    """Ellipse 周长测试"""

    def test_perimeter(self):
        """测试周长计算"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        perimeter = ellipse.perimeter()
        self.assertGreater(perimeter, 0)
        self.assertLess(perimeter, 2 * math.pi * 5)


class TestEllipseEccentricity(unittest.TestCase):
    """Ellipse 离心率测试"""

    def test_eccentricity(self):
        """测试离心率"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        e = ellipse.eccentricity()
        self.assertGreater(e, 0)
        self.assertLess(e, 1)
        self.assertAlmostEqual(e, 0.8)

    def test_circle_eccentricity(self):
        """测试圆离心率为0"""
        circle = Ellipse(Point2D(0, 0), 5.0, 5.0)
        self.assertEqual(circle.eccentricity(), 0.0)


class TestEllipseFocal(unittest.TestCase):
    """Ellipse 焦点测试"""

    def test_focal_distance(self):
        """测试焦距"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        self.assertAlmostEqual(ellipse.focal_distance(), 4.0)

    def test_foci(self):
        """测试焦点坐标"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        f1, f2 = ellipse.foci()
        self.assertAlmostEqual(f1.x, -4.0)
        self.assertAlmostEqual(f1.y, 0.0)
        self.assertAlmostEqual(f2.x, 4.0)
        self.assertAlmostEqual(f2.y, 0.0)


class TestEllipseBounds(unittest.TestCase):
    """Ellipse 边界测试"""

    def test_get_bounds(self):
        """测试获取边界框"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        bounds = ellipse.get_bounds()
        self.assertEqual(bounds[0], -5.0)
        self.assertEqual(bounds[1], -3.0)
        self.assertEqual(bounds[2], 5.0)
        self.assertEqual(bounds[3], 3.0)


class TestEllipseContains(unittest.TestCase):
    """Ellipse 点包含测试"""

    def test_contains_center(self):
        """测试中心点"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        self.assertTrue(ellipse.contains_point(Point2D(0, 0)))

    def test_contains_inside(self):
        """测试内部点"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        self.assertTrue(ellipse.contains_point(Point2D(2, 1)))

    def test_contains_on_boundary(self):
        """测试边界点"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        self.assertTrue(ellipse.contains_point(Point2D(5, 0)))

    def test_contains_outside(self):
        """测试外部点"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        self.assertFalse(ellipse.contains_point(Point2D(6, 0)))


class TestEllipseAxes(unittest.TestCase):
    """Ellipse 轴端点测试"""

    def test_major_axis_endpoints(self):
        """测试长轴端点"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        end1, end2 = ellipse.get_major_axis_endpoints()
        self.assertAlmostEqual(end1.x, -5.0)
        self.assertAlmostEqual(end2.x, 5.0)

    def test_minor_axis_endpoints(self):
        """测试短轴端点"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        end1, end2 = ellipse.get_minor_axis_endpoints()
        self.assertAlmostEqual(end1.y, -3.0)
        self.assertAlmostEqual(end2.y, 3.0)


class TestEllipseEquals(unittest.TestCase):
    """Ellipse 相等测试"""

    def test_equals(self):
        """测试相等"""
        e1 = Ellipse(Point2D(0, 0), 5.0, 3.0)
        e2 = Ellipse(Point2D(0, 0), 5.0, 3.0)
        self.assertEqual(e1, e2)

    def test_not_equals(self):
        """测试不等"""
        e1 = Ellipse(Point2D(0, 0), 5.0, 3.0)
        e2 = Ellipse(Point2D(1, 0), 5.0, 3.0)
        self.assertNotEqual(e1, e2)


class TestEllipseRotation(unittest.TestCase):
    """Ellipse 旋转测试"""

    def test_rotated_ellipse(self):
        """测试旋转椭圆"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0, rotation=45.0)
        self.assertEqual(ellipse.rotation, 45.0)

    def test_rotated_ellipse_contains(self):
        """测试旋转椭圆点包含"""
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0, rotation=45.0)
        self.assertTrue(ellipse.contains_point(Point2D(0, 0)))


if __name__ == "__main__":
    unittest.main()
