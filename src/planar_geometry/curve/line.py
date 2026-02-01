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

    def get_intersection(self, other: "Line", tolerance: float = 1e-9) -> Optional["Point2D"]:
        """
        计算两条直线的交点

        数学定义:
            两条直线的交点是同时满足两条直线方程的唯一点（非平行情况）。

        计算方法:
            设直线1经过点 P1，方向向量为 d1，直线2经过点 P2，方向向量为 d2。
            参数方程：

            .. math::

                L_1: \\vec{r} = P_1 + t \\cdot \\vec{d1}

                L_2: \\vec{r} = P_2 + s \\cdot \\vec{d2}

            在交点处 P1 + t*d1 = P2 + s*d2，求解得：

            .. math::

                t = \\frac{(P_2 - P_1) \\times \\vec{d2}}{\\vec{d1} \\times \\vec{d2}}

            其中 :math:`\\times` 表示2D叉积（标量结果）。

        重要性质:
            - 如果 d1 × d2 = 0，则两直线平行或重合，无交点
            - 两条相交直线有唯一交点
            - 交点与输入点的选择无关

        参数:
            other (Line): 另一条直线
            tolerance (float): 平行判定的容差，默认 1e-9

        返回:
            Point2D: 两直线的交点

        异常:
            ValueError: 两条直线平行或重合

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 射线追踪（Ray Tracing）中的光线交点
            - 几何裁剪
            - 直线相交检测

        使用示例::

            from planar_geometry import Line, Point2D, Vector2D

            # 水平线：y = 2
            line1 = Line(Point2D(0, 2), Vector2D(1, 0))

            # 垂直线：x = 3
            line2 = Line(Point2D(3, 0), Vector2D(0, 1))

            # 交点应该是 (3, 2)
            intersection = line1.get_intersection(line2)
            assert abs(intersection.x - 3) < 1e-9
            assert abs(intersection.y - 2) < 1e-9

            # 平行线 - 会抛异常
            line3 = Line(Point2D(0, 0), Vector2D(1, 0))
            line4 = Line(Point2D(0, 1), Vector2D(1, 0))
            try:
                line3.get_intersection(line4)
            except ValueError:
                print("Lines are parallel")
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

        数学定义:
            点到直线的距离是从该点到直线上最近点的欧氏距离。

        计算方法:
            设点为 P，直线经过点 A，方向向量为 d（已单位化）。
            向量 AP = P - A。点到直线的距离为：

            .. math::

                d = |\\vec{AP} \\times \\vec{d}|

            这是因为叉积的绝对值等于两向量形成的平行四边形面积，
            而平行四边形的高就是点到直线的距离（当 d 是单位向量时）。

            另一种理解：

            .. math::

                d = \\frac{|\\vec{AP} \\times \\vec{d}|}{|\\vec{d}|} = |\\vec{AP} \\times \\hat{d}|

            其中 :math:`\\hat{d}` 是单位方向向量。

        参数:
            point (Point2D): 参考点

        返回:
            float: 点到直线的距离（非负）

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 点线最近距离计算
            - 直线到点的碰撞检测
            - 平行线之间距离计算

        使用示例::

            from planar_geometry import Line, Point2D, Vector2D

            # 水平线：y = 0，通过原点，方向为 x 轴
            line = Line(Point2D(0, 0), Vector2D(1, 0))

            # 点 (0, 5) 到直线的距离应该是 5
            dist = line.get_distance_to_point(Point2D(0, 5))
            assert abs(dist - 5.0) < 1e-9

            # 点 (3, 4) 到直线 y = 0 的距离应该是 4
            dist2 = line.get_distance_to_point(Point2D(3, 4))
            assert abs(dist2 - 4.0) < 1e-9
        """
        # 点到直线的距离 = |AP × AD| / |AD|
        dx = point.x - self.point.x
        dy = point.y - self.point.y
        cross = dx * self.direction.y - dy * self.direction.x
        return abs(cross)

    def get_closest_point(self, point: "Point2D") -> "Point2D":
        """
        计算直线上离给定点最近的点（垂足）

        数学定义:
            给定点 P 和直线 L（经过点 A，方向为 d），垂足 F 是 L 上离 P 最近的点。

        计算方法:
            使用向量投影。设 AP = P - A，则垂足为：

            .. math::

                t = \\vec{AP} \\cdot \\hat{d}

                F = A + t \\cdot \\hat{d}

            其中 :math:`\\hat{d}` 是单位方向向量，t 是投影标量。

            几何意义：t 表示从 A 沿方向 d 走多远才能到达垂足。

        参数:
            point (Point2D): 参考点

        返回:
            Point2D: 直线上最近点的坐标

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 垂足计算
            - 点在直线上的投影
            - 垂直距离的辅助计算

        使用示例::

            from planar_geometry import Line, Point2D, Vector2D

            # 水平线：y = 0
            line = Line(Point2D(0, 0), Vector2D(1, 0))

            # 点 (3, 5) 在直线上的投影（垂足）应该是 (3, 0)
            foot = line.get_closest_point(Point2D(3, 5))
            assert abs(foot.x - 3.0) < 1e-9
            assert abs(foot.y - 0.0) < 1e-9

            # 点 (0, 0) 在自己上面，垂足就是自己
            foot2 = line.get_closest_point(Point2D(0, 0))
            assert abs(foot2.x - 0.0) < 1e-9
            assert abs(foot2.y - 0.0) < 1e-9
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

        数学定义:
            点 P 在直线 L 上当且仅当点到直线的距离为 0（或在容差范围内）。

        判定方法:
            1. 计算点 P 到直线 L 的最近点 F（垂足）
            2. 检查 P 和 F 是否相等（在容差范围内）

            .. math::

                P \\text{ on } L \\iff |P - F| < \\text{tolerance}

        参数:
            point (Point2D): 待检测点
            tolerance (float): 容差，默认 1e-9

        返回:
            bool: True 表示点在直线上

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 点线包含关系检测
            - 几何断言验证
            - 数值稳定性测试

        使用示例::

            from planar_geometry import Line, Point2D, Vector2D

            # 斜线：通过 (0,0)，方向为 (1,1)，即 y = x
            line = Line(Point2D(0, 0), Vector2D(1, 1))

            # 点 (3, 3) 在直线 y = x 上
            assert line.contains_point(Point2D(3, 3))

            # 点 (3, 4) 不在直线上
            assert not line.contains_point(Point2D(3, 4))

            # 起始点在直线上
            assert line.contains_point(Point2D(0, 0))
        """
        closest = self.get_closest_point(point)
        return point.equals(closest, tolerance)

    def __repr__(self) -> str:
        """
        返回直线的字符串表示

        说明:
            - 返回格式：Line(point, direction=unit_direction_vector)
            - 方向向量已单位化

        返回:
            str: 直线的字符串表示

        使用示例::

            from planar_geometry import Line, Point2D, Vector2D

            line = Line(Point2D(0, 0), Vector2D(3, 4))
            print(repr(line))
            # 输出: Line(Point2D(0.0, 0.0), direction=Vector2D(0.6, 0.8))
        """
        return f"Line({self.point}, direction={self.direction})"
