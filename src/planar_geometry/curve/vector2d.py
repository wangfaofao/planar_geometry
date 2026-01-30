# -*- coding: utf-8 -*-
"""
planar_geometry/curve/vector2_d.py

模块: Vector2D
描述: Vector2D类的实现
版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

依赖:
    - planar_geometry.abstracts: 抽象基类
    - planar_geometry.point: Point2D类

使用示例:
    from planar_geometry.curve import Vector2D
"""

import math
from typing import TYPE_CHECKING, Optional

from planar_geometry.abstracts import Curve

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve.vector2d import Vector2D


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
