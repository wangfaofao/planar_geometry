# -*- coding: utf-8 -*-
"""
planar_geometry/point.py

模块: 二维点
描述: 定义二维点类，作为所有几何元素的构建基础
版本: 0.1.0

功能:
    - Point2D: 二维点类

依赖:
    - math: 数学模块
    - measurable: 可计算度量抽象基类

使用示例:
    p1 = Point2D(1.0, 2.0)
    p2 = Point2D(4.0, 6.0)
    distance = p1.distance_to(p2)
"""

import math

from planar_geometry.measurable import Measurable1D


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

        Args:
            other: Point2D - 目标点

        返回:
            float: 距离值
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def __add__(self, other: tuple) -> "Point2D":
        """
        向量加法：点 + (x, y) = 新点

        Args:
            other: tuple - (x, y) 向量分量

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

    def __eq__(self, other: object) -> bool:
        """
        相等判断

        Args:
            other: object - 比较对象

        返回:
            bool: 是否相等
        """
        if not isinstance(other, Point2D):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"
