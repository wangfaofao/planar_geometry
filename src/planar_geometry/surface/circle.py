# -*- coding: utf-8 -*-
"""
planar_geometry/surface/circle.py

模块: Circle
描述: Circle类的实现
版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

依赖:
    - planar_geometry.abstracts: 抽象基类
    - planar_geometry.point: Point2D类
    - planar_geometry.curve: 曲线类
    - math: 数学模块

使用示例:
    from planar_geometry import Circle
"""

import math
from typing import TYPE_CHECKING, List, Optional, Tuple

from planar_geometry.abstracts import Surface

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import Vector2D


class Circle(Surface):
    """
    圆形类

    说明:
        - 由圆心和半径定义的圆
        - 可计算面积和周长

    属性:
        center: Point2D - 圆心
        radius: float - 半径

    使用示例:
        circle = Circle(Point2D(0, 0), 5.0)
        print(circle.area())  # 78.54
    """

    TOLERANCE: float = 1e-6

    def __init__(self, center: "Point2D", radius: float) -> None:
        """
        初始化圆形

        Args:
            center: Point2D - 圆心
            radius: float - 半径

        异常:
            ValueError: 半径为负数
        """
        if radius < 0:
            raise ValueError("半径不能为负数")
        self.center = center
        self.radius = radius

    @staticmethod
    def from_diameter(p1: "Point2D", p2: "Point2D") -> "Circle":
        """
        从直径创建圆形（工厂方法）

        Args:
            p1: Point2D - 直径一端
            p2: Point2D - 直径另一端

        返回:
            Circle: 新圆形实例
        """
        center = p1.midpoint_to(p2)
        radius = p1.distance_to(p2) / 2.0
        return Circle(center, radius)

    def area(self) -> float:
        """
        计算圆形面积

        返回:
            float: 面积值 (πr²)
        """
        return math.pi * self.radius * self.radius

    def perimeter(self) -> float:
        """
        计算圆形周长

        返回:
            float: 周长值 (2πr)
        """
        return 2.0 * math.pi * self.radius

    def get_bounds(self) -> tuple:
        """
        获取轴对齐边界框 (AABB)

        返回:
            tuple: (x_min, y_min, x_max, y_max)
        """
        return (
            self.center.x - self.radius,
            self.center.y - self.radius,
            self.center.x + self.radius,
            self.center.y + self.radius,
        )

    def get_center(self) -> "Point2D":
        """
        获取圆心

        返回:
            Point2D: 圆心坐标
        """
        return self.center

    def contains_point(self, point: "Point2D") -> bool:
        """
        判断点是否在圆内或圆上

        Args:
            point: Point2D - 待检测点

        返回:
            bool: True 表示点在圆内或圆上
        """
        distance = point.distance_to(self.center)
        return distance <= self.radius + self.TOLERANCE

    def get_circumference(self) -> float:
        """
        获取圆周长（别名）

        返回:
            float: 周长值
        """
        return self.perimeter()

    def equals(self, other: object, tolerance: float = 1e-6) -> bool:
        """
        判断与另一圆是否相等

        Args:
            other: object - 比较对象
            tolerance: float - 容差

        返回:
            bool: 是否相等
        """
        if not isinstance(other, Circle):
            return False
        return (
            self.center.equals(other.center, tolerance)
            and abs(self.radius - other.radius) < tolerance
        )

    def __eq__(self, other: object) -> bool:
        return self.equals(other)

    def __repr__(self) -> str:
        return f"Circle({self.center}, radius={self.radius})"


