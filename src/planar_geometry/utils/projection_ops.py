# -*- coding: utf-8 -*-
"""
planar_geometry/utils/projection_ops.py

模块: 投影和最近点查询
描述: 计算点到各类几何体的投影和最近点
版本: 0.2.0
作者: wangheng <wangfaofao@gmail.com>

功能:
    - nearest_point_on_geometry: 点到任意几何体的最近点（统一接口）
    - polygon_nearest_points: 两个多边形间的最近点对
    - point_to_circle_nearest: 点到圆周上的最近点（含极角）

依赖:
    - math: 数学模块
    - typing: 类型提示
    - geometry_utils: 现有工具函数

使用示例:
    from planar_geometry import Point2D, Circle, Polygon
    from planar_geometry.utils import nearest_point_on_geometry

    point = Point2D(10, 0)
    circle = Circle(Point2D(0, 0), 5)
    nearest, dist = nearest_point_on_geometry(point, circle)
"""

import math
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import Line, LineSegment
    from planar_geometry.surface import Circle, Polygon, Ellipse, Rectangle

from .geometry_utils import (
    point_to_line_closest_point,
    point_to_line_distance,
    point_to_segment_closest_point,
    point_to_segment_distance,
)


def nearest_point_on_geometry(
    point: "Point2D", geometry, tolerance: float = 1e-10
) -> Tuple["Point2D", float]:
    """
    计算点到任意几何体边界的最近点（统一接口）

    说明:
        - 支持所有几何类型（Line, LineSegment, Circle, Polygon, Ellipse等）
        - 返回 (最近点, 距离) 的二元组
        - 对于无限几何（Line），返回直线上的最近点
        - 对于有限几何（Circle, Polygon等），返回边界上的最近点

    Args:
        point: Point2D - 查询点
        geometry: 任意几何对象 (Line, LineSegment, Circle, Polygon, Ellipse, Rectangle)
        tolerance: float - 浮点容差

    返回:
        Tuple[Point2D, float]: (最近点, 点到最近点的距离)

    应用场景:
        - 广泛应用于碰撞检测、避障、对齐等
        - 替代现有的多个分散方法
        - 统一的查询接口

    示例:
        >>> from planar_geometry import Point2D, Circle
        >>> point = Point2D(10, 0)
        >>> circle = Circle(Point2D(0, 0), 5)
        >>> nearest, dist = nearest_point_on_geometry(point, circle)
        >>> print(f"最近点: {nearest}, 距离: {dist}")
    """
    from planar_geometry.curve import Line, LineSegment
    from planar_geometry.surface import Circle, Polygon, Ellipse, Rectangle

    # 直线：返回投影点
    if isinstance(geometry, Line):
        closest_point = point_to_line_closest_point(point, geometry)
        distance = point.distance_to(closest_point)
        return (closest_point, distance)

    # 线段：返回线段上的最近点
    elif isinstance(geometry, LineSegment):
        closest_point = point_to_segment_closest_point(point, geometry)
        distance = point.distance_to(closest_point)
        return (closest_point, distance)

    # 圆：返回圆周上的最近点
    elif isinstance(geometry, Circle):
        center = geometry.center
        radius = geometry.radius

        # 计算点到圆心的向量
        dx = point.x - center.x
        dy = point.y - center.y
        dist_to_center = math.sqrt(dx * dx + dy * dy)

        if dist_to_center < tolerance:
            # 点在圆心，返回圆周上任意一点
            from planar_geometry.point import Point2D

            closest = Point2D(center.x + radius, center.y)
            return (closest, radius)

        # 圆周上的最近点
        factor = radius / dist_to_center
        from planar_geometry.point import Point2D

        closest = Point2D(center.x + dx * factor, center.y + dy * factor)
        distance = point.distance_to(center) - radius

        return (closest, max(0, distance))

    # 矩形：检查内部、边界、外部
    elif isinstance(geometry, Rectangle):
        # 获取矩形的轴对齐边界框
        bounds = geometry.get_bounds()
        min_x, min_y, max_x, max_y = bounds

        # 限制点到矩形范围内
        closest_x = max(min_x, min(point.x, max_x))
        closest_y = max(min_y, min(point.y, max_y))

        from planar_geometry.point import Point2D

        closest = Point2D(closest_x, closest_y)
        distance = point.distance_to(closest)

        return (closest, distance)

    # 多边形：遍历所有边找最近点
    elif isinstance(geometry, Polygon):
        edges = geometry.get_edges()
        min_distance = float("inf")
        min_point = None

        for edge in edges:
            closest, distance = nearest_point_on_geometry(point, edge, tolerance)
            if distance < min_distance:
                min_distance = distance
                min_point = closest

        if min_point is None:
            # 应该不会发生，但作为防御性编程
            from planar_geometry.point import Point2D

            min_point = Point2D(0, 0)
            min_distance = 0

        return (min_point, min_distance)

    # 椭圆：使用参数化方法找最近点
    elif isinstance(geometry, Ellipse):
        return _ellipse_nearest_point(point, geometry, tolerance)

    else:
        raise TypeError(f"不支持的几何类型: {type(geometry)}")


