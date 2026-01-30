# -*- coding: utf-8 -*-
"""
planar_geometry

模块: 平面几何计算库
描述: 基于SOLID原则设计的几何库，支持Cython优化
版本: 0.1.0

功能:
    - 抽象基类: Measurable, Measurable1D, Measurable2D
    - 点: Point2D
    - 曲线: Curve, LineSegment, Line, Vector2D
    - 曲面: Surface, Rectangle, Circle, Polygon
    - 几何工具: line_segment_intersection, line_intersection, rectangle_intersection_points

使用示例:
    from planar_geometry import Point2D, Vector2D, Rectangle

    rect = Rectangle.from_center_and_size(
        center=Point2D(0, 0),
        size=2.0,
        direction=Vector2D(1, 0)
    )
    print(rect.area())
"""

from planar_geometry.measurable import Measurable, Measurable1D, Measurable2D
from planar_geometry.point import Point2D
from planar_geometry.curve import Curve, LineSegment, Line, Vector2D
from planar_geometry.surface import Surface, Rectangle, Circle, Polygon
from planar_geometry.geometry_utils import (
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
    "Measurable",
    "Measurable1D",
    "Measurable2D",
    "Point2D",
    "Curve",
    "LineSegment",
    "Line",
    "Vector2D",
    "Surface",
    "Rectangle",
    "Circle",
    "Polygon",
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
