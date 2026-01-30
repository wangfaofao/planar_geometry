# -*- coding: utf-8 -*-
"""
tests/test_geometry_utils.py

几何工具函数单元测试

版本: 0.01
作者: wangheng <wangfaofao@gmail.com>
"""

import unittest
import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from planar_geometry import (
    Point2D,
    Vector2D,
    LineSegment,
    Line,
    Rectangle,
    Circle,
    Polygon,
    line_segment_intersection,
    line_intersection,
    rectangle_intersection_points,
    polygon_intersection_points,
    point_to_segment_distance,
    point_to_segment_closest_point,
    point_to_line_distance,
    point_to_line_closest_point,
    point_to_rectangle_distance,
    point_to_polygon_distance,
    angle_between,
    angle_between_rad,
    are_perpendicular,
    are_parallel,
    segments_distance,
    segments_closest_points,
    bounding_box,
    centroid,
)


class TestLineSegmentIntersection(unittest.TestCase):
    """线段交点测试"""

    def test_crossing_segments(self):
        """测试相交线段"""
        s1 = LineSegment(Point2D(0, 0), Point2D(2, 2))
        s2 = LineSegment(Point2D(0, 2), Point2D(2, 0))
        result = line_segment_intersection(s1, s2)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.x, 1.0)
        self.assertAlmostEqual(result.y, 1.0)

    def test_parallel_segments(self):
        """测试平行线段"""
        s1 = LineSegment(Point2D(0, 0), Point2D(2, 0))
        s2 = LineSegment(Point2D(0, 1), Point2D(2, 1))
        result = line_segment_intersection(s1, s2)
        self.assertIsNone(result)

    def test_no_intersection(self):
        """测试不相交线段"""
        s1 = LineSegment(Point2D(0, 0), Point2D(1, 0))
        s2 = LineSegment(Point2D(2, 0), Point2D(3, 0))
        result = line_segment_intersection(s1, s2)
        self.assertIsNone(result)


class TestLineIntersection(unittest.TestCase):
    """直线交点测试"""

    def test_intersecting_lines(self):
        """测试相交直线"""
        l1 = Line(Point2D(0, 0), Vector2D(1, 1))
        l2 = Line(Point2D(0, 2), Vector2D(1, -1))
        result = line_intersection(l1, l2)
        self.assertAlmostEqual(result.x, 1.0)
        self.assertAlmostEqual(result.y, 1.0)

    def test_parallel_lines(self):
        """测试平行直线异常"""
        l1 = Line(Point2D(0, 0), Vector2D(1, 0))
        l2 = Line(Point2D(0, 1), Vector2D(1, 0))
        with self.assertRaises(ValueError):
            line_intersection(l1, l2)


class TestRectangleIntersection(unittest.TestCase):
    """矩形交点测试"""

    def test_intersecting_rectangles(self):
        """测试相交矩形"""
        r1 = Rectangle.from_bounds(0, 0, 2, 2)
        r2 = Rectangle.from_bounds(1, 1, 3, 3)
        points = rectangle_intersection_points(r1, r2)
        self.assertEqual(len(points), 2)


class TestPolygonIntersection(unittest.TestCase):
    """多边形交点测试"""

    def test_intersecting_triangles(self):
        """测试相交三角形"""
        tri1 = Polygon([Point2D(0, 0), Point2D(2, 0), Point2D(1, 2)])
        tri2 = Polygon([Point2D(1, 1), Point2D(3, 1), Point2D(2, 3)])
        points = polygon_intersection_points(tri1, tri2)
        self.assertTrue(len(points) > 0)


class TestPointToSegmentDistance(unittest.TestCase):
    """点到线段距离测试"""

    def test_perpendicular_foot(self):
        """测试垂足在线段上"""
        segment = LineSegment(Point2D(0, 0), Point2D(4, 0))
        distance = point_to_segment_distance(Point2D(2, 3), segment)
        self.assertEqual(distance, 3.0)

    def test_extension_point(self):
        """测试垂足在线段延长线上"""
        segment = LineSegment(Point2D(0, 0), Point2D(2, 0))
        distance = point_to_segment_distance(Point2D(5, 2), segment)
        self.assertAlmostEqual(distance, math.sqrt(13))


class TestPointToSegmentClosestPoint(unittest.TestCase):
    """点到线段最近点测试"""

    def test_closest_point(self):
        """测试最近点"""
        segment = LineSegment(Point2D(0, 0), Point2D(4, 0))
        closest = point_to_segment_closest_point(Point2D(2, 3), segment)
        self.assertEqual(closest.x, 2.0)
        self.assertEqual(closest.y, 0.0)


class TestPointToLineDistance(unittest.TestCase):
    """点到直线距离测试"""

    def test_distance(self):
        """测试距离"""
        line = Line(Point2D(0, 0), Vector2D(1, 0))
        distance = point_to_line_distance(Point2D(2, 3), line)
        self.assertEqual(distance, 3.0)


class TestPointToLineClosestPoint(unittest.TestCase):
    """点到直线最近点测试"""

    def test_closest_point(self):
        """测试最近点（垂足）"""
        line = Line(Point2D(0, 0), Vector2D(1, 0))
        closest = point_to_line_closest_point(Point2D(2, 3), line)
        self.assertEqual(closest.x, 2.0)
        self.assertEqual(closest.y, 0.0)


