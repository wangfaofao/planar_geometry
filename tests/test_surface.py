# -*- coding: utf-8 -*-
"""
tests/test_surface.py

Surface 模块单元测试

版本: 0.01
作者: wangheng <wangfaofao@gmail.com>
"""

import unittest
import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from planar_geometry import Point2D, Vector2D, Rectangle, Circle, Polygon


class TestRectangleCreation(unittest.TestCase):
    """Rectangle 创建测试"""

    def test_from_center_and_size(self):
        """测试工厂方法"""
        rect = Rectangle.from_center_and_size(Point2D(0, 0), 2.0, Vector2D(1, 0))
        self.assertEqual(len(rect.vertices), 4)

    def test_from_bounds(self):
        """测试从边界创建"""
        rect = Rectangle.from_bounds(0, 0, 4, 3)
        self.assertEqual(rect.area(), 12.0)

    def test_invalid_vertices(self):
        """测试无效顶点数"""
        with self.assertRaises(ValueError):
            Rectangle([Point2D(0, 0), Point2D(1, 0), Point2D(0, 1)])


class TestRectangleArea(unittest.TestCase):
    """Rectangle 面积测试"""

    def test_area(self):
        """测试面积计算"""
        rect = Rectangle.from_center_and_size(Point2D(0, 0), 2.0, Vector2D(1, 0))
        self.assertEqual(rect.area(), 4.0)

    def test_rotated_rectangle_area(self):
        """测试旋转矩形面积"""
        rect = Rectangle.from_center_and_size(
            Point2D(0, 0), 2.0, Vector2D(1, 1).normalized()
        )
        self.assertAlmostEqual(rect.area(), 4.0)


class TestRectanglePerimeter(unittest.TestCase):
    """Rectangle 周长测试"""

    def test_perimeter(self):
        """测试周长计算"""
        rect = Rectangle.from_center_and_size(Point2D(0, 0), 2.0, Vector2D(1, 0))
        self.assertEqual(rect.perimeter(), 8.0)


class TestRectangleBounds(unittest.TestCase):
    """Rectangle 边界测试"""

    def test_get_bounds(self):
        """测试获取边界框"""
        rect = Rectangle.from_bounds(0, 0, 4, 3)
        bounds = rect.get_bounds()
        self.assertEqual(bounds, (0, 0, 4, 3))


class TestRectangleCenter(unittest.TestCase):
    """Rectangle 中心测试"""

    def test_get_center(self):
        """测试获取中心"""
        rect = Rectangle.from_bounds(0, 0, 4, 4)
        center = rect.get_center()
        self.assertEqual(center.x, 2.0)
        self.assertEqual(center.y, 2.0)


class TestRectangleContains(unittest.TestCase):
    """Rectangle 点包含测试"""

    def test_contains_inside(self):
        """测试内部点"""
        rect = Rectangle.from_bounds(0, 0, 4, 4)
        self.assertTrue(rect.contains_point(Point2D(2, 2)))

    def test_contains_boundary(self):
        """测试边界点"""
        rect = Rectangle.from_bounds(0, 0, 4, 4)
        self.assertTrue(rect.contains_point(Point2D(0, 2)))

    def test_contains_outside(self):
        """测试外部点"""
        rect = Rectangle.from_bounds(0, 0, 4, 4)
        self.assertFalse(rect.contains_point(Point2D(5, 2)))


class TestRectangleIsSquare(unittest.TestCase):
    """Rectangle 正方形测试"""

    def test_is_square(self):
        """测试正方形判断"""
        rect = Rectangle.from_center_and_size(Point2D(0, 0), 2.0, Vector2D(1, 0))
        self.assertTrue(rect.is_square())

    def test_not_square(self):
        """测试非正方形"""
        rect = Rectangle.from_bounds(0, 0, 4, 2)
        self.assertFalse(rect.is_square())


