# -*- coding: utf-8 -*-
"""
planar_geometry/surface/ellipse.py

模块: Ellipse
描述: Ellipse类的实现
版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

依赖:
    - planar_geometry.abstracts: 抽象基类
    - planar_geometry.point: Point2D类
    - planar_geometry.curve: 曲线类
    - math: 数学模块

使用示例:
    from planar_geometry import Ellipse
"""

import math
from typing import TYPE_CHECKING, List, Optional, Tuple

from planar_geometry.abstracts import Surface

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import Vector2D


class Ellipse(Surface):
    """
    椭圆类

    说明:
        - 由中心点、长轴和短轴定义的椭圆
        - 支持椭圆的几何计算

    属性:
        center: Point2D - 椭圆中心
        semi_major: float - 半长轴长度
        semi_minor: float - 半短轴长度
        rotation: float - 旋转角度（度）

    使用示例:
        ellipse = Ellipse(Point2D(0, 0), 5.0, 3.0)
        print(ellipse.area())  # 47.12
    """

    TOLERANCE: float = 1e-6

    def __init__(
        self,
        center: "Point2D",
        semi_major: float,
        semi_minor: float,
        rotation: float = 0.0,
    ) -> None:
        """
        初始化椭圆

        Args:
            center: Point2D - 椭圆中心
            semi_major: float - 半长轴长度（必须 >= semi_minor）
            semi_minor: float - 半短轴长度
            rotation: float - 旋转角度（度）

        异常:
            ValueError: 轴长为负或 semi_major < semi_minor
        """
        if semi_major < 0 or semi_minor < 0:
            raise ValueError("轴长不能为负数")

        if semi_major < semi_minor:
            raise ValueError("semi_major 必须 >= semi_minor")

        self.center = center
        self.semi_major = semi_major
        self.semi_minor = semi_minor
        self.rotation = rotation

    @staticmethod
    def from_center_and_axes(
        center: "Point2D", major_axis: float, minor_axis: float, rotation: float = 0.0
    ) -> "Ellipse":
        """
        从中心和轴创建椭圆（工厂方法）

        Args:
            center: Point2D - 椭圆中心
            major_axis: float - 长轴长度
            minor_axis: float - 短轴长度
            rotation: float - 旋转角度（度）

        返回:
            Ellipse: 新椭圆实例
        """
        return Ellipse(center, major_axis / 2, minor_axis / 2, rotation)

    @staticmethod
    def from_foci_and_point(
        focus1: "Point2D", focus2: "Point2D", point: "Point2D"
    ) -> "Ellipse":
        """
        从两个焦点和椭圆上一点创建椭圆（工厂方法）

        Args:
            focus1: Point2D - 第一个焦点
            focus2: Point2D - 第二个焦点
            point: Point2D - 椭圆上的点

        返回:
            Ellipse: 新椭圆实例
        """
        center = focus1.midpoint_to(focus2)
        c = focus1.distance_to(center)
        d = point.distance_to(focus1) + point.distance_to(focus2)
        major_axis = d

        if major_axis < 2 * c + Ellipse.TOLERANCE:
            raise ValueError("焦点间距不能大于等于2a")

        semi_major = major_axis / 2
        semi_minor = math.sqrt(semi_major * semi_major - c * c)

        rotation = math.degrees(math.atan2(focus2.y - focus1.y, focus2.x - focus1.x))

        return Ellipse(center, semi_major, semi_minor, rotation)

    def area(self) -> float:
        """
        计算椭圆面积

        返回:
            float: 面积值 (π * a * b)
        """
        return math.pi * self.semi_major * self.semi_minor

    def perimeter(self) -> float:
        """
        计算椭圆周长

        说明:
            - 使用 Ramanujan 近似公式
            - 较高精度且计算高效

        返回:
            float: 周长近似值
        """
        a = self.semi_major
        b = self.semi_minor

        h = ((a - b) * (a - b)) / ((a + b) * (a + b))

        return math.pi * (a + b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))

    def eccentricity(self) -> float:
        """
        获取离心率

        返回:
            float: 离心率 e = sqrt(1 - b²/a²)
        """
        if self.semi_major < self.TOLERANCE:
            return 0.0

        return math.sqrt(
            1
            - (self.semi_minor * self.semi_minor) / (self.semi_major * self.semi_major)
        )

    def focal_distance(self) -> float:
        """
        获取焦距（两焦点间距的一半）

        返回:
            float: 焦距 c = sqrt(a² - b²)
        """
        return math.sqrt(
            self.semi_major * self.semi_major - self.semi_minor * self.semi_minor
        )

    def foci(self) -> Tuple["Point2D", "Point2D"]:
        """
        获取两个焦点

        返回:
            Tuple[Point2D, Point2D]: (focus1, focus2)
        """
        c = self.focal_distance()
        rotation_rad = math.radians(self.rotation)

        dx = c * math.cos(rotation_rad)
        dy = c * math.sin(rotation_rad)

        focus1 = Point2D(self.center.x - dx, self.center.y - dy)
        focus2 = Point2D(self.center.x + dx, self.center.y + dy)

        return (focus1, focus2)

    def get_bounds(self) -> tuple:
        """
        获取轴对齐边界框 (AABB)

        返回:
            tuple: (x_min, y_min, x_max, y_max)
        """
        a = self.semi_major
        b = self.semi_minor

        if (
            abs(self.rotation) < self.TOLERANCE
            or abs(self.rotation - 180) < self.TOLERANCE
        ):
            return (
                self.center.x - a,
                self.center.y - b,
                self.center.x + a,
                self.center.y + b,
            )

        cos_r = abs(math.cos(math.radians(self.rotation)))
        sin_r = abs(math.sin(math.radians(self.rotation)))

        half_width = a * cos_r + b * sin_r
        half_height = a * sin_r + b * cos_r

        return (
            self.center.x - half_width,
            self.center.y - half_height,
            self.center.x + half_width,
            self.center.y + half_height,
        )

    def get_center(self) -> "Point2D":
        """
        获取椭圆中心

        返回:
            Point2D: 中心坐标
        """
        return self.center

    def contains_point(self, point: "Point2D") -> bool:
        """
        判断点是否在椭圆内或边界上

        说明:
            - 使用椭圆方程判断
            - 考虑旋转角度

        Args:
            point: Point2D - 待检测点

        返回:
            bool: True 表示点在椭圆内或在边界上
        """
        dx = point.x - self.center.x
        dy = point.y - self.center.y

        rotation_rad = math.radians(self.rotation)
        cos_r = math.cos(rotation_rad)
        sin_r = math.sin(rotation_rad)

        x_rot = dx * cos_r + dy * sin_r
        y_rot = -dx * sin_r + dy * cos_r

        a = self.semi_major
        b = self.semi_minor

        value = (x_rot * x_rot) / (a * a) + (y_rot * y_rot) / (b * b)

        return value <= 1.0 + self.TOLERANCE

    def get_major_axis_endpoints(self) -> Tuple["Point2D", "Point2D"]:
        """
        获取长轴的两个端点

        返回:
            Tuple[Point2D, Point2D]: (end1, end2)
        """
        rotation_rad = math.radians(self.rotation)
        cos_r = math.cos(rotation_rad)
        sin_r = math.sin(rotation_rad)

        dx = self.semi_major * cos_r
        dy = self.semi_major * sin_r

        end1 = Point2D(self.center.x - dx, self.center.y - dy)
        end2 = Point2D(self.center.x + dx, self.center.y + dy)

        return (end1, end2)

    def get_minor_axis_endpoints(self) -> Tuple["Point2D", "Point2D"]:
        """
        获取短轴的两个端点

        返回:
            Tuple[Point2D, Point2D]: (end1, end2)
        """
        rotation_rad = math.radians(self.rotation + 90)
        cos_r = math.cos(rotation_rad)
        sin_r = math.sin(rotation_rad)

        dx = self.semi_minor * cos_r
        dy = self.semi_minor * sin_r

        end1 = Point2D(self.center.x - dx, self.center.y - dy)
        end2 = Point2D(self.center.x + dx, self.center.y + dy)

        return (end1, end2)

    def equals(self, other: object, tolerance: float = 1e-6) -> bool:
        """
        判断与另一椭圆是否相等

        Args:
            other: object - 比较对象
            tolerance: float - 容差

        返回:
            bool: 是否相等
        """
        if not isinstance(other, Ellipse):
            return False

        return (
            self.center.equals(other.center, tolerance)
            and abs(self.semi_major - other.semi_major) < tolerance
            and abs(self.semi_minor - other.semi_minor) < tolerance
            and abs(self.rotation - other.rotation) < tolerance
        )

    def __eq__(self, other: object) -> bool:
        return self.equals(other)

    def __repr__(self) -> str:
        return (
            f"Ellipse(center={self.center}, "
            f"semi_major={self.semi_major}, "
            f"semi_minor={self.semi_minor}, "
            f"rotation={self.rotation})"
        )


from planar_geometry.point import Point2D
from planar_geometry.curve import Vector2D, LineSegment
from planar_geometry.geometry_utils import line_segment_intersection
