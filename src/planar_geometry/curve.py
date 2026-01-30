# -*- coding: utf-8 -*-
"""
planar_geometry/curve.py

模块: 曲线 - 一维几何元素
描述: 定义曲线抽象基类及具体实现（线段、直线、向量）
版本: 0.01
作者: wangheng <wangfaofao@gmail.com>

功能:
    - Curve: 曲线抽象基类
    - LineSegment: 线段类
    - Line: 直线类
    - Vector2D: 二维向量类

依赖:
    - math: 数学模块
    - abc: 抽象基类模块
    - measurable: 可计算度量抽象基类
    - point: 点类

使用示例:
    from planar_geometry import Point2D, Vector2D, LineSegment

    p1 = Point2D(0, 0)
    p2 = Point2D(3, 4)
    segment = LineSegment(p1, p2)
    print(segment.length())
"""

import math
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from planar_geometry.measurable import Measurable1D

if TYPE_CHECKING:
    from planar_geometry.point import Point2D


class Curve(Measurable1D, ABC):
    """
    曲线抽象基类（一维几何元素）

    说明:
        - 继承Measurable1D
        - 抽象化一维几何元素的行为

    设计原则:
        - ISP: 只暴露曲线相关接口
    """

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def length(self) -> float:
        pass


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
        from planar_geometry.curve import Vector2D

        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        v = Vector2D(dx, dy)
        return v.normalized()

    def contains_point(self, point: "Point2D", tolerance: float = 1e-9) -> bool:
        """
        判断点是否在线段上（含端点）

        说明:
            - 使用参数方程法判断
            - 点 P 在线段上当: P = start + t * (end - start), t ∈ [0, 1]

        Args:
            point: Point2D - 待检测点
            tolerance: float - 容差

        返回:
            bool: True 表示点在线段上
        """
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y

        if abs(dx) < tolerance and abs(dy) < tolerance:
            return self.start.equals(point, tolerance)

        t = ((point.x - self.start.x) * dx + (point.y - self.start.y) * dy) / (
            dx * dx + dy * dy
        )

        if -tolerance <= t <= 1.0 + tolerance:
            closest = Point2D(self.start.x + t * dx, self.start.y + t * dy)
            return point.equals(closest, tolerance)
        return False

    def get_parameter(self, point: "Point2D") -> float:
        """
        获取点在直线上的参数 t

        说明:
            - P = start + t * (end - start)
            - t < 0: 点在起点之前
            - t ∈ [0, 1]: 点在线段上
            - t > 1: 点在终点之后

        Args:
            point: Point2D - 目标点

        返回:
            float: 参数 t 值
        """
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y

        if abs(dx) < 1e-12 and abs(dy) < 1e-12:
            return 0.0

        return ((point.x - self.start.x) * dx + (point.y - self.start.y) * dy) / (
            dx * dx + dy * dy
        )

    def get_closest_point(self, point: "Point2D") -> "Point2D":
        """
        获取线段上离给定点最近的点

        Args:
            point: Point2D - 目标点

        返回:
            Point2D: 最近的点
        """
        t = self.get_parameter(point)
        t_clamped = max(0.0, min(1.0, t))

        return Point2D(
            self.start.x + t_clamped * (self.end.x - self.start.x),
            self.start.y + t_clamped * (self.end.y - self.start.y),
        )

    def get_distance_to_point(self, point: "Point2D") -> float:
        """
        计算点到线段的最短距离

        Args:
            point: Point2D - 目标点

        返回:
            float: 最短距离
        """
        closest = self.get_closest_point(point)
        return point.distance_to(closest)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LineSegment):
            return NotImplemented
        return (self.start == other.start and self.end == other.end) or (
            self.start == other.end and self.end == other.start
        )

    def __repr__(self) -> str:
        return f"LineSegment({self.start}, {self.end})"