class TestCircleCreation(unittest.TestCase):
    """Circle 创建测试"""

    def test_basic_creation(self):
        """测试基本创建"""
        circle = Circle(Point2D(0, 0), 5.0)
        self.assertEqual(circle.center.x, 0.0)
        self.assertEqual(circle.center.y, 0.0)
        self.assertEqual(circle.radius, 5.0)

    def test_from_diameter(self):
        """测试从直径创建"""
        circle = Circle.from_diameter(Point2D(0, 0), Point2D(4, 0))
        self.assertEqual(circle.center.x, 2.0)
        self.assertEqual(circle.radius, 2.0)

    def test_negative_radius(self):
        """测试负半径异常"""
        with self.assertRaises(ValueError):
            Circle(Point2D(0, 0), -1.0)


class TestCircleArea(unittest.TestCase):
    """Circle 面积测试"""

    def test_area(self):
        """测试面积计算"""
        circle = Circle(Point2D(0, 0), 1.0)
        self.assertAlmostEqual(circle.area(), math.pi)

    def test_area_r5(self):
        """测试半径5的圆面积"""
        circle = Circle(Point2D(0, 0), 5.0)
        self.assertAlmostEqual(circle.area(), 25 * math.pi)


class TestCirclePerimeter(unittest.TestCase):
    """Circle 周长测试"""

    def test_perimeter(self):
        """测试周长计算"""
        circle = Circle(Point2D(0, 0), 1.0)
        self.assertAlmostEqual(circle.perimeter(), 2 * math.pi)


class TestCircleContains(unittest.TestCase):
    """Circle 点包含测试"""

    def test_contains_inside(self):
        """测试内部点"""
        circle = Circle(Point2D(0, 0), 5.0)
        self.assertTrue(circle.contains_point(Point2D(0, 0)))
        self.assertTrue(circle.contains_point(Point2D(3, 4)))

    def test_contains_boundary(self):
        """测试边界点"""
        circle = Circle(Point2D(0, 0), 5.0)
        self.assertTrue(circle.contains_point(Point2D(5, 0)))

    def test_contains_outside(self):
        """测试外部点"""
        circle = Circle(Point2D(0, 0), 5.0)
        self.assertFalse(circle.contains_point(Point2D(6, 0)))


class TestCircleEquals(unittest.TestCase):
    """Circle 相等测试"""

    def test_equals(self):
        """测试相等"""
        c1 = Circle(Point2D(0, 0), 5.0)
        c2 = Circle(Point2D(0, 0), 5.0)
        self.assertEqual(c1, c2)

    def test_not_equals(self):
        """测试不等"""
        c1 = Circle(Point2D(0, 0), 5.0)
        c2 = Circle(Point2D(1, 0), 5.0)
        self.assertNotEqual(c1, c2)


