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

        数学定义:
            线段长度是两端点间的欧几里得距离：

            .. math::

                L = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}

        返回:
            float: 线段长度（非负）

        复杂度:
            O(1) - 常数时间操作

        使用示例::

            from planar_geometry import LineSegment, Point2D

            # 直角线段 (0,0) 到 (3,4)，长度应该是 5
            seg = LineSegment(Point2D(0, 0), Point2D(3, 4))
            assert abs(seg.length() - 5.0) < 1e-9
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

        数学定义:
            点 P 在线段 AB 上当且仅当：
            1. P 在直线 AB 上（距离为 0）
            2. P 在 A 和 B 之间（参数 0 <= t <= 1）

        判定方法:
            使用参数方程 P = A + t*(B - A)，其中：

            .. math::

                t = \\frac{(P - A) \\cdot (B - A)}{|B - A|^2}

            线段包含条件：

            .. math::

                0 \\leq t \\leq 1 \\quad \\text{and} \\quad \\text{distance}(P, \\text{line}) < \\text{tolerance}

        参数:
            point (Point2D): 待检测点
            tolerance (float): 容差，默认 1e-9

        返回:
            bool: True 表示点在线段上

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 点与线段的碰撞检测
            - 线段交点验证
            - 几何关系查询

        使用示例::

            from planar_geometry import LineSegment, Point2D

            # 线段从 (0,0) 到 (4,0)
            seg = LineSegment(Point2D(0, 0), Point2D(4, 0))

            # 中点 (2,0) 在线段上
            assert seg.contains_point(Point2D(2, 0))

            # 端点在线段上
            assert seg.contains_point(Point2D(0, 0))
            assert seg.contains_point(Point2D(4, 0))

            # 延长线上的点 (5,0) 不在线段上
            assert not seg.contains_point(Point2D(5, 0))

            # 不在直线上的点 (2,1) 不在线段上
            assert not seg.contains_point(Point2D(2, 1))
        """
        t = self.get_parameter(point)
        return 0 <= t <= 1 and self.get_distance_to_point(point) < tolerance

    def get_parameter(self, point: "Point2D") -> float:
        """
        获取点在线段对应直线上的参数 t

        数学定义:
            参数 t 用参数方程表示：

            .. math::

                P = A + t \\cdot (B - A)

            其中 A 为起点，B 为终点，P 为待查询点。解得：

            .. math::

                t = \\frac{(P - A) \\cdot (B - A)}{|B - A|^2}

        参数解释:
            - t = 0：点在起点 A
            - t = 1：点在终点 B
            - 0 < t < 1：点在线段内部
            - t < 0：点在线段起点外侧
            - t > 1：点在线段终点外侧

        参数:
            point (Point2D): 待计算点

        返回:
            float: 参数值 t

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 线段参数化表示
            - 线段分割点计算
            - 点在线段上的相对位置判定

        使用示例::

            from planar_geometry import LineSegment, Point2D

            seg = LineSegment(Point2D(0, 0), Point2D(4, 0))

            # 起点的参数
            t_start = seg.get_parameter(Point2D(0, 0))
            assert abs(t_start - 0.0) < 1e-9

            # 终点的参数
            t_end = seg.get_parameter(Point2D(4, 0))
            assert abs(t_end - 1.0) < 1e-9

            # 中点的参数
            t_mid = seg.get_parameter(Point2D(2, 0))
            assert abs(t_mid - 0.5) < 1e-9

            # 线段外的点
            t_outside = seg.get_parameter(Point2D(5, 0))
            assert abs(t_outside - 1.25) < 1e-9  # > 1
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

        数学定义:
            给定点 P 和线段 AB，线段上离 P 最近的点由以下规则确定：

            1. 计算 P 在直线 AB 上的投影点 F，参数为 t
            2. 如果 0 <= t <= 1：最近点就是 F（投影点在线段上）
            3. 如果 t < 0：最近点是 A（起点）
            4. 如果 t > 1：最近点是 B（终点）

            .. math::

                F = A + t \\cdot (B - A), \\quad t = \\text{clamp}(t, 0, 1)

        参数:
            point (Point2D): 参考点

        返回:
            Point2D: 线段上最近的点

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 点到线段的垂足计算
            - 线段-点最近距离问题
            - 碰撞检测中的约束投影

        使用示例::

            from planar_geometry import LineSegment, Point2D

            seg = LineSegment(Point2D(0, 0), Point2D(4, 0))

            # 点 (2, 3) 的最近点是 (2, 0)
            closest = seg.get_closest_point(Point2D(2, 3))
            assert abs(closest.x - 2.0) < 1e-9
            assert abs(closest.y - 0.0) < 1e-9

            # 点 (5, 0) 超出线段，最近点是终点 (4, 0)
            closest2 = seg.get_closest_point(Point2D(5, 0))
            assert abs(closest2.x - 4.0) < 1e-9

            # 点 (-1, 0) 超出线段，最近点是起点 (0, 0)
            closest3 = seg.get_closest_point(Point2D(-1, 0))
            assert abs(closest3.x - 0.0) < 1e-9
        """
        t = self.get_parameter(point)
        t = max(0.0, min(1.0, t))  # 限制在 [0, 1]
        return self.start.add(t * (self.end.x - self.start.x), t * (self.end.y - self.start.y))

    def get_distance_to_point(self, point: "Point2D") -> float:
        """
        计算点到线段的最短距离

        数学定义:
            点 P 到线段 AB 的距离是 P 到线段上最近点的欧几里得距离：

            .. math::

                d = \\min_{F \\in AB} |P - F|

            其中 F 是线段上的点。最近点由参数 t 的截断确定。

        计算方法:
            1. 计算点在无限直线上的投影参数 t
            2. 将 t 限制在 [0, 1] 范围内（确保投影点在线段上）
            3. 计算点与投影点的距离

        参数:
            point (Point2D): 参考点

        返回:
            float: 点到线段的最短距离（非负）

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 点线段距离计算
            - 碰撞检测（点与线段）
            - 几何查询

        使用示例::

            from planar_geometry import LineSegment, Point2D

            seg = LineSegment(Point2D(0, 0), Point2D(4, 0))

            # 点 (2, 3) 到线段的距离是 3
            dist = seg.get_distance_to_point(Point2D(2, 3))
            assert abs(dist - 3.0) < 1e-9

            # 线段上的点距离为 0
            dist2 = seg.get_distance_to_point(Point2D(2, 0))
            assert abs(dist2 - 0.0) < 1e-9

            # 点 (5, 0) 到线段，最近点是 (4, 0)，距离为 1
            dist3 = seg.get_distance_to_point(Point2D(5, 0))
            assert abs(dist3 - 1.0) < 1e-9
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