class Line(Curve):
    """
    直线类（无限延伸）

    说明:
        - 过两点定义的无限直线
        - 长度视为无穷大

    属性:
        point: Point2D - 直线上一点
        direction: Vector2D - 方向向量

    使用示例:
        l = Line(Point2D(0, 0), Vector2D(1, 1))
    """

    def __init__(self, point: "Point2D", direction: "Vector2D") -> None:
        """
        初始化直线

        Args:
            point: Point2D - 直线上任意一点
            direction: Vector2D - 方向向量
        """
        self.point = point
        self.direction = direction.normalized()

    def length(self) -> float:
        """
        计算直线长度

        说明:
            - 直线无限延伸，长度为无穷大

        返回:
            float: float('inf')
        """
        return float("inf")

    def get_intersection(self, other: "Line") -> "Point2D":
        """
        计算与另一条直线的交点

        说明:
            - 使用参数方程法求解
            - 平行直线无交点

        Args:
            other: Line - 另一条直线

        返回:
            Point2D: 交点坐标

        异常:
            ValueError: 两条直线平行
        """
        x1, y1 = self.point.x, self.point.y
        x2 = x1 + self.direction.x
        y2 = y1 + self.direction.y
        x3, y3 = other.point.x, other.point.y
        x4 = x3 + other.direction.x
        y4 = y3 + other.direction.y

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-9:
            raise ValueError("Lines are parallel")

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom

        return Point2D(x1 + t * (x2 - x1), y1 + t * (y2 - y1))

    def get_distance_to_point(self, point: "Point2D") -> float:
        """
        计算点到直线的距离

        Args:
            point: Point2D - 目标点

        返回:
            float: 距离值
        """
        x0, y0 = point.x, point.y
        x1, y1 = self.point.x, self.point.y
        dx, dy = self.direction.x, self.direction.y

        num = abs(dy * x0 - dx * y0 + dx * y1 - dy * x1)
        denom = math.sqrt(dx * dx + dy * dy)

        return num / denom if denom > 0 else 0.0

    def get_closest_point(self, point: "Point2D") -> "Point2D":
        """
        获取直线上离给定点最近的点（垂足）

        Args:
            point: Point2D - 目标点

        返回:
            Point2D: 最近的点
        """
        x0, y0 = point.x, point.y
        x1, y1 = self.point.x, self.point.y
        dx, dy = self.direction.x, self.direction.y

        t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)

        return Point2D(x1 + t * dx, y1 + t * dy)

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