class TestPolygonCreation(unittest.TestCase):
    """Polygon 创建测试"""

    def test_triangle(self):
        """测试三角形"""
        tri = Polygon([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertEqual(len(tri.vertices), 3)

    def test_quadrilateral(self):
        """测试四边形"""
        quad = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        self.assertEqual(len(quad.vertices), 4)

    def test_invalid_vertices(self):
        """测试无效顶点数"""
        with self.assertRaises(ValueError):
            Polygon([Point2D(0, 0), Point2D(1, 0)])

    def test_from_points(self):
        """测试工厂方法"""
        points = [Point2D(0, 0), Point2D(1, 0), Point2D(0, 1)]
        poly = Polygon.from_points(points)
        self.assertEqual(len(poly.vertices), 3)

    def test_regular_polygon(self):
        """测试正多边形"""
        hex = Polygon.regular(6, Point2D(0, 0), 1.0)
        self.assertEqual(len(hex.vertices), 6)

    def test_triangle_factory(self):
        """测试三角形工厂"""
        tri = Polygon.triangle(Point2D(0, 0), Point2D(3, 0), Point2D(0, 4))
        self.assertEqual(len(tri.vertices), 3)


class TestPolygonArea(unittest.TestCase):
    """Polygon 面积测试"""

    def test_triangle_area(self):
        """测试三角形面积"""
        tri = Polygon([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertEqual(tri.area(), 6.0)

    def test_quadrilateral_area(self):
        """测试四边形面积"""
        quad = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        self.assertEqual(quad.area(), 12.0)

    def test_regular_hexagon_area(self):
        """测试正六边形面积"""
        hex = Polygon.regular(6, Point2D(0, 0), 1.0)
        self.assertAlmostEqual(hex.area(), 2.598, places=3)


class TestPolygonPerimeter(unittest.TestCase):
    """Polygon 周长测试"""

    def test_triangle_perimeter(self):
        """测试三角形周长"""
        tri = Polygon([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertAlmostEqual(tri.perimeter(), 12.0)


class TestPolygonBounds(unittest.TestCase):
    """Polygon 边界测试"""

    def test_get_bounds(self):
        """测试获取边界框"""
        quad = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        bounds = quad.get_bounds()
        self.assertEqual(bounds, (0, 0, 4, 3))


class TestPolygonCenter(unittest.TestCase):
    """Polygon 中心测试"""

    def test_get_center(self):
        """测试获取中心"""
        quad = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        center = quad.get_center()
        self.assertEqual(center.x, 2.0)
        self.assertEqual(center.y, 1.5)


class TestPolygonContains(unittest.TestCase):
    """Polygon 点包含测试"""

    def test_triangle_contains(self):
        """测试三角形点包含"""
        tri = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(0, 3)])
        self.assertTrue(tri.contains_point(Point2D(1, 1)))
        self.assertFalse(tri.contains_point(Point2D(2, 2)))

    def test_quad_contains(self):
        """测试四边形点包含"""
        quad = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        self.assertTrue(quad.contains_point(Point2D(2, 1.5)))

    def test_boundary_contains(self):
        """测试边界点包含"""
        quad = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        self.assertTrue(quad.contains_point(Point2D(2, 0)))


class TestPolygonConvex(unittest.TestCase):
    """Polygon 凸性测试"""

    def test_convex_triangle(self):
        """测试三角形是凸的"""
        tri = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(0, 3)])
        self.assertTrue(tri.is_convex())

    def test_convex_quad(self):
        """测试凸四边形"""
        quad = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        self.assertTrue(quad.is_convex())

    def test_concave_polygon(self):
        """测试凹多边形"""
        concave = Polygon(
            [Point2D(0, 0), Point2D(4, 0), Point2D(2, 1), Point2D(4, 4), Point2D(0, 4)]
        )
        self.assertFalse(concave.is_convex())


class TestPolygonSimple(unittest.TestCase):
    """Polygon 简单性测试"""

    def test_simple_polygon(self):
        """测试简单多边形"""
        quad = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        self.assertTrue(quad.is_simple())


class TestPolygonRegular(unittest.TestCase):
    """Polygon 正则性测试"""

    def test_regular_hexagon(self):
        """测试正六边形"""
        hex = Polygon.regular(6, Point2D(0, 0), 1.0)
        self.assertTrue(hex.is_regular())

    def test_not_regular(self):
        """测试非正多边形"""
        quad = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        self.assertFalse(quad.is_regular())


class TestPolygonVertexEdge(unittest.TestCase):
    """Polygon 顶点和边测试"""

    def test_get_vertex_count(self):
        """测试获取顶点数"""
        tri = Polygon([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertEqual(tri.get_vertex_count(), 3)

    def test_get_edge_count(self):
        """测试获取边数"""
        tri = Polygon([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertEqual(tri.get_edge_count(), 3)

    def test_get_vertex(self):
        """测试获取顶点"""
        tri = Polygon([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        self.assertEqual(tri.get_vertex(0), Point2D(0, 0))
        self.assertEqual(tri.get_vertex(1), Point2D(3, 0))
        self.assertEqual(tri.get_vertex(2), Point2D(0, 4))
        self.assertEqual(tri.get_vertex(3), Point2D(0, 0))  # 循环
        self.assertEqual(tri.get_vertex(-1), Point2D(0, 4))  # 负索引

    def test_get_edge(self):
        """测试获取边"""
        tri = Polygon([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
        edge = tri.get_edge(0)
        self.assertEqual(edge[0], Point2D(0, 0))
        self.assertEqual(edge[1], Point2D(3, 0))


class TestPolygonConvexHull(unittest.TestCase):
    """Polygon 凸包测试"""

    def test_convex_hull_triangle(self):
        """测试三角形凸包"""
        points = [Point2D(0, 0), Point2D(1, 0), Point2D(0, 1)]
        poly = Polygon(points)
        hull = poly.get_convex_hull()
        self.assertEqual(hull.get_vertex_count(), 3)


if __name__ == "__main__":
    unittest.main()