class TestPointToRectangleDistance(unittest.TestCase):
    """点到矩形距离测试"""

    def test_inside(self):
        """测试点在矩形内"""
        rect = Rectangle.from_bounds(0, 0, 4, 3)
        distance = point_to_rectangle_distance(Point2D(2, 1), rect)
        self.assertEqual(distance, 0.0)

    def test_outside(self):
        """测试点在矩形外"""
        rect = Rectangle.from_bounds(0, 0, 4, 3)
        distance = point_to_rectangle_distance(Point2D(5, 1), rect)
        self.assertEqual(distance, 1.0)


class TestPointToPolygonDistance(unittest.TestCase):
    """点多边形距离测试"""

    def test_inside(self):
        """测试点在多边形内"""
        poly = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        distance = point_to_polygon_distance(Point2D(2, 1), poly)
        self.assertEqual(distance, 0.0)

    def test_outside(self):
        """测试点在多边形外"""
        poly = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
        distance = point_to_polygon_distance(Point2D(5, 1), poly)
        self.assertEqual(distance, 1.0)


class TestAngleBetween(unittest.TestCase):
    """向量夹角测试"""

    def test_perpendicular(self):
        """测试垂直向量夹角"""
        v1 = Vector2D(1, 0)
        v2 = Vector2D(0, 1)
        angle = angle_between(v1, v2)
        self.assertEqual(angle, 90.0)

    def test_parallel(self):
        """测试平行向量夹角"""
        v1 = Vector2D(1, 0)
        v2 = Vector2D(2, 0)
        angle = angle_between(v1, v2)
        self.assertEqual(angle, 0.0)

    def test_diagonal(self):
        """测试对角向量夹角"""
        v1 = Vector2D(1, 0)
        v2 = Vector2D(1, 1)
        angle = angle_between(v1, v2)
        self.assertAlmostEqual(angle, 45.0)


class TestAngleBetweenRad(unittest.TestCase):
    """向量夹角弧度测试"""

    def test_perpendicular_rad(self):
        """测试垂直向量夹角弧度"""
        v1 = Vector2D(1, 0)
        v2 = Vector2D(0, 1)
        angle = angle_between_rad(v1, v2)
        self.assertAlmostEqual(angle, math.pi / 2)


class TestArePerpendicular(unittest.TestCase):
    """向量垂直测试"""

    def test_perpendicular(self):
        """测试垂直"""
        v1 = Vector2D(1, 0)
        v2 = Vector2D(0, 1)
        self.assertTrue(are_perpendicular(v1, v2))

    def test_not_perpendicular(self):
        """测试不垂直"""
        v1 = Vector2D(1, 0)
        v2 = Vector2D(1, 1)
        self.assertFalse(are_perpendicular(v1, v2))


class TestAreParallel(unittest.TestCase):
    """向量平行测试"""

    def test_parallel(self):
        """测试平行"""
        v1 = Vector2D(1, 0)
        v2 = Vector2D(2, 0)
        self.assertTrue(are_parallel(v1, v2))

    def test_not_parallel(self):
        """测试不平行"""
        v1 = Vector2D(1, 0)
        v2 = Vector2D(0, 1)
        self.assertFalse(are_parallel(v1, v2))


class TestSegmentsDistance(unittest.TestCase):
    """线段距离测试"""

    def test_intersecting(self):
        """测试相交线段"""
        s1 = LineSegment(Point2D(0, 0), Point2D(2, 2))
        s2 = LineSegment(Point2D(0, 2), Point2D(2, 0))
        distance = segments_distance(s1, s2)
        self.assertEqual(distance, 0.0)

    def test_parallel_separated(self):
        """测试平行分离线段"""
        s1 = LineSegment(Point2D(0, 0), Point2D(2, 0))
        s2 = LineSegment(Point2D(0, 2), Point2D(2, 2))
        distance = segments_distance(s1, s2)
        self.assertEqual(distance, 2.0)


class TestSegmentsClosestPoints(unittest.TestCase):
    """线段最近点对测试"""

    def test_closest_points(self):
        """测试最近点对"""
        s1 = LineSegment(Point2D(0, 0), Point2D(2, 0))
        s2 = LineSegment(Point2D(1, 2), Point2D(3, 2))
        p1, p2 = segments_closest_points(s1, s2)
        self.assertEqual(p1.x, 1.0)
        self.assertEqual(p1.y, 0.0)
        self.assertEqual(p2.x, 1.0)
        self.assertEqual(p2.y, 2.0)


class TestBoundingBox(unittest.TestCase):
    """边界框测试"""

    def test_bounding_box(self):
        """测试边界框计算"""
        points = [Point2D(0, 0), Point2D(4, 3), Point2D(2, 5)]
        bounds = bounding_box(points)
        self.assertEqual(bounds, (0, 0, 4, 5))

    def test_empty_points_error(self):
        """测试空点列表异常"""
        with self.assertRaises(ValueError):
            bounding_box([])


class TestCentroid(unittest.TestCase):
    """重心测试"""

    def test_centroid(self):
        """测试重心计算"""
        points = [Point2D(0, 0), Point2D(4, 0), Point2D(0, 4)]
        center = centroid(points)
        self.assertAlmostEqual(center.x, 4 / 3)
        self.assertAlmostEqual(center.y, 4 / 3)

    def test_empty_points_error(self):
        """测试空点列表异常"""
        with self.assertRaises(ValueError):
            centroid([])


if __name__ == "__main__":
    unittest.main()
