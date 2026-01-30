# -*- coding: utf-8 -*-
"""
planar_geometry/surface/rectangle.py

模块: Rectangle
描述: Rectangle类的实现
版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

依赖:
    - planar_geometry.abstracts: 抽象基类
    - planar_geometry.point: Point2D类
    - planar_geometry.curve: 曲线类
    - math: 数学模块

使用示例:
    from planar_geometry import Rectangle
"""

import math
from typing import TYPE_CHECKING, List, Optional, Tuple

from planar_geometry.abstracts import Surface

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import Vector2D


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
        half = size / 2.0
        normal = Vector2D(-direction.y, direction.x).normalized()

        c_dir = (direction.x * half, direction.y * half)
        c_norm = (normal.x * half, normal.y * half)

        v0 = Point2D(center.x - c_dir[0] - c_norm[0], center.y - c_dir[1] - c_norm[1])
        v1 = Point2D(center.x + c_dir[0] - c_norm[0], center.y + c_dir[1] - c_norm[1])
        v2 = Point2D(center.x + c_dir[0] + c_norm[0], center.y + c_dir[1] + c_norm[1])
        v3 = Point2D(center.x - c_dir[0] + c_norm[0], center.y - c_dir[1] + c_norm[1])

        return Rectangle([v0, v1, v2, v3])

    @staticmethod
    def from_bounds(
        x_min: float, y_min: float, x_max: float, y_max: float
    ) -> "Rectangle":
        """
        从边界框创建矩形（工厂方法）

        Args:
            x_min: float - 最小x
            y_min: float - 最小y
            x_max: float - 最大x
            y_max: float - 最大y

        返回:
            Rectangle: 新矩形实例
        """
        v0 = Point2D(x_min, y_min)
        v1 = Point2D(x_max, y_min)
        v2 = Point2D(x_max, y_max)
        v3 = Point2D(x_min, y_max)
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

    def get_edge_count(self) -> int:
        """
        获取边数

        返回:
            int: 4
        """
        return 4

    def get_vertex_count(self) -> int:
        """
        获取顶点数

        返回:
            int: 4
        """
        return 4

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
            - 使用AABB快速检测

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

    def is_square(self, tolerance: float = 1e-6) -> bool:
        """
        判断是否为正方形

        Args:
            tolerance: float - 容差

        返回:
            bool: 是否为正方形
        """
        width = self.vertices[0].distance_to(self.vertices[1])
        height = self.vertices[0].distance_to(self.vertices[3])
        return abs(width - height) < tolerance

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rectangle):
            return NotImplemented
        return all(self.vertices[i] == other.vertices[i] for i in range(4))

    def __repr__(self) -> str:
        return f"Rectangle({self.vertices[0]}, {self.vertices[1]}, {self.vertices[2]}, {self.vertices[3]})"


