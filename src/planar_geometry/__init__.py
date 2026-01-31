# -*- coding: utf-8 -*-
"""
planar_geometry

模块: 平面几何计算库
描述: 基于SOLID原则设计的几何库，支持Cython优化
版本: 0.2.0

功能:
    - 抽象基类: Measurable, Measurable1D, Measurable2D
    - 点: Point2D
    - 曲线: Curve, LineSegment, Line, Vector2D
    - 曲面: Surface, Rectangle, Circle, Polygon, Triangle, Ellipse
    - 几何工具 (v0.1.0): 交点、距离、角度、点集计算
    - 增强工具 (v0.2.0): 圆/椭圆交点、投影查询、查询操作、角度增强、坐标转换

使用示例:
    from planar_geometry import (
        Point2D, Vector2D, Rectangle, Circle, Polygon,
        line_segment_intersection,
        circle_line_intersection,
        angle_between_three_points,
        cartesian_to_polar
    )

    rect = Rectangle.from_center_and_size(
        center=Point2D(0, 0),
        size=2.0,
        direction=Vector2D(1, 0)
    )
    print(rect.area())

    # v0.2.0 新增: 圆与直线交点
    circle = Circle(Point2D(0, 0), 5)
    line = Line(Point2D(-10, 0), Vector2D(1, 0))
    intersections = circle_line_intersection(circle, line)

    # v0.2.0 新增: 三点夹角
    p1, p2, p3 = Point2D(0, 0), Point2D(1, 0), Point2D(1, 1)
    angle = angle_between_three_points(p1, p2, p3)  # 90度

    # v0.2.0 新增: 笛卡尔到极坐标
    distance, angle = cartesian_to_polar(Point2D(1, 1), Point2D(0, 0))
"""

from planar_geometry.abstracts import (
    Measurable,
    Measurable1D,
    Measurable2D,
    Curve,
    Surface,
)
from planar_geometry.point import Point2D
from planar_geometry.curve import LineSegment, Line, Vector2D
from planar_geometry.surface import (
    Rectangle,
    Circle,
    Polygon,
    Triangle,
    Ellipse,
)
from planar_geometry.utils import (
    # v0.1.0 原有函数
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
    # v0.2.0 新增函数 - 交点计算
    circle_line_intersection,
    circle_segment_intersection,
    circles_intersection,
    line_polygon_intersection_points,
    segment_polygon_intersection_points,
    ellipse_line_intersection,
    ellipse_circle_intersection,
    # v0.2.0 新增函数 - 投影查询
    nearest_point_on_geometry,
    polygon_nearest_points,
    point_to_circle_nearest,
    # v0.2.0 新增函数 - 查询操作
    point_side_of_segment,
    circle_polygon_intersect,
    minimum_distance,
    within_distance,
    # v0.2.0 新增函数 - 角度计算
    angle_between_three_points,
    polygon_vertex_angles,
    point_polar_angle,
    # v0.2.0 新增函数 - 坐标转换
    cartesian_to_polar,
    polar_to_cartesian,
    sort_points_by_angle,
    are_collinear,
)

__all__ = [
    # 抽象基类
    "Measurable",
    "Measurable1D",
    "Measurable2D",
    "Curve",
    "Surface",
    # 几何元素
    "Point2D",
    "LineSegment",
    "Line",
    "Vector2D",
    "Rectangle",
    "Circle",
    "Polygon",
    "Triangle",
    "Ellipse",
    # v0.1.0 工具函数
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
    # v0.2.0 新增函数 - 交点计算
    "circle_line_intersection",
    "circle_segment_intersection",
    "circles_intersection",
    "line_polygon_intersection_points",
    "segment_polygon_intersection_points",
    "ellipse_line_intersection",
    "ellipse_circle_intersection",
    # v0.2.0 新增函数 - 投影查询
    "nearest_point_on_geometry",
    "polygon_nearest_points",
    "point_to_circle_nearest",
    # v0.2.0 新增函数 - 查询操作
    "point_side_of_segment",
    "circle_polygon_intersect",
    "minimum_distance",
    "within_distance",
    # v0.2.0 新增函数 - 角度计算
    "angle_between_three_points",
    "polygon_vertex_angles",
    "point_polar_angle",
    # v0.2.0 新增函数 - 坐标转换
    "cartesian_to_polar",
    "polar_to_cartesian",
    "sort_points_by_angle",
    "are_collinear",
]
