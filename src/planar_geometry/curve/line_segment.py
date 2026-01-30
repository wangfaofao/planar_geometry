# -*- coding: utf-8 -*-
"""
planar_geometry/curve/line_segment.py

模块: LineSegment
描述: LineSegment 类的实现
版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

依赖:
    - planar_geometry.abstracts: 抽象基类
    - planar_geometry.point: Point2D 类

使用示例:
    from planar_geometry.curve import LineSegment
"""

import math
from typing import TYPE_CHECKING, Optional

from planar_geometry.abstracts import Curve

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve.vector2d import Vector2D


class LineSegment(Curve):
    """
    线段类

    说明:
        - 由两个端点定义的有限线段
        - 可计算长度

    属性:
        start: Point2D - 起点
        end: Point2D - 终点

    使用示例:
        s = LineSegment(Point2D(0, 0), Point2D(3, 4))
        print(s.length())
    """

    def __init__(self, start: "Point2D", end: "Point2D") -> None:
        """
        初始化线段

        Args:
            start: Point2D - 起点
            end: Point2D - 终点
        """
        self.start = start
        self.end = end

    def length(self) -> float:
        """
        计算线段长度

        返回:
            float: 线段长度（欧几里得距离）
        """
        return self.start.distance_to(self.end)

    def midpoint(self) -> "Point2D":
        """
        获取线段中点

        返回:
            Point2D: 中点坐标
        """
        return self.start.midpoint_to(self.end)

    def direction(self) -> "Vector2D":
        """
        获取线段方向向量（归一化）

        返回:
            Vector2D: 从起点指向终点的单位向量
        """
        from planar_geometry.curve.vector2d import Vector2D

        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        v = Vector2D(dx, dy)
        return v.normalized()

    def contains_point(self, point: "Point2D", tolerance: float = 1e-9) -> bool:
        """
        判断点是否在线段上

        说明:
            - 检查点是否在线段上（包括端点）

        Args:
            point: Point2D - 待检测点
            tolerance: float - 容差

        返回:
            bool: True 表示点在线段上
        """
        t = self.get_parameter(point)
        return 0 <= t <= 1 and self.get_distance_to_point(point) < tolerance

    def get_parameter(self, point: "Point2D") -> float:
        """
        获取点在直线上的参数 t

        说明:
            - 参数 t: point = start + t * (end - start)
            - t = 0: 点在起点
            - t = 1: 点在终点
            - 0 < t < 1: 点在线段内

        Args:
            point: Point2D - 待计算点

        返回:
            float: 参数值 t
        """
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        len_sq = dx * dx + dy * dy

        if len_sq < 1e-15:  # 线段退化为点
            return 0.0

        px = point.x - self.start.x
        py = point.y - self.start.y
        return (px * dx + py * dy) / len_sq

    def get_closest_point(self, point: "Point2D") -> "Point2D":
        """
        获取线段上离给定点最近的点

        Args:
            point: Point2D - 参考点

        返回:
            Point2D: 线段上最近的点
        """
        t = self.get_parameter(point)
        t = max(0.0, min(1.0, t))  # 限制在 [0, 1]
        return self.start.add(
            t * (self.end.x - self.start.x), t * (self.end.y - self.start.y)
        )

    def get_distance_to_point(self, point: "Point2D") -> float:
        """
        计算点到线段的最短距离

        Args:
            point: Point2D - 参考点

        返回:
            float: 距离值
        """
        closest = self.get_closest_point(point)
        return point.distance_to(closest)

    def __eq__(self, other: object) -> bool:
        """
        判断两条线段是否相等

        Args:
            other: object - 比较对象

        返回:
            bool: 是否相等
        """
        if not isinstance(other, LineSegment):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __repr__(self) -> str:
        return f"LineSegment({self.start}, {self.end})"
