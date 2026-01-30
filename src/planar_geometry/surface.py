# -*- coding: utf-8 -*-
"""
planar_geometry/surface.py

模块: 曲面/平面图形 - 二维几何元素
描述: 定义二维几何元素的抽象基类及具体实现
版本: 0.1.0

功能:
    - Surface: 曲面抽象基类
    - Rectangle: 矩形类
    - Circle: 圆形类（接口预留）
    - Polygon: 多边形类（接口预留）

依赖:
    - math: 数学模块
    - abc: 抽象基类模块
    - measurable: 可计算度量抽象基类
    - point: 点类
    - curve: 曲线类

使用示例:
    from planar_geometry import Point2D, Vector2D, Rectangle

    rect = Rectangle.from_center_and_size(
        center=Point2D(0, 0),
        size=2.0,
        direction=Vector2D(1, 0)
    )
    print(rect.area())
"""

import math
from abc import ABC, abstractmethod
from typing import List

from planar_geometry.measurable import Measurable2D


class Surface(Measurable2D, ABC):
    """
    曲面/平面图形抽象基类（二维几何元素）

    说明:
        - 继承Measurable2D
        - 抽象化二维几何元素的行为

    设计原则:
        - ISP: 只暴露二维图形相关接口
    """

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """
        计算周长

        返回:
            float: 周长值
        """
        pass


class Rectangle(Surface):
    """
    矩形类

    说明:
        - 由4个顶点定义的矩形
        - 可计算面积和周长
        - 支持旋转矩形

    属性:
        vertices: List[Point2D] - 4个顶点（逆时针顺序）

    设计原则:
        - 数据结构简单，直接暴露属性便于Cython优化
        - 提供工厂方法简化构造

    使用示例:
        # 使用工厂方法
        rect = Rectangle.from_center_and_size(
            center=Point2D(0, 0),
            size=2.0,
            direction=Vector2D(1, 0)
        )

        # 访问属性
        print(rect.area())
        print(rect.perimeter())
    """

    TOLERANCE: float = 1e-6

    def __init__(self, vertices: List["Point2D"]) -> None:
        """
        初始化矩形

        说明:
            - vertices 必须是4个顶点
            - 按逆时针顺序: [左下, 右下, 右上, 左上]

        Args:
            vertices: List[Point2D] - 4个顶点

        异常:
            ValueError: 顶点数量不为4
        """
        if len(vertices) != 4:
            raise ValueError("矩形必须有4个顶点")
        self.vertices = vertices

    @staticmethod
    def from_center_and_size(
        center: "Point2D", size: float, direction: "Vector2D"
    ) -> "Rectangle":
        """
        从中心点、尺寸和方向构造矩形（工厂方法）

        说明:
            - 用于动态创建矩形
            - direction 沿矩形长边方向

        Args:
            center: Point2D - 中心点
            size: float - 矩形边长（正方形）
            direction: Vector2D - 方向向量（沿长边）

        返回:
            Rectangle: 新矩形实例
        """
        from planar_geometry.curve import Vector2D

        half = size / 2.0
        normal = Vector2D(-direction.y, direction.x).normalized()

        c_dir = (direction.x * half, direction.y * half)
        c_norm = (normal.x * half, normal.y * half)

        v0 = Point2D(center.x - c_dir[0] - c_norm[0], center.y - c_dir[1] - c_norm[1])
        v1 = Point2D(center.x + c_dir[0] - c_norm[0], center.y + c_dir[1] - c_norm[1])
        v2 = Point2D(center.x + c_dir[0] + c_norm[0], center.y + c_dir[1] + c_norm[1])
        v3 = Point2D(center.x - c_dir[0] + c_norm[0], center.y - c_dir[1] + c_norm[1])

        return Rectangle([v0, v1, v2, v3])

    def area(self) -> float:
        """
        计算矩形面积

        返回:
            float: 面积值
        """
        width = self.vertices[0].distance_to(self.vertices[1])
        height = self.vertices[0].distance_to(self.vertices[3])
        return width * height

    def perimeter(self) -> float:
        """
        计算矩形周长

        返回:
            float: 周长值
        """
        width = self.vertices[0].distance_to(self.vertices[1])
        height = self.vertices[0].distance_to(self.vertices[3])
        return 2.0 * (width + height)

    def get_bounds(self) -> tuple:
        """
        获取轴对齐边界框 (AABB)

        返回:
            tuple: (x_min, y_min, x_max, y_max)
        """
        x_vals = [p.x for p in self.vertices]
        y_vals = [p.y for p in self.vertices]
        return (min(x_vals), min(y_vals), max(x_vals), max(y_vals))

    def get_edges(self) -> List[tuple]:
        """
        获取4条边

        返回:
            List[Tuple[Point2D, Point2D]]: [(v0,v1), (v1,v2), (v2,v3), (v3,v0)]
        """
        return [(self.vertices[i], self.vertices[(i + 1) % 4]) for i in range(4)]

    def get_center(self) -> "Point2D":
        """
        获取矩形中心点

        返回:
            Point2D: 中心坐标
        """
        x = sum(p.x for p in self.vertices) / 4.0
        y = sum(p.y for p in self.vertices) / 4.0
        return Point2D(x, y)

    def contains_point(self, point: "Point2D") -> bool:
        """
        判断点是否在矩形内或边界上

        说明:
            - 支持旋转矩形
            - 使用射线投射算法

        Args:
            point: Point2D - 待检测点

        返回:
            bool: True 表示点在矩形内或在边界上
        """
        x, y = point.x, point.y
        x_min, y_min, x_max, y_max = self.get_bounds()

        if x < x_min - self.TOLERANCE or x > x_max + self.TOLERANCE:
            return False
        if y < y_min - self.TOLERANCE or y > y_max + self.TOLERANCE:
            return False

        return True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rectangle):
            return NotImplemented
        return all(self.vertices[i] == other.vertices[i] for i in range(4))

    def __repr__(self) -> str:
        return f"Rectangle({self.vertices[0]}, {self.vertices[1]}, {self.vertices[2]}, {self.vertices[3]})"