class Vector2D(Curve):
    """
    二维向量类

    说明:
        - 有方向和模长
        - 可计算模长作为长度

    属性:
        x: float - x分量
        y: float - y分量

    使用示例:
        v = Vector2D(3, 4)
        print(v.length())
    """

    def __init__(self, x: float, y: float) -> None:
        """
        初始化二维向量

        Args:
            x: float - x分量
            y: float - y分量
        """
        self.x = x
        self.y = y

    def length(self) -> float:
        """
        计算向量模长

        返回:
            float: 模长值
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def length_squared(self) -> float:
        """
        计算向量模长平方

        说明:
            - 避免开方运算，性能更高

        返回:
            float: 模长平方值
        """
        return self.x * self.x + self.y * self.y

    def angle(self) -> float:
        """
        计算向量角度（度）

        返回:
            float: 角度值 [0, 360)
        """
        angle_rad = math.atan2(self.y, self.x)
        return math.degrees(angle_rad) % 360.0

    def angle_rad(self) -> float:
        """
        计算向量角度（弧度）

        返回:
            float: 角度值 [0, 2π)
        """
        return math.atan2(self.y, self.x) % (2 * math.pi)

    def normalized(self) -> "Vector2D":
        """
        返回归一化向量

        返回:
            Vector2D: 归一化后的向量
        """
        length = self.length()
        if length > 0:
            return Vector2D(self.x / length, self.y / length)
        return Vector2D(0, 0)

    def dot(self, other: "Vector2D") -> float:
        """
        点积

        Args:
            other: Vector2D - 另一向量

        返回:
            float: 点积结果
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: "Vector2D") -> float:
        """
        叉积（二维，标量）

        Args:
            other: Vector2D - 另一向量

        返回:
            float: 叉积结果（标量）
        """
        return self.x * other.y - self.y * other.x

    def perpendicular(self) -> "Vector2D":
        """
        获取垂直向量（逆时针旋转90度）

        返回:
            Vector2D: 垂直向量
        """
        return Vector2D(-self.y, self.x)

    def rotated(self, angle_deg: float) -> "Vector2D":
        """
        旋转向量

        Args:
            angle_deg: float - 旋转角度（度）

        返回:
            Vector2D: 旋转后的向量
        """
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Vector2D(
            self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a
        )

    def projection(self, other: "Vector2D") -> "Vector2D":
        """
        投影到另一向量

        Args:
            other: Vector2D - 目标向量

        返回:
            Vector2D: 投影向量
        """
        dot = self.dot(other)
        other_len_sq = other.length_squared()
        if other_len_sq == 0:
            return Vector2D(0, 0)
        scalar = dot / other_len_sq
        return Vector2D(other.x * scalar, other.y * scalar)

    def component(self, direction: "Vector2D") -> float:
        """
        获取在指定方向上的分量（标量投影）

        Args:
            direction: Vector2D - 方向向量

        返回:
            float: 分量值（标量）
        """
        dir_norm = direction.normalized()
        return self.dot(dir_norm)

    def add(self, other: "Vector2D") -> "Vector2D":
        """
        向量加法

        Args:
            other: Vector2D - 另一向量

        返回:
            Vector2D: 结果向量
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def subtract(self, other: "Vector2D") -> "Vector2D":
        """
        向量减法

        Args:
            other: Vector2D - 另一向量

        返回:
            Vector2D: 结果向量
        """
        return Vector2D(self.x - other.x, self.y - other.y)

    def multiply(self, scalar: float) -> "Vector2D":
        """
        标量乘法

        Args:
            scalar: float - 标量

        返回:
            Vector2D: 结果向量
        """
        return Vector2D(self.x * scalar, self.y * scalar)

    def divide(self, scalar: float) -> "Vector2D":
        """
        标量除法

        Args:
            scalar: float - 标量

        返回:
            Vector2D: 结果向量

        异常:
            ZeroDivisionError: 标量为0
        """
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Vector2D(self.x / scalar, self.y / scalar)

    def negate(self) -> "Vector2D":
        """
        取负

        返回:
            Vector2D: 取负后的向量
        """
        return Vector2D(-self.x, -self.y)

    def is_zero(self, tolerance: float = 1e-9) -> bool:
        """
        判断是否为零向量

        Args:
            tolerance: float - 容差

        返回:
            bool: 是否为零向量
        """
        return abs(self.x) < tolerance and abs(self.y) < tolerance

    def equals(self, other: "Vector2D", tolerance: float = 1e-9) -> bool:
        """
        判断与另一向量是否相等

        Args:
            other: Vector2D - 比较对象
            tolerance: float - 容差

        返回:
            bool: 是否相等
        """
        return abs(self.x - other.x) < tolerance and abs(self.y - other.y) < tolerance

    def to_tuple(self) -> tuple:
        """
        转换为元组

        返回:
            tuple: (x, y)
        """
        return (self.x, self.y)

    @staticmethod
    def from_tuple(data: tuple) -> "Vector2D":
        """
        从元组创建向量

        Args:
            data: tuple - (x, y) 元组

        返回:
            Vector2D: 创建的向量
        """
        return Vector2D(data[0], data[1])

    @staticmethod
    def zero() -> "Vector2D":
        """
        创建零向量

        返回:
            Vector2D: 零向量 (0, 0)
        """
        return Vector2D(0, 0)

    @staticmethod
    def unit_x() -> "Vector2D":
        """
        创建X轴单位向量

        返回:
            Vector2D: (1, 0)
        """
        return Vector2D(1, 0)

    @staticmethod
    def unit_y() -> "Vector2D":
        """
        创建Y轴单位向量

        返回:
            Vector2D: (0, 1)
        """
        return Vector2D(0, 1)

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2D":
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> "Vector2D":
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector2D(self.x / scalar, self.y / scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __hash__(self) -> int:
        return hash((round(self.x, 9), round(self.y, 9)))

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


from planar_geometry.point import Point2D