def polygon_nearest_points(
    poly1: "Polygon", poly2: "Polygon", tolerance: float = 1e-10
) -> Tuple["Point2D", "Point2D", float]:
    """
    计算两个多边形间的最近点对

    说明:
        - 返回 (点1, 点2, 距离) 三元组
        - 包括顶点-顶点、顶点-边、边-边的所有情况
        - 使用 AABB 提前排除不相关的点对

    Args:
        poly1: Polygon - 第一个多边形
        poly2: Polygon - 第二个多边形
        tolerance: float - 浮点容差

    返回:
        Tuple[Point2D, Point2D, float]: (点1, 点2, 最小距离)

    应用场景:
        - 碰撞检测和最小距离计算
        - 接近度分析
        - 物体对齐

    算法原理:
        1. 检查所有顶点对的距离
        2. 检查 poly1 的顶点到 poly2 的边的距离
        3. 检查 poly2 的顶点到 poly1 的边的距离
        4. 取最小值
    """
    min_distance = float("inf")
    min_point1 = None
    min_point2 = None

    vertices1 = poly1.vertices
    vertices2 = poly2.vertices

    # 检查顶点-顶点距离
    for v1 in vertices1:
        for v2 in vertices2:
            distance = v1.distance_to(v2)
            if distance < min_distance:
                min_distance = distance
                min_point1 = v1
                min_point2 = v2

    # 检查 poly1 顶点到 poly2 边的距离
    for v1 in vertices1:
        for edge2 in poly2.get_edges():
            closest, distance = nearest_point_on_geometry(v1, edge2, tolerance)
            if distance < min_distance:
                min_distance = distance
                min_point1 = v1
                min_point2 = closest

    # 检查 poly2 顶点到 poly1 边的距离
    for v2 in vertices2:
        for edge1 in poly1.get_edges():
            closest, distance = nearest_point_on_geometry(v2, edge1, tolerance)
            if distance < min_distance:
                min_distance = distance
                min_point1 = closest
                min_point2 = v2

    return (min_point1, min_point2, min_distance)


def point_to_circle_nearest(
    point: "Point2D", circle: "Circle", tolerance: float = 1e-10
) -> Tuple["Point2D", float, float]:
    """
    计算点到圆周上的最近点（含极角信息）

    说明:
        - 返回 (最近点, 距离, 极角) 的三元组
        - 极角相对于圆心，范围 [0, 360) 度
        - 极角 0° 表示圆心正右方

    Args:
        point: Point2D - 查询点
        circle: Circle - 圆
        tolerance: float - 浮点容差

    返回:
        Tuple[Point2D, float, float]: (最近点, 距离, 极角)

    应用场景:
        - 获取圆周上的点位置
        - 极坐标表示
        - 旋转运动跟踪

    示例:
        >>> from planar_geometry import Point2D, Circle
        >>> point = Point2D(10, 0)
        >>> circle = Circle(Point2D(0, 0), 5)
        >>> nearest, dist, angle = point_to_circle_nearest(point, circle)
        >>> print(f"最近点在 {angle}° 方向，距离 {dist}")
    """
    from planar_geometry.point import Point2D

    center = circle.center
    radius = circle.radius

    # 计算点到圆心的向量
    dx = point.x - center.x
    dy = point.y - center.y
    dist_to_center = math.sqrt(dx * dx + dy * dy)

    if dist_to_center < tolerance:
        # 点在圆心，返回圆周上的任意点（通常选择正右方）
        nearest_point = Point2D(center.x + radius, center.y)
        polar_angle = 0.0
        return (nearest_point, radius, polar_angle)

    # 圆周上的最近点
    factor = radius / dist_to_center
    nearest_x = center.x + dx * factor
    nearest_y = center.y + dy * factor
    nearest_point = Point2D(nearest_x, nearest_y)

    # 计算距离（点到圆心的距离减去半径）
    distance = max(0.0, dist_to_center - radius)

    # 计算极角（从圆心到最近点的方向）
    polar_angle = math.degrees(math.atan2(dy, dx))
    if polar_angle < 0:
        polar_angle += 360

    return (nearest_point, distance, polar_angle)


def _ellipse_nearest_point(
    point: "Point2D", ellipse: "Ellipse", tolerance: float = 1e-10
) -> Tuple["Point2D", float]:
    """
    私有函数：计算点到椭圆上最近点

    说明:
        - 使用参数扫描法
        - 在给定容差范围内找到最优解

    Args:
        point: Point2D - 查询点
        ellipse: Ellipse - 椭圆
        tolerance: float - 容差

    返回:
        Tuple[Point2D, float]: (最近点, 距离)
    """
    from planar_geometry.point import Point2D

    center = ellipse.center
    a = ellipse.semi_major_axis
    b = ellipse.semi_minor_axis
    angle_rad = math.radians(ellipse.rotation_angle)

    # 参数扫描法：椭圆上的点 = (cx + a*cos(t)*cos(θ) - b*sin(t)*sin(θ),
    #                            cy + a*cos(t)*sin(θ) + b*sin(t)*cos(θ))
    min_distance = float("inf")
    best_point = None

    for i in range(360):
        t = math.radians(i)
        cos_t = math.cos(t)
        sin_t = math.sin(t)

        x = center.x + a * cos_t * math.cos(angle_rad) - b * sin_t * math.sin(angle_rad)
        y = center.y + a * cos_t * math.sin(angle_rad) + b * sin_t * math.cos(angle_rad)

        ellipse_point = Point2D(x, y)
        distance = point.distance_to(ellipse_point)

        if distance < min_distance:
            min_distance = distance
            best_point = ellipse_point

    return (best_point, min_distance)