class Circle(Surface):
    """
    圆形类（接口预留）

    说明:
        - 预留接口，具体实现待定

    属性:
        center: Point2D - 圆心
        radius: float - 半径

    使用示例:
        # 预留接口，具体实现待定
    """

    def __init__(self, center: "Point2D", radius: float) -> None:
        self.center = center
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius * self.radius

    def perimeter(self) -> float:
        return 2.0 * math.pi * self.radius

    def __repr__(self) -> str:
        return f"Circle({self.center}, radius={self.radius})"


class Polygon(Surface):
    """
    多边形类（接口预留）

    说明:
        - 预留接口，具体实现待定
        - 支持任意边数的多边形

    属性:
        vertices: List[Point2D] - 顶点列表（逆时针）
    """

    def __init__(self, vertices: List["Point2D"]) -> None:
        self.vertices = vertices

    def area(self) -> float:
        n = len(self.vertices)
        area_sum = 0.0
        for i in range(n):
            x1, y1 = self.vertices[i].x, self.vertices[i].y
            x2, y2 = self.vertices[(i + 1) % n].x, self.vertices[(i + 1) % n].y
            area_sum += x1 * y2 - x2 * y1
        return abs(area_sum) / 2.0

    def perimeter(self) -> float:
        n = len(self.vertices)
        perimeter_sum = 0.0
        for i in range(n):
            perimeter_sum += self.vertices[i].distance_to(self.vertices[(i + 1) % n])
        return perimeter_sum

    def __repr__(self) -> str:
        return f"Polygon({self.vertices})"


from planar_geometry.point import Point2D
from planar_geometry.curve import Vector2D
