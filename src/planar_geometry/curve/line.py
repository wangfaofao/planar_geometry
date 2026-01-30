# -*- coding: utf-8 -*-
"""
planar_geometry/curve/line.py

模块: Line
描述: Line 类的实现
版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

依赖:
    - planar_geometry.abstracts: 抽象基类
    - planar_geometry.point: Point2D 类

使用示例:
    from planar_geometry.curve import Line
"""

import math
from typing import TYPE_CHECKING, Optional

from planar_geometry.abstracts import Curve

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve.vector2d import Vector2D


class Line(Curve):
    """
    直线类（无限延伸）

    说明:
        - 由一个点和方向向量定义的无限延伸直线
        - 长度为无穷大

    属性:
        point: Point2D - 直线上一点
        direction: Vector2D - 方向向量（单位化）

    使用示例:
        line = Line(Point2D(0, 0), Vector2D(1, 1))
    """

    def __init__(self, point: "Point2D", direction: "Vector2D") -> None:
        """
        初始化直线

        Args:
            point: Point2D - 直线上一点
            direction: Vector2D - 方向向量（会被单位化）
        """
        self.point = point
        self.direction = direction.normalized()

    def length(self) -> float:
        """
        获取直线长度

        返回:
            float: 正无穷大
        """
        return float("inf")

    def get_intersection(
        self, other: "Line", tolerance: float = 1e-9
    ) -> Optional["Point2D"]:
        """
        计算两条直线的交点

        说明:
            - 平行线将抛出 ValueError 异常

        Args:
            other: Line - 另一条直线
            tolerance: float - 容差

        返回:
            Point2D: 交点

        异常:
            ValueError: 两条直线平行
        """
        # 获取两条直线的方向向量
        d1_x = self.direction.x
        d1_y = self.direction.y
        d2_x = other.direction.x
        d2_y = other.direction.y

        # 计算叉积
        cross = d1_x * d2_y - d1_y * d2_x

        if abs(cross) < tolerance:  # 平行或重合
            raise ValueError("Lines are parallel and do not intersect")

        # 参数 t
        dx = other.point.x - self.point.x
        dy = other.point.y - self.point.y
        t = (dx * d2_y - dy * d2_x) / cross

        # 计算交点
        from planar_geometry.point import Point2D

        return Point2D(self.point.x + t * d1_x, self.point.y + t * d1_y)

    def get_distance_to_point(self, point: "Point2D") -> float:
        """
        计算点到直线的距离

        Args:
            point: Point2D - 参考点

        返回:
            float: 距离值
        """
        # 点到直线的距离 = |AP × AD| / |AD|
        dx = point.x - self.point.x
        dy = point.y - self.point.y
        cross = dx * self.direction.y - dy * self.direction.x
        return abs(cross)

    def get_closest_point(self, point: "Point2D") -> "Point2D":
        """
        获取直线上离给定点最近的点（垂足）

        Args:
            point: Point2D - 参考点

        返回:
            Point2D: 垂足坐标
        """
        # 参数 t
        dx = point.x - self.point.x
        dy = point.y - self.point.y
        t = dx * self.direction.x + dy * self.direction.y

        # 计算垂足
        from planar_geometry.point import Point2D

        return Point2D(
            self.point.x + t * self.direction.x,
            self.point.y + t * self.direction.y,
        )

    def contains_point(self, point: "Point2D", tolerance: float = 1e-9) -> bool:
        """
        判断点是否在直线上

        Args:
            point: Point2D - 待检测点
            tolerance: float - 容差

        返回:
            bool: True 表示点在直线上
        """
        closest = self.get_closest_point(point)
        return point.equals(closest, tolerance)

    def __repr__(self) -> str:
        return f"Line({self.point}, direction={self.direction})"
