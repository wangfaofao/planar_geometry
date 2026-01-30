# -*- coding: utf-8 -*-
"""
planar_geometry/geometry_utils.py

模块: 几何工具函数
描述: 提供独立的几何计算函数（跨对象关系）
版本: 0.01
作者: wangheng <wangfaofao@gmail.com>

功能:
    - 线段交点: line_segment_intersection
    - 直线交点: line_intersection
    - 矩形交点: rectangle_intersection_points
    - 多边形交点: polygon_intersection_points
    - 点到线距离: point_to_segment_distance, point_to_line_distance
    - 点到面距离: point_to_rectangle_distance, point_to_polygon_distance
    - 向量角度: angle_between, are_perpendicular, are_parallel
    - 线段距离: segments_distance, segments_closest_points

依赖:
    - math: 数学模块
    - typing: 类型提示
    - point: 点类
    - curve: 曲线类
    - surface: 曲面类

使用示例:
    from planar_geometry import Point2D, LineSegment, line_segment_intersection

    s1 = LineSegment(Point2D(0, 0), Point2D(2, 2))
    s2 = LineSegment(Point2D(0, 2), Point2D(2, 0))
    intersection = line_segment_intersection(s1, s2)
"""

import math
from typing import List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import LineSegment, Line, Vector2D
    from planar_geometry.surface import Rectangle, Polygon


def line_segment_intersection(
    s1: "LineSegment", s2: "LineSegment", tolerance: float = 1e-9
) -> Optional["Point2D"]:
    """
    计算两条线段的交点

    说明:
        - 使用参数方程法求解
        - 线段1: P(t) = p1 + t(p2-p1), t ∈ [0,1]
        - 线段2: Q(s) = p3 + s(p4-p3), s ∈ [0,1]
        - 求解 P(t) = Q(s) 得到交点

    Args:
        s1: LineSegment - 第一条线段
        s2: LineSegment - 第二条线段
        tolerance: float - 浮点容差

    返回:
        Optional[Point2D]: 交点坐标（若相交），否则 None

    边界情况:
        - 平行线检测
        - 端点相交
    """
    p1, p2 = s1.start, s1.end
    p3, p4 = s2.start, s2.end

    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    x4, y4 = p4.x, p4.y

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if abs(denom) < tolerance:
        return None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    s = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom

    if -tolerance <= t <= 1.0 + tolerance and -tolerance <= s <= 1.0 + tolerance:
        px = x1 + t * (x2 - x1)
        py = y1 + t * (y2 - y1)
        return Point2D(px, py)

    return None


