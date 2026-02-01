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
        从三边长构造三角形（工厂方法）

        数学原理:
            已知三边长 a, b, c，使用海伦公式（Heron's formula）计算面积：

            .. math::

                s = \\frac{a + b + c}{2}  (\\text{半周长})

                A = \\sqrt{s(s-a)(s-b)(s-c)}

            随后通过三角形的高度公式构造具体的顶点坐标。

        三角形不等式条件：
            三条边长必须满足：

            .. math::

                a + b > c, \\quad a + c > b, \\quad b + c > a

        参数:
            a (float): 第一条边的长度（正数）
            b (float): 第二条边的长度（正数）
            c (float): 第三条边的长度（正数）

        返回:
            Triangle: 新的三角形实例

        异常:
            ValueError: 如果边长 ≤ 0 或不满足三角形不等式

        复杂度:
            O(1) - 常数时间操作

        使用示例::

            # 直角三角形 (3-4-5)
            tri_345 = Triangle.from_sides(3.0, 4.0, 5.0)
            assert abs(tri_345.area() - 6.0) < 1e-9

            # 等边三角形
            tri_eq = Triangle.from_sides(1.0, 1.0, 1.0)

            # 无效的三角形会抛出异常
            try:
                Triangle.from_sides(1.0, 2.0, 5.0)  # 1 + 2 ≤ 5
            except ValueError:
                print("不满足三角形不等式")
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
        计算三角形的三个内角

        数学原理:
            使用余弦定理（Law of Cosines）计算三个内角。
            设三角形的三边为 a, b, c，对应的角为 A, B, C，则：

            .. math::

                \\cos(A) = \\frac{b^2 + c^2 - a^2}{2bc}

                \\cos(B) = \\frac{a^2 + c^2 - b^2}{2ac}

                \\cos(C) = \\frac{a^2 + b^2 - c^2}{2ab}

            随后通过反余弦函数得到角度：

            .. math::

                A = \\arccos(\\cos(A)), \\quad B = \\arccos(\\cos(B)), \\quad C = \\arccos(\\cos(C))

        说明:
            - 返回值为度数 (degree)
            - 三个内角之和恒为 180°
            - 计算过程中会对 cos 值进行 clamp 处理以处理浮点误差

        返回:
            Tuple[float, float, float]: 三个内角，单位为度 (A, B, C)

        复杂度:
            O(1)

        使用示例::

            # 直角三角形 (3-4-5)
            tri = Triangle.from_sides(3.0, 4.0, 5.0)
            angles = tri.get_angles()
            A, B, C = angles

            # 应该有一个90度的角
            assert any(abs(angle - 90.0) < 1e-6 for angle in angles)

            # 内角和为180度
            assert abs(sum(angles) - 180.0) < 1e-6

            # 等边三角形
            tri_eq = Triangle.from_sides(1.0, 1.0, 1.0)
            angles_eq = tri_eq.get_angles()
            assert all(abs(angle - 60.0) < 1e-6 for angle in angles_eq)
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
        计算三角形的外心（外接圆圆心）

        数学定义:
            外心是三条边的垂直平分线的交点，也是外接圆的圆心。

        重要性质:
            - 外心到三个顶点的距离相等，都等于外接圆半径 R
            - 外心可能在三角形内部（锐角三角形）、边上（直角三角形）或外部（钝角三角形）
            - 外接圆是经过三角形三个顶点的圆

        计算方法:
            使用行列式法。设三个顶点为 P₁ = (x₁, y₁), P₂ = (x₂, y₂), P₃ = (x₃, y₃)，则外心坐标：

            .. math::

                O_x = \\frac{|(P_1|^2(P_2^y - P_3^y) + |P_2|^2(P_3^y - P_1^y) + |P_3|^2(P_1^y - P_2^y)|}{2D}

                O_y = \\frac{|(P_1|^2(P_3^x - P_2^x) + |P_2|^2(P_1^x - P_3^x) + |P_3|^2(P_2^x - P_1^x)|}{2D}

            其中 :math:`D` 是行列式：

            .. math::

                D = x_1(y_2 - y_3) + x_2(y_3 - y_1) + x_3(y_1 - y_2)

            （注：D 为0时三点共线）

        返回:
            Point2D: 外心坐标；若三点共线，返回三角形中心

        复杂度:
            O(1)

        应用场景:
            - 三角形外接圆计算
            - 圆周运动轨迹
            - 最小外包圆问题

        使用示例::

            # 直角三角形 - 外心在斜边中点
            tri = Triangle.from_sides(3.0, 4.0, 5.0)
            circumcenter = tri.circumcenter()

            # 验证：外心到三个顶点的距离相等
            v1, v2, v3 = tri.vertices
            d1 = circumcenter.distance_to(v1)
            d2 = circumcenter.distance_to(v2)
            d3 = circumcenter.distance_to(v3)
            assert abs(d1 - d2) < 1e-9
            assert abs(d2 - d3) < 1e-9
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
        计算三角形的内心（内切圆圆心）

        数学定义:
            内心是三条角平分线的交点，也是内切圆的圆心。

        重要性质:
            - 内心到三条边的距离相等，都等于内切圆半径 r
            - 内心总是在三角形内部
            - 内心分割三角形为三个较小的三角形，其面积与对应边长成正比

        计算方法:
            使用加权坐标法。设三个顶点为 P1, P2, P3，对边长分别为 a, b, c
            (a = |P2P3|, b = |P3P1|, c = |P1P2|)，则内心坐标为三个顶点
            的加权平均，权重为对边长：

            .. math::

                I = \\frac{a \\cdot P_1 + b \\cdot P_2 + c \\cdot P_3}{a + b + c}

                I_x = \\frac{a \\cdot x_1 + b \\cdot x_2 + c \\cdot x_3}{a + b + c}

                I_y = \\frac{a \\cdot y_1 + b \\cdot y_2 + c \\cdot y_3}{a + b + c}

            其中周长 :math:`p = a + b + c`

        返回:
            Point2D: 内心坐标

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 内切圆计算
            - 三角形分割问题
            - 几何最优化问题

        使用示例::

            # 直角三角形
            tri = Triangle.from_sides(3.0, 4.0, 5.0)
            incenter = tri.incenter()

            # 验证：内心到三条边的距离相等（等于内切圆半径）
            r = tri.inradius()
            # 内心应该在三角形内部
            assert tri.contains_point(incenter)
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
        计算三角形的垂心（三条高的交点）

        数学定义:
            垂心是从每个顶点到对边的垂线（高）的交点。

        重要性质:
            - 锐角三角形的垂心在三角形内部
            - 直角三角形的垂心在直角顶点上
            - 钝角三角形的垂心在三角形外部

        计算方法:
            使用行列式法。设三个顶点为 P1 = (x1, y1), P2 = (x2, y2), P3 = (x3, y3)，
            定义向量 P1P2 = (A, B) 和 P1P3 = (C, D)，则垂心坐标为：

            .. math::

                A = x_2 - x_1, \\quad B = y_2 - y_1

                C = x_3 - x_1, \\quad D = y_3 - y_1

                E = A(x_1 + x_2) + B(y_1 + y_2)

                F = C(x_1 + x_3) + D(y_1 + y_3)

                G = 2(A(x_2 - x_3) + B(y_2 - y_3))

                H_x = \\frac{DE - BF}{G}

                H_y = \\frac{AF - CE}{G}

            其中 :math:`G` 为行列式，当 :math:`G \\approx 0` 时三点共线

        返回:
            Point2D: 垂心坐标；若三点共线，返回三角形中心

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 垂足圆（九点圆）计算
            - 欧拉线（通过垂心、重心、外心的直线）
            - 高的计算

        使用示例::

            # 直角三角形 - 垂心在直角顶点
            tri = Triangle.from_sides(3.0, 4.0, 5.0)
            orthocenter = tri.orthocenter()

            # 等边三角形 - 垂心与重心、外心重合
            tri_eq = Triangle.from_sides(1.0, 1.0, 1.0)
            orthocenter_eq = tri_eq.orthocenter()
            centroid_eq = tri_eq.centroid()
            # assert orthocenter_eq 接近 centroid_eq
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
        计算三角形的外接圆半径

        数学定义:
            外接圆半径是通过三个顶点的圆的半径。

        计算方法（方法一 - 使用面积）:
            已知三角形的三边长 a, b, c 和面积 A，使用正弦定理的推导：

            .. math::

                R = \\frac{a}{2\\sin(A)} = \\frac{b}{2\\sin(B)} = \\frac{c}{2\\sin(C)}

            结合面积公式 :math:`A = \\frac{1}{2}bc\\sin(A)`，可得：

            .. math::

                R = \\frac{abc}{4A}

            其中 :math:`A` 由海伦公式计算：

            .. math::

                s = \\frac{a + b + c}{2} \\quad (\\text{半周长})

                A = \\sqrt{s(s-a)(s-b)(s-c)}

        重要性质:
            - 外接圆是经过三角形三个顶点的唯一圆
            - 外心（圆心）到三个顶点的距离都等于 R
            - 对于直角三角形，外接圆的直径等于斜边长

        返回:
            float: 外接圆半径；若三角形退化（面积为0），返回 inf

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 外接圆绘制与计算
            - 三角形的最小外包圆问题
            - 三角形相似性判定

        使用示例::

            # 直角三角形 (3-4-5) - 外接圆直径应为斜边 5
            tri_345 = Triangle.from_sides(3.0, 4.0, 5.0)
            R = tri_345.circumradius()
            assert abs(R - 2.5) < 1e-9  # R = 5/2

            # 等边三角形，边长为 a
            tri_eq = Triangle.from_sides(1.0, 1.0, 1.0)
            R_eq = tri_eq.circumradius()
            # R = a / sqrt(3) ≈ 0.577
            assert abs(R_eq - 1.0 / math.sqrt(3)) < 1e-9
        """
        a, b, c = self.get_side_lengths()
        s = (a + b + c) / 2.0
        area = self.area()

        if area < self.TOLERANCE:
            return float("inf")

        return (a * b * c) / (4 * area)

    def inradius(self) -> float:
        """
        计算三角形的内切圆半径

        数学定义:
            内切圆半径是与三角形三条边相切的圆的半径。

        计算方法:
            使用面积和半周长的关系。设三角形的三边长为 a, b, c，
            面积为 A，半周长为 s，则内切圆半径为：

            .. math::

                s = \\frac{a + b + c}{2}

                r = \\frac{A}{s}

            这个公式来自于三角形可以分解为三个小三角形，
            每个小三角形以内心为顶点，三角形的边为底：

            .. math::

                A = A_1 + A_2 + A_3 = \\frac{1}{2}ar + \\frac{1}{2}br + \\frac{1}{2}cr = \\frac{1}{2}(a+b+c)r = sr

                \\therefore r = \\frac{A}{s}

        重要性质:
            - 内切圆是与三角形三条边都相切的最大圆
            - 内心到三条边的距离都等于 r
            - 对于等腰直角三角形，r = (a - √2·c) / 2，其中 c 是直角边

        返回:
            float: 内切圆半径；若三角形退化（半周长为0），返回 0

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 内切圆绘制与计算
            - 三角形填充区域计算
            - 圆形容纳问题

        使用示例::

            # 直角三角形 (3-4-5)
            tri_345 = Triangle.from_sides(3.0, 4.0, 5.0)
            r = tri_345.inradius()
            # 面积为6，半周长为6，所以 r = 6/6 = 1
            assert abs(r - 1.0) < 1e-9

            # 等边三角形，边长为 a
            tri_eq = Triangle.from_sides(1.0, 1.0, 1.0)
            r_eq = tri_eq.inradius()
            # r = a / (2*sqrt(3)) ≈ 0.289
            assert abs(r_eq - 1.0 / (2 * math.sqrt(3))) < 1e-9
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
        """
        返回三角形的字符串表示

        说明:
            - 返回格式：Triangle(Point2D(...), Point2D(...), Point2D(...))
            - 用于调试和日志输出

        返回:
            str: 三角形的字符串表示

        复杂度:
            O(1) - 常数时间操作

        使用示例::

            tri = Triangle.from_sides(3.0, 4.0, 5.0)
            print(repr(tri))
            # 输出: Triangle(Point2D(0.0, 0.0), Point2D(3.0, 0.0), Point2D(...))
        """
        return f"Triangle({self.vertices[0]}, {self.vertices[1]}, {self.vertices[2]})"
