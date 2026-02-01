# -*- coding: utf-8 -*-
"""
planar_geometry/surface/triangle.py

模块: Triangle
描述: Triangle类的实现
版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

依赖:
    - planar_geometry.abstracts: 抽象基类
    - planar_geometry.point: Point2D类
    - planar_geometry.curve: 曲线类
    - math: 数学模块

使用示例:
    from planar_geometry import Triangle
"""

import math
from typing import TYPE_CHECKING, List, Optional, Tuple

from planar_geometry.abstracts import Surface
from planar_geometry.surface.polygon import Polygon
from planar_geometry.surface.circle import Circle
from planar_geometry.point import Point2D

if TYPE_CHECKING:
    from planar_geometry.curve import Vector2D


class Triangle(Polygon):
    """
    三角形类

    说明:
        - 继承自Polygon，特殊的三边多边形
        - 提供三角形特有的几何计算
        - 工厂方法：from_points(), from_sides()

    属性:
        vertices: List[Point2D] - 3个顶点

    使用示例::

        # 从三个点创建
        tri = Triangle.from_points([
            Point2D(0, 0),
            Point2D(3, 0),
            Point2D(0, 4)
        ])
        print(tri.area())  # 6.0

        # 已知三边长创建
        tri = Triangle.from_sides(3.0, 4.0, 5.0)
    """

    def __init__(self, vertices: List["Point2D"]) -> None:
        """
        初始化三角形

        说明:
            - vertices 必须是3个顶点
            - 按逆时针顺序排列

        Args:
            vertices: List[Point2D] - 3个顶点

        异常:
            ValueError: 顶点数不为3
        """
        if len(vertices) != 3:
            raise ValueError("三角形必须有3个顶点")
        super().__init__(vertices)

    @staticmethod
    def from_points(points: List["Point2D"]) -> "Triangle":
        """
        从三个点创建三角形（工厂方法）

        Args:
            points: List[Point2D] - 3个点

        返回:
            Triangle: 新三角形实例
        """
        return Triangle(points)

    @staticmethod
    def from_sides(a: float, b: float, c: float) -> "Triangle":
        """
        从三边长创建三角形（工厂方法）

        说明:
            - 使用海伦公式计算面积和高度
            - 自动定位顶点位置

        Args:
            a: float - 第一边长
            b: float - 第二边长
            c: float - 第三边长

        返回:
            Triangle: 新三角形实例

        异常:
            ValueError: 边长不满足三角形不等式
        """
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("边长必须为正数")

        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("边长不满足三角形不等式")

        s = (a + b + c) / 2.0
        area = math.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))

        p1 = Point2D(0, 0)
        p2 = Point2D(a, 0)

        if area < Triangle.TOLERANCE:
            return Triangle([p1, p2, Point2D(a / 2, 0)])

        height = 2 * area / a
        mid_x = a / 2

        if abs(b * b - (mid_x * mid_x + height * height)) < abs(
            c * c - (mid_x * mid_x + height * height)
        ):
            p3 = Point2D(mid_x, height)
        else:
            p3 = Point2D(mid_x, -height)

        return Triangle([p1, p2, p3])

    def get_side_lengths(self) -> Tuple[float, float, float]:
        """
        获取三条边的长度

        返回:
            Tuple[float, float, float]: (a, b, c) 三边长度
        """
        a = self.vertices[0].distance_to(self.vertices[1])
        b = self.vertices[1].distance_to(self.vertices[2])
        c = self.vertices[2].distance_to(self.vertices[0])
        return (a, b, c)

    def get_angles(self) -> Tuple[float, float, float]:
        """
        获取三个内角

        说明:
            - 返回角度值（度）

        返回:
            Tuple[float, float, float]: (A, B, C) 三个内角
        """
        a, b, c = self.get_side_lengths()

        cos_A = (b * b + c * c - a * a) / (2 * b * c)
        cos_B = (a * a + c * c - b * b) / (2 * a * c)
        cos_C = (a * a + b * b - c * c) / (2 * a * b)

        cos_A = max(-1.0, min(1.0, cos_A))
        cos_B = max(-1.0, min(1.0, cos_B))
        cos_C = max(-1.0, min(1.0, cos_C))

        A = math.degrees(math.acos(cos_A))
        B = math.degrees(math.acos(cos_B))
        C = math.degrees(math.acos(cos_C))

        return (A, B, C)

    def circumcenter(self) -> "Point2D":
        """
        获取外心（三边垂直平分线的交点）

        说明:
            - 外心到三个顶点的距离相等
            - 外接圆的圆心

        返回:
            Point2D: 外心坐标
        """
        p1, p2, p3 = self.vertices

        d = 2 * (p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y))

        if abs(d) < self.TOLERANCE:
            return self.get_center()

        ux = (
            (p1.x * p1.x + p1.y * p1.y) * (p2.y - p3.y)
            + (p2.x * p2.x + p2.y * p2.y) * (p3.y - p1.y)
            + (p3.x * p3.x + p3.y * p3.y) * (p1.y - p2.y)
        ) / d

        uy = (
            (p1.x * p1.x + p1.y * p1.y) * (p3.x - p2.x)
            + (p2.x * p2.x + p2.y * p2.y) * (p1.x - p3.x)
            + (p3.x * p3.x + p3.y * p3.y) * (p2.x - p1.x)
        ) / d

        return Point2D(ux, uy)

    def incenter(self) -> "Point2D":
        """
        获取内心（三条角平分线的交点）

        说明:
            - 内心到三边的距离相等
            - 内切圆的圆心

        返回:
            Point2D: 内心坐标
        """
        a, b, c = self.get_side_lengths()
        perimeter = a + b + c

        if perimeter < self.TOLERANCE:
            return self.get_center()

        p1, p2, p3 = self.vertices

        ux = (a * p1.x + b * p2.x + c * p3.x) / perimeter
        uy = (a * p1.y + b * p2.y + c * p3.y) / perimeter

        return Point2D(ux, uy)

    def orthocenter(self) -> "Point2D":
        """
        获取垂心（三条高的交点）

        返回:
            Point2D: 垂心坐标
        """
        p1, p2, p3 = self.vertices

        A = p2.x - p1.x
        B = p2.y - p1.y
        C = p3.x - p1.x
        D = p3.y - p1.y

        E = A * (p1.x + p2.x) + B * (p1.y + p2.y)
        F = C * (p1.x + p3.x) + D * (p1.y + p3.y)
        G = 2.0 * (A * (p2.x - p3.x) + B * (p2.y - p3.y))

        if abs(G) < self.TOLERANCE:
            return self.get_center()

        ix = (D * E - B * F) / G
        iy = (A * F - C * E) / G

        return Point2D(ix, iy)

    def centroid(self) -> "Point2D":
        """
        获取重心（三条中线的交点）

        说明:
            - 重心将每条中线分为2:1

        返回:
            Point2D: 重心坐标
        """
        return self.get_center()

    def circumradius(self) -> float:
        """
        获取外接圆半径

        返回:
            float: 外接圆半径
        """
        a, b, c = self.get_side_lengths()
        s = (a + b + c) / 2.0
        area = self.area()

        if area < self.TOLERANCE:
            return float("inf")

        return (a * b * c) / (4 * area)

    def inradius(self) -> float:
        """
        获取内切圆半径

        返回:
            float: 内切圆半径
        """
        a, b, c = self.get_side_lengths()
        s = (a + b + c) / 2.0
        area = self.area()

        if s < self.TOLERANCE:
            return 0.0

        return area / s

    def is_right_angled(self, tolerance: float = 1e-6) -> bool:
        """
        判断是否为直角三角形

        Args:
            tolerance: float - 容差

        返回:
            bool: 是否为直角三角形
        """
        a, b, c = self.get_side_lengths()
        sides = sorted([a, b, c])

        return abs(sides[0] * sides[0] + sides[1] * sides[1] - sides[2] * sides[2]) < tolerance

    def is_equilateral(self, tolerance: float = 1e-6) -> bool:
        """
        判断是否为等边三角形

        Args:
            tolerance: float - 容差

        返回:
            bool: 是否为等边三角形
        """
        a, b, c = self.get_side_lengths()
        return abs(a - b) < tolerance and abs(b - c) < tolerance and abs(a - c) < tolerance

    def is_isosceles(self, tolerance: float = 1e-6) -> bool:
        """
        判断是否为等腰三角形

        Args:
            tolerance: float - 容差

        返回:
            bool: 是否为等腰三角形
        """
        a, b, c = self.get_side_lengths()
        return abs(a - b) < tolerance or abs(b - c) < tolerance or abs(a - c) < tolerance

    def get_circumcircle(self) -> "Circle":
        """
        获取外接圆

        返回:
            Circle: 外接圆
        """
        center = self.circumcenter()
        radius = self.circumradius()
        return Circle(center, radius)

    def get_incicle(self) -> "Circle":
        """
        获取内切圆

        返回:
            Circle: 内切圆
        """
        center = self.incenter()
        radius = self.inradius()
        return Circle(center, radius)

    def __repr__(self) -> str:
        return f"Triangle({self.vertices[0]}, {self.vertices[1]}, {self.vertices[2]})"
