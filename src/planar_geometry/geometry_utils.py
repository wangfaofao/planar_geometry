# -*- coding: utf-8 -*-
"""
planar_geometry/geometry_utils.py

模块: 几何工具函数
描述: 提供独立的几何计算函数（不属于特定类的方法）
版本: 0.1.0

功能:
    - line_segment_intersection: 线段交点计算
    - line_intersection: 直线交点计算
    - rectangle_intersection_points: 矩形边界交点收集

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
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import LineSegment, Line, Vector2D
    from planar_geometry.surface import Rectangle


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
from planar_geometry.surface import Rectangle
