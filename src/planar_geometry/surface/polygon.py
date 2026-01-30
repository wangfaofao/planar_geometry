# -*- coding: utf-8 -*-
"""
planar_geometry/surface/polygon.py

模块: Polygon
描述: Polygon类的实现
版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

依赖:
    - planar_geometry.abstracts: 抽象基类
    - planar_geometry.point: Point2D类
    - planar_geometry.curve: 曲线类
    - math: 数学模块

使用示例:
    from planar_geometry import Polygon
"""

import math
from typing import TYPE_CHECKING, List, Optional, Tuple

from planar_geometry.abstracts import Surface

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import Vector2D


class Polygon(Surface):
    """
    多边形类

    说明:
        - 由顶点列表定义的多边形
        - 支持任意边数
        - 顶点按逆时针顺序排列

    属性:
        vertices: List[Point2D] - 顶点列表（逆时针）

    使用示例:
        # 三角形
        tri = Polygon([
            Point2D(0, 0),
            Point2D(3, 0),
            Point2D(0, 4)
        ])
        print(tri.area())  # 6.0

        # 四边形
        quad = Polygon([
            Point2D(0, 0),
            Point2D(4, 0),
            Point2D(4, 3),
            Point2D(0, 3)
        ])
        print(quad.area())  # 12.0
    """

    TOLERANCE: float = 1e-6

    def __init__(self, vertices: List["Point2D"]) -> None:
        """
        初始化多边形

        说明:
            - vertices 至少需要3个顶点
            - 按逆时针顺序排列

        Args:
            vertices: List[Point2D] - 顶点列表

        异常:
            ValueError: 顶点数少于3
        """
        if len(vertices) < 3:
            raise ValueError("多边形至少有3个顶点")
        self.vertices = vertices

    @staticmethod
    def from_points(points: List["Point2D"]) -> "Polygon":
        """
        从点列表创建多边形（工厂方法）

        Args:
            points: List[Point2D] - 点列表

        返回:
            Polygon: 新多边形实例
        """
        return Polygon(points)

    @staticmethod
    def regular(
        n: int, center: "Point2D", radius: float, rotation: float = 0.0
    ) -> "Polygon":
        """
        创建正多边形（工厂方法）

        Args:
            n: int - 边数
            center: Point2D - 中心点
            radius: float - 外接圆半径
            rotation: float - 旋转角度（度）

        返回:
            Polygon: 正多边形实例

        异常:
            ValueError: 边数少于3
        """
        if n < 3:
            raise ValueError("正多边形至少有3边")

        vertices = []
        angle_step = 2.0 * math.pi / n
        rotation_rad = math.radians(rotation)

        for i in range(n):
            angle = i * angle_step + rotation_rad
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            vertices.append(Point2D(x, y))

        return Polygon(vertices)

    @staticmethod
    def triangle(p1: "Point2D", p2: "Point2D", p3: "Point2D") -> "Polygon":
        """
        从三个点创建三角形（工厂方法）

        Args:
            p1: Point2D - 第一个顶点
            p2: Point2D - 第二个顶点
            p3: Point2D - 第三个顶点

        返回:
            Polygon: 三角形实例
        """
        return Polygon([p1, p2, p3])

    @staticmethod
    def rectangle(
        p1: "Point2D", p2: "Point2D", p3: "Point2D", p4: "Point2D"
    ) -> "Polygon":
        """
        从四个点创建四边形（工厂方法）

        Args:
            p1-p4: Point2D - 四个顶点

        返回:
            Polygon: 四边形实例
        """
        return Polygon([p1, p2, p3, p4])

    def area(self) -> float:
        """
        计算多边形面积

        说明:
            - 使用鞋带公式（Shoelace Formula）
            - area = |Σ(x_i * y_{i+1} - x_{i+1} * y_i)| / 2

        返回:
            float: 面积值
        """
        n = len(self.vertices)
        area_sum = 0.0
        for i in range(n):
            x1, y1 = self.vertices[i].x, self.vertices[i].y
            x2, y2 = self.vertices[(i + 1) % n].x, self.vertices[(i + 1) % n].y
            area_sum += x1 * y2 - x2 * y1
        return abs(area_sum) / 2.0

    def perimeter(self) -> float:
        """
        计算多边形周长

        返回:
            float: 周长值
        """
        n = len(self.vertices)
        perimeter_sum = 0.0
        for i in range(n):
            perimeter_sum += self.vertices[i].distance_to(self.vertices[(i + 1) % n])
        return perimeter_sum

    def get_bounds(self) -> tuple:
        """
        获取轴对齐边界框 (AABB)

        返回:
            tuple: (x_min, y_min, x_max, y_max)
        """
        x_vals = [p.x for p in self.vertices]
        y_vals = [p.y for p in self.vertices]
        return (min(x_vals), min(y_vals), max(x_vals), max(y_vals))

    def get_center(self) -> "Point2D":
        """
        获取多边形中心（重心）

        说明:
            - 计算所有顶点的平均值
            - 对于简单多边形是合理的近似

        返回:
            Point2D: 中心坐标
        """
        n = len(self.vertices)
        x = sum(p.x for p in self.vertices) / n
        y = sum(p.y for p in self.vertices) / n
        return Point2D(x, y)

    def centroid(self) -> "Point2D":
        """
        获取多边形质心

        说明:
            - 使用顶点加权平均
            - 对于非均匀密度的多边形可能不准确

        返回:
            Point2D: 质心坐标
        """
        return self.get_center()

    def get_edges(self) -> List[tuple]:
        """
        获取所有边

        返回:
            List[Tuple[Point2D, Point2D]]: 边列表
        """
        n = len(self.vertices)
        return [(self.vertices[i], self.vertices[(i + 1) % n]) for i in range(n)]

    def get_edge_count(self) -> int:
        """
        获取边数

        返回:
            int: 边数（等于顶点数）
        """
        return len(self.vertices)

    def get_vertex_count(self) -> int:
        """
        获取顶点数

        返回:
            int: 顶点数
        """
        return len(self.vertices)

    def get_vertex(self, index: int) -> "Point2D":
        """
        获取指定索引的顶点

        Args:
            index: int - 索引（支持负数）

        返回:
            Point2D: 顶点坐标
        """
        n = len(self.vertices)
        idx = index % n
        return self.vertices[idx]

    def get_edge(self, index: int) -> tuple:
        """
        获取指定索引的边

        Args:
            index: int - 边索引

        返回:
            Tuple[Point2D, Point2D]: 边
        """
        n = len(self.vertices)
        idx = index % n
        return (self.vertices[idx], self.vertices[(idx + 1) % n])

    def contains_point(self, point: "Point2D") -> bool:
        """
        判断点是否在多边形内或边界上

        说明:
            - 使用射线投射算法（Ray Casting）
            - 统计从点出发的射线与多边形边界的交点数
            - 奇数个交点：点在多边形内

        Args:
            point: Point2D - 待检测点

        返回:
            bool: True 表示点在多边形内或在边界上
        """
        x, y = point.x, point.y
        n = len(self.vertices)
        inside = False

        j = n - 1
        for i in range(n):
            xi, yi = self.vertices[i].x, self.vertices[i].y
            xj, yj = self.vertices[j].x, self.vertices[j].y

            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside

            j = i

        if inside:
            return True

        for i in range(n):
            edge = self.get_edge(i)
            if edge[0].equals(point, self.TOLERANCE) or edge[1].equals(
                point, self.TOLERANCE
            ):
                return True
            segment = LineSegment(edge[0], edge[1])
            if segment.contains_point(point, self.TOLERANCE):
                return True

        return False

    def is_convex(self) -> bool:
        """
        判断多边形是否为凸多边形

        说明:
            - 检查所有内角是否都小于180度
            - 使用叉积符号一致性判断

        返回:
            bool: 是否为凸多边形
        """
        n = len(self.vertices)
        if n < 4:
            return True

        sign = 0
        for i in range(n):
            p0 = self.vertices[i]
            p1 = self.vertices[(i + 1) % n]
            p2 = self.vertices[(i + 2) % n]

            v1 = (p1.x - p0.x, p1.y - p0.y)
            v2 = (p2.x - p1.x, p2.y - p1.y)

            cross = v1[0] * v2[1] - v1[1] * v2[0]

            if abs(cross) > self.TOLERANCE:
                if sign == 0:
                    sign = 1 if cross > 0 else -1
                elif (cross > 0 and sign < 0) or (cross < 0 and sign > 0):
                    return False

        return True

    def is_simple(self) -> bool:
        """
        判断多边形是否为简单多边形（不自交）

        说明:
            - 检查非相邻边是否相交
            - O(n²) 复杂度

        返回:
            bool: 是否为简单多边形
        """
        n = len(self.vertices)
        edges = self.get_edges()

        for i in range(n):
            for j in range(i + 2, n):
                if j == i or (i == 0 and j == n - 1):
                    continue

                edge1 = edges[i]
                edge2 = edges[j]

                intersection = line_segment_intersection(
                    LineSegment(edge1[0], edge1[1]), LineSegment(edge2[0], edge2[1])
                )

                if intersection is not None:
                    return False

        return True

    def is_regular(self) -> bool:
        """
        判断多边形是否为正多边形

        说明:
            - 所有边等长
            - 所有内角相等

        返回:
            bool: 是否为正多边形
        """
        n = len(self.vertices)
        if n < 3:
            return False

        edge_lengths = []
        for i in range(n):
            length = self.vertices[i].distance_to(self.vertices[(i + 1) % n])
            edge_lengths.append(length)

        length_std = math.sqrt(
            sum((l - sum(edge_lengths) / n) ** 2 for l in edge_lengths) / n
        )
        if length_std > self.TOLERANCE:
            return False

        angles = []
        for i in range(n):
            p0 = self.vertices[(i - 1) % n]
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % n]

            v1 = (p0.x - p1.x, p0.y - p1.y)
            v2 = (p2.x - p1.x, p2.y - p1.y)

            dot = v1[0] * v2[0] + v1[1] * v2[1]
            len1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
            len2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

            if len1 > 0 and len2 > 0:
                cos_angle = dot / (len1 * len2)
                cos_angle = max(-1.0, min(1.0, cos_angle))
                angle = math.degrees(math.acos(cos_angle))
                angles.append(angle)

        angle_std = 0.0
        if angles:
            angle_mean = sum(angles) / len(angles)
            angle_std = math.sqrt(
                sum((a - angle_mean) ** 2 for a in angles) / len(angles)
            )

        return angle_std < self.TOLERANCE

    def get_convex_hull(self) -> "Polygon":
        """
        获取凸包

        说明:
            - 使用 Graham Scan 算法
            - 返回包含所有顶点的最小凸多边形

        返回:
            Polygon: 凸包多边形
        """
        points = sorted(self.vertices, key=lambda p: (p.x, p.y))

        if len(points) <= 2:
            return Polygon(points)

        def cross(o: "Point2D", a: "Point2D", b: "Point2D") -> float:
            return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= self.TOLERANCE:
                lower.pop()
            lower.append(p)

        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= self.TOLERANCE:
                upper.pop()
            upper.append(p)

        hull = lower[:-1] + upper[:-1]
        return Polygon(hull)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polygon):
            return NotImplemented
        if len(self.vertices) != len(other.vertices):
            return False
        return all(
            self.vertices[i].equals(other.vertices[i], self.TOLERANCE)
            for i in range(len(self.vertices))
        )

    def __repr__(self) -> str:
        return f"Polygon({self.vertices})"


