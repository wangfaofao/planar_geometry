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
from planar_geometry.point import Point2D
from planar_geometry.curve import LineSegment

if TYPE_CHECKING:
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

    使用示例::

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
    def regular(n: int, center: "Point2D", radius: float, rotation: float = 0.0) -> "Polygon":
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
    def rectangle(p1: "Point2D", p2: "Point2D", p3: "Point2D", p4: "Point2D") -> "Polygon":
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
        计算多边形的面积

        数学定义:
            多边形面积使用鞋带公式（Shoelace Formula，也称 Gauss Area Formula）计算。

        计算方法:
            设多边形有 n 个顶点 P0 = (x0, y0), P1 = (x1, y1), ..., Pn-1 = (xn-1, yn-1)，
            按逆时针顺序排列，则面积为：

            .. math::

                A = \\frac{1}{2} \\left| \\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i) \\right|

            其中约定 :math:`P_{n} = P_{0}` （首尾相连）。

            展开形式：

            .. math::

                A = \\frac{1}{2} |x_0(y_1 - y_{n-1}) + x_1(y_2 - y_0) + ... + x_{n-1}(y_0 - y_{n-2})|

        重要性质:
            - 无论顶点顺序如何，面积总是正数（使用绝对值）
            - 时间复杂度线性于顶点数 O(n)
            - 对于凸多边形和凹多边形都适用
            - 顶点顺序（顺时针或逆时针）不影响面积大小

        返回:
            float: 多边形的面积（非负）

        复杂度:
            O(n) - n 为顶点数

        应用场景:
            - 多边形面积计算
            - 图形重心计算
            - 碰撞检测中的面积比较

        使用示例::

            # 矩形：(0,0), (4,0), (4,3), (0,3)
            rect = Polygon([Point2D(0, 0), Point2D(4, 0),
                           Point2D(4, 3), Point2D(0, 3)])
            assert abs(rect.area() - 12.0) < 1e-9

            # 三角形：(0,0), (3,0), (0,4)
            tri = Polygon([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
            assert abs(tri.area() - 6.0) < 1e-9
        """
        n = len(self.vertices)
        area_sum = 0.0
        for i in range(n):
            x1, y1 = self.vertices[i].x, self.vertices[i].y
            x2, y2 = self.vertices[(i + 1) % n].x, self.vertices[(i + 1) % n].y
            area_sum += x1 * y2 - x2 * y1
        return abs(area_sum) / 2.0

    def test_simple_math(self) -> float:
        """
        测试简单公式: :math:`E = mc^2`。
        再测试你的复杂公式: :math:`A = \\frac{1}{2} | \\sum (x_i y_{i+1} - x_{i+1} y_i) |`。
        """
        return 0.0

    def perimeter(self) -> float:
        """
        计算多边形的周长

        数学定义:
            多边形周长是所有边长的和。设多边形有 n 个顶点 P0, P1, ..., Pn-1，则周长为：

            .. math::

                L = \\sum_{i=0}^{n-1} |P_{i} P_{i+1}|

            其中 :math:`|P_{i} P_{i+1}|` 表示相邻两个顶点之间的欧氏距离。

        返回:
            float: 多边形的周长

        复杂度:
            O(n) - n 为顶点数，每条边需要计算距离

        应用场景:
            - 计算多边形边界长度
            - 评估周长与面积比（如评估多边形"圆度"）
            - 路径规划和距离估计

        使用示例::

            # 单位正方形周长 = 4
            square = Polygon([Point2D(0, 0), Point2D(1, 0),
                            Point2D(1, 1), Point2D(0, 1)])
            assert abs(square.perimeter() - 4.0) < 1e-9

            # 直角三角形 (3-4-5) 周长 = 12
            tri = Polygon([Point2D(0, 0), Point2D(3, 0), Point2D(0, 4)])
            assert abs(tri.perimeter() - 12.0) < 1e-9
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

        数学定义:
            使用射线投射算法（Ray Casting Algorithm）判断点是否在多边形内部。

        计算方法:
            从点 P 向右发射一条射线，统计射线与多边形边界的交点数量：

            - 交点数为奇数：点在多边形内部
            - 交点数为偶数：点在多边形外部
            - 点在边界或顶点上：特殊判断

            算法步骤：

            1. 初始化计数器为 0
            2. 对于多边形的每条边 Pi -> Pi+1：
               - 如果点的 y 坐标在边的 y 范围内（但不包含上端点）
               - 且射线与边相交（通过 x 坐标判断）
               - 则计数器加 1
            3. 如果计数器为奇数，点在内部

            .. math::

                \\text{inside} = (\\text{intersection\\_count} \\mod 2) == 1

        返回:
            bool: True 表示点在多边形内或在边界上

        复杂度:
            O(n) - n 为顶点数

        应用场景:
            - 碰撞检测（点与多边形）
            - 区域查询（查找在特定区域内的对象）
            - 地理信息系统（点在地理区域内判定）

        使用示例::

            # 单位正方形
            square = Polygon([Point2D(0, 0), Point2D(1, 0),
                            Point2D(1, 1), Point2D(0, 1)])

            # 内部的点
            assert square.contains_point(Point2D(0.5, 0.5))

            # 外部的点
            assert not square.contains_point(Point2D(2, 2))

            # 边界上的点
            assert square.contains_point(Point2D(0.5, 0))
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
            if edge[0].equals(point, self.TOLERANCE) or edge[1].equals(point, self.TOLERANCE):
                return True
            segment = LineSegment(edge[0], edge[1])
            if segment.contains_point(point, self.TOLERANCE):
                return True

        return False

    def is_convex(self) -> bool:
        """
        判断多边形是否为凸多边形

        数学定义:
            凸多边形是所有内角都小于 180 度的多边形，等价于任意两个顶点的连线
            都在多边形内部。

        计算方法:
            使用叉积（Cross Product）检查所有连续三个顶点的转向方向是否一致：

            对于三个连续顶点 P0, P1, P2，计算向量的叉积：

            .. math::

                \\vec{v1} = P_1 - P_0, \\quad \\vec{v2} = P_2 - P_1

                \\text{cross} = v1_x \\cdot v2_y - v1_y \\cdot v2_x

            - 如果所有叉积同号（全正或全负），多边形为凸多边形
            - 如果叉积有不同符号，多边形为凹多边形
            - 叉积为 0 表示三点共线（退化情况）

            凸性判定：

            .. math::

                \\text{convex} = \\forall i: \\text{sign}(\\text{cross}_i) = \\text{constant}

        重要性质:
            - 三角形总是凸多边形
            - 凸多边形是凸集（任意两点连线在集合内）
            - 凸多边形的面积和周长计算更高效

        返回:
            bool: 是否为凸多边形

        复杂度:
            O(n) - n 为顶点数

        应用场景:
            - 碰撞检测优化（凸多边形使用分离轴定理 SAT）
            - 几何算法加速
            - 多边形分类

        使用示例::

            # 凸多边形 - 正方形
            square = Polygon([Point2D(0, 0), Point2D(1, 0),
                            Point2D(1, 1), Point2D(0, 1)])
            assert square.is_convex()

            # 凹多边形 - 五角星形
            star = Polygon([Point2D(0, 1), Point2D(0.2, 0.2),
                          Point2D(1, 0), Point2D(0.3, 0.4),
                          Point2D(0.5, -0.5)])
            assert not star.is_convex()
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

        数学定义:
            简单多边形是不存在自交（Self-intersection）的多边形。
            即：除了相邻边在顶点处的接触外，多边形的边不相交。

        计算方法:
            检查所有非相邻的边对是否相交。对于边 Edge_i 和 Edge_j（其中 :math:`|i - j| \geq 2`），
            检查它们是否在端点之外相交。

            特殊处理：
            - 相邻边：共享一个顶点，不被认为是相交
            - 首尾相邻的边：Edge_0 和 Edge_{n-1} 相邻

            .. math::

                \\text{simple} = \\forall i, j: |i - j| \\geq 2 \\land \\text{intersection}(E_i, E_j) = \\emptyset

        返回:
            bool: 是否为简单多边形（不自交）

        复杂度:
            O(n^2) - 需要检查所有边对的相交情况

        应用场景:
            - 多边形有效性验证
            - 自交多边形的检测与修复
            - 几何数据清理

        使用示例::

            # 简单多边形 - 正方形
            square = Polygon([Point2D(0, 0), Point2D(1, 0),
                            Point2D(1, 1), Point2D(0, 1)])
            assert square.is_simple()

            # 自交多边形 - 蝴蝶形（相对位置使得边相交）
            # butterfly = Polygon([...])  # 某些配置会产生自交
            # assert not butterfly.is_simple()
        """
        from planar_geometry.utils import line_segment_intersection

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

        数学定义:
            正多边形（Regular Polygon）是所有边等长且所有内角相等的多边形。
            对于 n 边形，每个内角为：

            .. math::

                \\theta = \\frac{(n-2) \\times 180°}{n}

        判定条件:
            1. 所有边长相等：

               .. math::

                   |P_i - P_{i+1}| = L, \\quad \\forall i

            2. 所有内角相等：

               .. math::

                   \\angle P_{i-1} P_i P_{i+1} = \\theta, \\quad \\forall i

            采用标准差方法判定相等性，允许浮点误差。

        计算方法:
            1. 计算所有边长，检查标准差是否小于容差 TOLERANCE
            2. 计算所有内角（使用向量点积和反余弦），检查标准差是否小于容差
            3. 两个条件都满足则为正多边形

        返回:
            bool: 是否为正多边形

        复杂度:
            O(n) - n 为顶点数

        应用场景:
            - 多边形分类
            - 对称性检测
            - 正多边形构造验证

        使用示例::

            # 正三角形
            tri_eq = Polygon.regular(3, Point2D(0, 0), 1.0)
            assert tri_eq.is_regular()

            # 正方形
            square = Polygon.regular(4, Point2D(0, 0), 1.0)
            assert square.is_regular()

            # 非正多边形 - 矩形（不是正方形）
            rect = Polygon([Point2D(0, 0), Point2D(2, 0),
                          Point2D(2, 1), Point2D(0, 1)])
            assert not rect.is_regular()
        """
        n = len(self.vertices)
        if n < 3:
            return False

        edge_lengths = []
        for i in range(n):
            length = self.vertices[i].distance_to(self.vertices[(i + 1) % n])
            edge_lengths.append(length)

        length_std = math.sqrt(sum((l - sum(edge_lengths) / n) ** 2 for l in edge_lengths) / n)
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
            angle_std = math.sqrt(sum((a - angle_mean) ** 2 for a in angles) / len(angles))

        return angle_std < self.TOLERANCE

    def get_convex_hull(self) -> "Polygon":
        """
        计算多边形顶点的凸包

        数学定义:
            凸包（Convex Hull）是包含所有给定点的最小凸多边形。

        计算方法:
            使用 Graham Scan（格雷厄姆扫描）算法，时间复杂度 O(n log n)：

            1. **排序**：按 x 坐标（主）和 y 坐标（次）升序排列所有点
            2. **下链**：从左到右扫描，构建下凸包
            3. **上链**：从右到左扫描，构建上凸包
            4. **合并**：组合下链和上链得到完整凸包

            判断转向方向使用叉积（Cross Product）：

            .. math::

                \\text{cross}(O, A, B) = (A_x - O_x)(B_y - O_y) - (A_y - O_y)(B_x - O_x)

            - cross > 0：左转（逆时针）
            - cross < 0：右转（顺时针）
            - cross = 0：共线

        返回:
            Polygon: 凸包多边形（顶点按逆时针排列）

        复杂度:
            O(n log n) - 主要由排序阶段决定

        应用场景:
            - 碰撞检测（凸包与凸包）
            - 最小外包形状计算
            - 计算几何中的基础操作

        使用示例::

            # 从不规则点集计算凸包
            points = Polygon([Point2D(0, 0), Point2D(2, 2),
                            Point2D(2, 0), Point2D(1, 1)])  # (1,1)在三角形内
            hull = points.get_convex_hull()
            # 凸包应该只有外面的三个顶点
            assert hull.get_vertex_count() == 3
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
