# -*- coding: utf-8 -*-
"""
planar_geometry/utils/__init__.py

包: 工具函数模块
======================================

描述:
    提供独立的几何计算函数，用于处理几何对象之间的关系。
    这些函数不属于任何特定的几何类，而是处理多个几何对象的相互作用。

版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

功能分类:

1. 交点计算:
   - line_segment_intersection: 两条线段的交点
   - line_intersection: 两条直线的交点
   - rectangle_intersection_points: 两个矩形的交点集合
   - polygon_intersection_points: 两个多边形的交点集合

2. 距离计算:
   - point_to_segment_distance: 点到线段的最短距离
   - point_to_segment_closest_point: 线段上最近的点
   - point_to_line_distance: 点到直线的距离
   - point_to_line_closest_point: 直线上最近的点（垂足）
   - point_to_rectangle_distance: 点到矩形的最短距离
   - point_to_polygon_distance: 点到多边形的最短距离
   - segments_distance: 两条线段的最短距离
   - segments_closest_points: 两条线段的最近点对

3. 角度计算:
   - angle_between: 两个向量的夹角（度）
   - angle_between_rad: 两个向量的夹角（弧度）
   - are_perpendicular: 两个向量是否垂直
   - are_parallel: 两个向量是否平行

4. 点集工具:
   - bounding_box: 点集的轴对齐边界框
   - centroid: 点集的重心

使用示例:
    from planar_geometry.utils import (
        line_segment_intersection,
        point_to_segment_distance,
        angle_between,
        bounding_box
    )
    # 或
    from planar_geometry import (
        line_segment_intersection,
        point_to_segment_distance,
        angle_between,
        bounding_box
    )

    # 交点计算
    seg1 = LineSegment(Point2D(0, 0), Point2D(2, 2))
    seg2 = LineSegment(Point2D(0, 2), Point2D(2, 0))
    intersection = line_segment_intersection(seg1, seg2)  # Point2D(1, 1)

    # 距离计算
    point = Point2D(2, 3)
    segment = LineSegment(Point2D(0, 0), Point2D(4, 0))
    dist = point_to_segment_distance(point, segment)  # 3.0

    # 角度计算
    v1 = Vector2D(1, 0)
    v2 = Vector2D(0, 1)
    angle = angle_between(v1, v2)  # 90.0

    # 点集工具
    points = [Point2D(0, 0), Point2D(4, 3), Point2D(2, 5)]
    bounds = bounding_box(points)  # (0, 0, 4, 5)
    center = centroid(points)  # Point2D(2.0, 2.67)

相关模块:
    - planar_geometry.point: Point2D 类
    - planar_geometry.curve: LineSegment, Line, Vector2D 类
    - planar_geometry.surface: Rectangle, Circle, Polygon 类

子模块:
    - geometry_utils: 所有工具函数的实现
"""

from planar_geometry.utils.geometry_utils import (
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

__all__ = [
    "line_segment_intersection",
    "line_intersection",
    "rectangle_intersection_points",
    "polygon_intersection_points",
    "point_to_segment_distance",
    "point_to_segment_closest_point",
    "point_to_line_distance",
    "point_to_line_closest_point",
    "point_to_rectangle_distance",
    "point_to_polygon_distance",
    "angle_between",
    "angle_between_rad",
    "are_perpendicular",
    "are_parallel",
    "segments_distance",
    "segments_closest_points",
    "bounding_box",
    "centroid",
]