def line_intersection(
    l1: "Line", l2: "Line", tolerance: float = 1e-9
) -> Optional["Point2D"]:
    """
    计算两条直线的交点

    说明:
        - 直线无限延伸
        - 平行直线无交点

    Args:
        l1: Line - 第一条直线
        l2: Line - 第二条直线
        tolerance: float - 浮点容差

    返回:
        Optional[Point2D]: 交点坐标（若相交），否则 None

    异常:
        ValueError: 两条直线平行
    """
    x1, y1 = l1.point.x, l1.point.y
    x2 = x1 + l1.direction.x
    y2 = y1 + l1.direction.y
    x3, y3 = l2.point.x, l2.point.y
    x4 = x3 + l2.direction.x
    y4 = y3 + l2.direction.y

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if abs(denom) < tolerance:
        raise ValueError("Lines are parallel")

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom

    return Point2D(x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def rectangle_intersection_points(
    r1: "Rectangle", r2: "Rectangle", tolerance: float = 1e-6
) -> List["Point2D"]:
    """
    计算两个矩形边界的所有交点

    说明:
        - 获取两个矩形的所有边（共8条）
        - 对每对边进行交点检测（最多16次）
        - 收集并去重所有交点

    Args:
        r1: Rectangle - 第一个矩形
        r2: Rectangle - 第二个矩形
        tolerance: float - 去重容差

    返回:
        List[Point2D]: 交点列表（可能为空）
    """
    edges1 = r1.get_edges()
    edges2 = r2.get_edges()

    intersections = []

    for e1 in edges1:
        for e2 in edges2:
            point = line_segment_intersection(
                LineSegment(e1[0], e1[1]), LineSegment(e2[0], e2[1])
            )
            if point is not None:
                if not _point_in_list(point, intersections, tolerance):
                    intersections.append(point)

    return intersections


def polygon_intersection_points(
    poly1: "Polygon", poly2: "Polygon", tolerance: float = 1e-6
) -> List["Point2D"]:
    """
    计算两个多边形边界的所有交点

    说明:
        - 获取两个多边形的所有边
        - 对每对边进行交点检测
        - 收集并去重所有交点

    Args:
        poly1: Polygon - 第一个多边形
        poly2: Polygon - 第二个多边形
        tolerance: float - 去重容差

    返回:
        List[Point2D]: 交点列表（可能为空）
    """
    edges1 = poly1.get_edges()
    edges2 = poly2.get_edges()

    intersections = []

    for e1 in edges1:
        for e2 in edges2:
            point = line_segment_intersection(
                LineSegment(e1[0], e1[1]), LineSegment(e2[0], e2[1])
            )
            if point is not None:
                if not _point_in_list(point, intersections, tolerance):
                    intersections.append(point)

    return intersections


def point_to_segment_distance(point: "Point2D", segment: "LineSegment") -> float:
    """
    计算点到线段的最短距离

    Args:
        point: Point2D - 目标点
        segment: LineSegment - 目标线段

    返回:
        float: 最短距离
    """
    return segment.get_distance_to_point(point)


def point_to_segment_closest_point(
    point: "Point2D", segment: "LineSegment"
) -> "Point2D":
    """
    计算线段上离给定点最近的点

    Args:
        point: Point2D - 目标点
        segment: LineSegment - 目标线段

    返回:
        Point2D: 最近的点
    """
    return segment.get_closest_point(point)


def point_to_line_distance(point: "Point2D", line: "Line") -> float:
    """
    计算点到直线的距离

    Args:
        point: Point2D - 目标点
        line: Line - 目标直线

    返回:
        float: 最短距离
    """
    return line.get_distance_to_point(point)


def point_to_line_closest_point(point: "Point2D", line: "Line") -> "Point2D":
    """
    计算直线上离给定点最近的点（垂足）

    Args:
        point: Point2D - 目标点
        line: Line - 目标直线

    返回:
        Point2D: 最近的点
    """
    return line.get_closest_point(point)


def point_to_rectangle_distance(point: "Point2D", rect: "Rectangle") -> float:
    """
    计算点到矩形的最短距离

    说明:
        - 如果点在矩形内，距离为0
        - 如果点在矩形外，计算到最近边的距离

    Args:
        point: Point2D - 目标点
        rect: Rectangle - 目标矩形

    返回:
        float: 最短距离
    """
    if rect.contains_point(point):
        return 0.0

    x, y = point.x, point.y
    x_min, y_min, x_max, y_max = rect.get_bounds()

    dx = max(x_min - x, 0, x - x_max)
    dy = max(y_min - y, 0, y - y_max)

    return math.sqrt(dx * dx + dy * dy)


def point_to_polygon_distance(point: "Point2D", poly: "Polygon") -> float:
    """
    计算点到多边形的最短距离

    说明:
        - 如果点在多边形内，距离为0
        - 如果点在多边形外，计算到最近边的距离

    Args:
        point: Point2D - 目标点
        poly: Polygon - 目标多边形

    返回:
        float: 最短距离
    """
    if poly.contains_point(point):
        return 0.0

    min_distance = float("inf")

    for edge in poly.get_edges():
        segment = LineSegment(edge[0], edge[1])
        distance = point_to_segment_distance(point, segment)
        if distance < min_distance:
            min_distance = distance

    return min_distance


def angle_between(v1: "Vector2D", v2: "Vector2D") -> float:
    """
    计算两个向量之间的夹角

    说明:
        - 返回角度范围 [0, 180]

    Args:
        v1: Vector2D - 第一个向量
        v2: Vector2D - 第二个向量

    返回:
        float: 夹角（度）
    """
    dot = v1.dot(v2)
    len1 = v1.length()
    len2 = v2.length()

    if len1 == 0 or len2 == 0:
        return 0.0

    cos_angle = dot / (len1 * len2)
    cos_angle = max(-1.0, min(1.0, cos_angle))

    return math.degrees(math.acos(cos_angle))


def angle_between_rad(v1: "Vector2D", v2: "Vector2D") -> float:
    """
    计算两个向量之间的夹角

    说明:
        - 返回角度范围 [0, π]

    Args:
        v1: Vector2D - 第一个向量
        v2: Vector2D - 第二个向量

    返回:
        float: 夹角（弧度）
    """
    dot = v1.dot(v2)
    len1 = v1.length()
    len2 = v2.length()

    if len1 == 0 or len2 == 0:
        return 0.0

    cos_angle = dot / (len1 * len2)
    cos_angle = max(-1.0, min(1.0, cos_angle))

    return math.acos(cos_angle)


def are_perpendicular(v1: "Vector2D", v2: "Vector2D", tolerance: float = 1e-6) -> bool:
    """
    判断两个向量是否垂直

    Args:
        v1: Vector2D - 第一个向量
        v2: Vector2D - 第二个向量
        tolerance: float - 容差

    返回:
        bool: 是否垂直
    """
    return abs(v1.dot(v2)) < tolerance


def are_parallel(v1: "Vector2D", v2: "Vector2D", tolerance: float = 1e-6) -> bool:
    """
    判断两个向量是否平行

    Args:
        v1: Vector2D - 第一个向量
        v2: Vector2D - 第二个向量
        tolerance: float - 容差

    返回:
        bool: 是否平行
    """
    cross = abs(v1.cross(v2))
    len1 = v1.length()
    len2 = v2.length()

    if len1 == 0 or len2 == 0:
        return True

    return cross / (len1 * len2) < tolerance


def segments_distance(s1: "LineSegment", s2: "LineSegment") -> float:
    """
    计算两条线段之间的最短距离

    说明:
        - 如果线段相交，距离为0
        - 否则计算端点到另一条线段的距离

    Args:
        s1: LineSegment - 第一条线段
        s2: LineSegment - 第二条线段

    返回:
        float: 最短距离
    """
    intersection = line_segment_intersection(s1, s2)
    if intersection is not None:
        return 0.0

    d1 = point_to_segment_distance(s1.start, s2)
    d2 = point_to_segment_distance(s1.end, s2)
    d3 = point_to_segment_distance(s2.start, s1)
    d4 = point_to_segment_distance(s2.end, s1)

    return min(d1, d2, d3, d4)


def segments_closest_points(
    s1: "LineSegment", s2: "LineSegment"
) -> Tuple["Point2D", "Point2D"]:
    """
    计算两条线段之间的最近点对

    Args:
        s1: LineSegment - 第一条线段
        s2: LineSegment - 第二条线段

    返回:
        Tuple[Point2D, Point2D]: (s1上的最近点, s2上的最近点)
    """
    intersection = line_segment_intersection(s1, s2)
    if intersection is not None:
        return (intersection, intersection)

    candidates = [
        (s1.get_closest_point(s2.start), s2.start),
        (s1.get_closest_point(s2.end), s2.end),
        (s2.get_closest_point(s1.start), s1.start),
        (s2.get_closest_point(s1.end), s1.end),
    ]

    min_dist = float("inf")
    best_pair = candidates[0]

    for p1, p2 in candidates:
        dist = p1.distance_to(p2)
        if dist < min_dist:
            min_dist = dist
            best_pair = (p1, p2)

    return best_pair


def point_line_distance_squared(
    px: float, py: float, line_point: "Point2D", line_dir: "Vector2D"
) -> float:
    """
    计算点到直线的距离平方（辅助函数）

    Args:
        px, py: float - 目标点坐标
        line_point: Point2D - 直线上一点
        line_dir: Vector2D - 直线方向向量

    返回:
        float: 距离平方
    """
    dx = px - line_point.x
    dy = py - line_point.y

    dir_len_sq = line_dir.length_squared()
    if dir_len_sq == 0:
        return dx * dx + dy * dy

    t = (dx * line_dir.x + dy * line_dir.y) / dir_len_sq

    closest_x = line_point.x + t * line_dir.x
    closest_y = line_point.y + t * line_dir.y

    return (px - closest_x) ** 2 + (py - closest_y) ** 2


def bounding_box(points: List["Point2D"]) -> Tuple[float, float, float, float]:
    """
    计算点集的轴对齐边界框

    Args:
        points: List[Point2D] - 点列表

    返回:
        Tuple[float, float, float, float]: (x_min, y_min, x_max, y_max)

    异常:
        ValueError: 点列表为空
    """
    if not points:
        raise ValueError("点列表不能为空")

    x_vals = [p.x for p in points]
    y_vals = [p.y for p in points]

    return (min(x_vals), min(y_vals), max(x_vals), max(y_vals))


def centroid(points: List["Point2D"]) -> "Point2D":
    """
    计算点集的重心

    Args:
        points: List[Point2D] - 点列表

    返回:
        Point2D: 重心坐标

    异常:
        ValueError: 点列表为空
    """
    if not points:
        raise ValueError("点列表不能为空")

    n = len(points)
    x = sum(p.x for p in points) / n
    y = sum(p.y for p in points) / n

    return Point2D(x, y)


def _point_in_list(point: "Point2D", points: List["Point2D"], tolerance: float) -> bool:
    """
    辅助函数：检查点是否在列表中（使用容差）

    Args:
        point: Point2D - 待检查的点
        points: List[Point2D] - 点列表
        tolerance: float - 容差

    返回:
        bool: 是否在列表中
    """
    for p in points:
        if abs(p.x - point.x) < tolerance and abs(p.y - point.y) < tolerance:
            return True
    return False


from planar_geometry.point import Point2D
from planar_geometry.curve import LineSegment, Line, Vector2D
from planar_geometry.surface import Rectangle, Polygon
