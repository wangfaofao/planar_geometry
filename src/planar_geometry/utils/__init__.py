# -*- coding: utf-8 -*-
"""
planar_geometry/utils/__init__.py

模块: 工具函数模块包
描述: 提供独立的几何计算函数
版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

功能:
    - 交点计算、距离计算、角度计算、点集工具函数

使用示例:
    from planar_geometry.utils import line_segment_intersection
    # 或
    from planar_geometry import line_segment_intersection
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
