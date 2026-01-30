# -*- coding: utf-8 -*-
"""
planar_geometry/point.py

模块: 二维点
描述: 定义二维点类，作为所有几何元素的构建基础
版本: 0.01
作者: wangheng <wangfaofao@gmail.com>

功能:
    - Point2D: 二维点类

依赖:
    - math: 数学模块
    - measurable: 可计算度量抽象基类

使用示例:
    from planar_geometry import Point2D

    p1 = Point2D(1.0, 2.0)
    p2 = Point2D(4.0, 6.0)
    distance = p1.distance_to(p2)
"""

import math

from planar_geometry.abstracts import Measurable1D


class Point2D(Measurable1D):
    """
    二维点类

    说明:
        - 零维几何元素
        - 作为所有几何元素的构建基础
        - 长度为0

    属性:
        x: float - 横坐标
        y: float - 纵坐标

    设计原则:
        - 数据结构简单，直接暴露属性便于Cython优化
        - 实现Measurable1D接口，length()返回0

    使用示例:
        p = Point2D(1.0, 2.0)
        print(p.x, p.y)
    """

    def __init__(self, x: float, y: float) -> None:
        """
        初始化二维点

        Args:
            x: float - 横坐标
            y: float - 纵坐标
        """
        self.x = x
        self.y = y

    def length(self) -> float:
        """
        计算长度

        说明:
            - 点长度为0

        返回:
            float: 0.0
        """
        return 0.0

    def distance_to(self, other: "Point2D") -> float:
        """
        计算到另一个点的欧几里得距离

        说明:
            - 使用标准欧几里得距离公式
            - distance = sqrt((x1-x2)^2 + (y1-y2)^2)

        Args:
            other: Point2D - 目标点

        返回:
            float: 距离值
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def distance_squared_to(self, other: "Point2D") -> float:
        """
        计算到另一个点的距离平方

        说明:
            - 避免开方运算，性能更高
            - 比较距离时常用

        Args:
            other: Point2D - 目标点

        返回:
            float: 距离平方值
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy

    def midpoint_to(self, other: "Point2D") -> "Point2D":
        """
        计算到另一个点的中点

        Args:
            other: Point2D - 目标点

        返回:
            Point2D: 中点坐标
        """
        return Point2D((self.x + other.x) / 2.0, (self.y + other.y) / 2.0)

    def add(self, dx: float, dy: float) -> "Point2D":
        """
        平移点

        Args:
            dx: float - x方向偏移
            dy: float - y方向偏移

        返回:
            Point2D: 平移后的点
        """
        return Point2D(self.x + dx, self.y + dy)

    def subtract(self, other: "Point2D") -> tuple:
        """
        点减法：点 - 点 = (dx, dy)

        Args:
            other: Point2D - 减去的点

        返回:
            tuple: (dx, dy) 向量分量
        """
        return (self.x - other.x, self.y - other.y)

    def multiply(self, scalar: float) -> "Point2D":
        """
        标量乘法：点 * 标量 = 新点

        Args:
            scalar: float - 标量

        返回:
            Point2D: 新点坐标
        """
        return Point2D(self.x * scalar, self.y * scalar)

    def negate(self) -> "Point2D":
        """
        取负：-点 = (-x, -y)

        返回:
            Point2D: 取负后的点
        """
        return Point2D(-self.x, -self.y)

    def equals(self, other: "Point2D", tolerance: float = 1e-9) -> bool:
        """
        判断与另一点是否相等（带容差）

        Args:
            other: Point2D - 比较对象
            tolerance: float - 容差

        返回:
            bool: 是否相等
        """
        return abs(self.x - other.x) < tolerance and abs(self.y - other.y) < tolerance

    def is_zero(self, tolerance: float = 1e-9) -> bool:
        """
        判断是否为零点

        Args:
            tolerance: float - 容差

        返回:
            bool: 是否为零点
        """
        return abs(self.x) < tolerance and abs(self.y) < tolerance

    def to_tuple(self) -> tuple:
        """
        转换为元组

        返回:
            tuple: (x, y)
        """
        return (self.x, self.y)

    @staticmethod
    def from_tuple(data: tuple) -> "Point2D":
        """
        从元组创建点

        Args:
            data: tuple - (x, y) 元组

        返回:
            Point2D: 创建的点
        """
        return Point2D(data[0], data[1])

    @staticmethod
    def origin() -> "Point2D":
        """
        创建原点

        返回:
            Point2D: 原点 (0, 0)
        """
        return Point2D(0.0, 0.0)

    def __add__(self, other: tuple) -> "Point2D":
        """
        向量加法：点 + (dx, dy) = 新点

        Args:
            other: tuple - (dx, dy) 向量分量

        返回:
            Point2D: 新点坐标
        """
        return Point2D(self.x + other[0], self.y + other[1])

    def __sub__(self, other: "Point2D") -> tuple:
        """
        点减法：点 - 点 = (x, y)

        Args:
            other: Point2D - 减去的点

        返回:
            tuple: (dx, dy) 向量分量
        """
        return (self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Point2D":
        """
        标量乘法：点 * 标量 = 新点

        Args:
            scalar: float - 标量

        返回:
            Point2D: 新点坐标
        """
        return Point2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Point2D":
        """
        标量乘法：标量 * 点 = 新点

        Args:
            scalar: float - 标量

        返回:
            Point2D: 新点坐标
        """
        return Point2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> "Point2D":
        """
        标量除法：点 / 标量 = 新点

        Args:
            scalar: float - 标量

        返回:
            Point2D: 新点坐标

        异常:
            ZeroDivisionError: 标量为0
        """
        if scalar == 0.0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Point2D(self.x / scalar, self.y / scalar)

    def __eq__(self, other: object) -> bool:
        """
        相等判断

        说明:
            - 使用 math.isclose 进行浮点比较

        Args:
            other: object - 比较对象

        返回:
            bool: 是否相等
        """
        if not isinstance(other, Point2D):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __hash__(self) -> int:
        """
        哈希值

        说明:
            - 使Point2D可用于字典键和集合

        返回:
            int: 哈希值
        """
        return hash((round(self.x, 9), round(self.y, 9)))

    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
