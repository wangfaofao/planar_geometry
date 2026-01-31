# -*- coding: utf-8 -*-
"""
planar_geometry/utils/__init__.py

包: 工具函数模块
======================================

描述:
    提供独立的几何计算函数，用于处理几何对象之间的关系。
    这些函数不属于任何特定的几何类，而是处理多个几何对象的相互作用。

版本: 0.2.0
作者: wangheng <wangfaofao@gmail.com>

功能分类:

1. 交点计算 (geometry_utils):
   - line_segment_intersection: 两条线段的交点
   - line_intersection: 两条直线的交点
   - rectangle_intersection_points: 两个矩形的交点集合
   - polygon_intersection_points: 两个多边形的交点集合

2. 增强交点计算 (intersection_ops) - v0.2.0 新增:
   - circle_line_intersection: 圆与直线的交点
   - circle_segment_intersection: 圆与线段的交点
   - circles_intersection: 两个圆的交点
   - line_polygon_intersection_points: 直线与多边形的所有交点
   - segment_polygon_intersection_points: 线段与多边形的交点
   - ellipse_line_intersection: 椭圆与直线的交点
   - ellipse_circle_intersection: 椭圆与圆的交点

3. 距离和投影计算 (geometry_utils):
   - point_to_segment_distance: 点到线段的最短距离
   - point_to_segment_closest_point: 线段上最近的点
   - point_to_line_distance: 点到直线的距离
   - point_to_line_closest_point: 直线上最近的点（垂足）
   - point_to_rectangle_distance: 点到矩形的最短距离
   - point_to_polygon_distance: 点到多边形的最短距离
   - segments_distance: 两条线段的最短距离
   - segments_closest_points: 两条线段的最近点对

4. 增强投影计算 (projection_ops) - v0.2.0 新增:
   - nearest_point_on_geometry: 点到任意几何体的投影（统一接口）
   - polygon_nearest_points: 两个多边形的最近点对
   - point_to_circle_nearest: 点到圆的最近点（含极角）

5. 查询操作 (query_ops) - v0.2.0 新增:
   - point_side_of_segment: 点相对于线段的方向判断
   - circle_polygon_intersect: 圆与多边形相交检测
   - minimum_distance: 两个几何体间的最小距离
   - within_distance: 距离内相交检测

6. 角度计算 (geometry_utils):
   - angle_between: 两个向量的夹角（度）
   - angle_between_rad: 两个向量的夹角（弧度）
   - are_perpendicular: 两个向量是否垂直
   - are_parallel: 两个向量是否平行

7. 增强角度计算 (angle_ops) - v0.2.0 新增:
   - angle_between_three_points: 三点确定的有向角
   - polygon_vertex_angles: 多边形各顶点处的内角
   - point_polar_angle: 点相对于参考点的极角

8. 坐标转换 (coordinate_ops) - v0.2.0 新增:
   - cartesian_to_polar: 笛卡尔坐标转极坐标
   - polar_to_cartesian: 极坐标转笛卡尔坐标
   - sort_points_by_angle: 按极角排序点集
   - are_collinear: 判断多点是否共线

9. 点集工具 (geometry_utils):
   - bounding_box: 点集的轴对齐边界框
   - centroid: 点集的重心

使用示例:
     from planar_geometry.utils import (
         line_segment_intersection,
         point_to_segment_distance,
         angle_between,
         bounding_box,
         circle_line_intersection,
         angle_between_three_points,
         cartesian_to_polar,
         are_collinear
     )
     # 或
     from planar_geometry import (
         line_segment_intersection,
         circle_line_intersection,
         angle_between_three_points,
         cartesian_to_polar
     )

相关模块:
     - planar_geometry.point: Point2D 类
     - planar_geometry.curve: LineSegment, Line, Vector2D 类
     - planar_geometry.surface: Rectangle, Circle, Polygon, Triangle, Ellipse 类

子模块:
     - geometry_utils: 原有工具函数实现 (v0.1.0)
     - intersection_ops: 增强交点计算 (v0.2.0)
     - projection_ops: 增强投影查询 (v0.2.0)
     - query_ops: 查询操作 (v0.2.0)
     - angle_ops: 增强角度计算 (v0.2.0)
     - coordinate_ops: 坐标系统转换 (v0.2.0)
"""

# 导入 v0.1.0 原有函数
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

# 导入 v0.2.0 新增函数
from planar_geometry.utils.intersection_ops import (
    circle_line_intersection,
    circle_segment_intersection,
    circles_intersection,
    line_polygon_intersection_points,
    segment_polygon_intersection_points,
    ellipse_line_intersection,
    ellipse_circle_intersection,
)

from planar_geometry.utils.projection_ops import (
    nearest_point_on_geometry,
    polygon_nearest_points,
    point_to_circle_nearest,
)

from planar_geometry.utils.query_ops import (
    point_side_of_segment,
    circle_polygon_intersect,
    minimum_distance,
    within_distance,
)

from planar_geometry.utils.angle_ops import (
    angle_between_three_points,
    polygon_vertex_angles,
    point_polar_angle,
)

from planar_geometry.utils.coordinate_ops import (
    cartesian_to_polar,
    polar_to_cartesian,
    sort_points_by_angle,
    are_collinear,
)

__all__ = [
    # v0.1.0 原有函数
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
