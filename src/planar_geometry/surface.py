# -*- coding: utf-8 -*-
"""
planar_geometry/surface.py

模块: 曲面/平面图形 - 二维几何元素
描述: 定义二维几何元素的抽象基类及具体实现
版本: 0.01
作者: wangheng <wangfaofao@gmail.com>

功能:
    - Surface: 曲面抽象基类
    - Rectangle: 矩形类
    - Circle: 圆形类
    - Polygon: 多边形类

依赖:
    - math: 数学模块
    - abc: 抽象基类模块
    - typing: 类型提示
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
from typing import List, Optional, Tuple

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


class Triangle(Polygon):
    """
    三角形类

    说明:
        - 继承自Polygon，特殊的三边多边形
        - 提供三角形特有的几何计算
        - 工厂方法：from_points(), from_sides()

    属性:
        vertices: List[Point2D] - 3个顶点

    使用示例:
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

        return (
            abs(sides[0] * sides[0] + sides[1] * sides[1] - sides[2] * sides[2])
            < tolerance
        )

    def is_equilateral(self, tolerance: float = 1e-6) -> bool:
        """
        判断是否为等边三角形

        Args:
            tolerance: float - 容差

        返回:
            bool: 是否为等边三角形
        """
        a, b, c = self.get_side_lengths()
        return (
            abs(a - b) < tolerance and abs(b - c) < tolerance and abs(a - c) < tolerance
        )

    def is_isosceles(self, tolerance: float = 1e-6) -> bool:
        """
        判断是否为等腰三角形

        Args:
            tolerance: float - 容差

        返回:
            bool: 是否为等腰三角形
        """
        a, b, c = self.get_side_lengths()
        return (
            abs(a - b) < tolerance or abs(b - c) < tolerance or abs(a - c) < tolerance
        )

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
