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
from planar_geometry.point import Point2D

if TYPE_CHECKING:
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
        计算圆形的面积

        数学定义:
            圆形面积公式为：

            .. math::

                A = \\pi r^2

            其中 r 是圆的半径。

        返回:
            float: 面积值（非负）

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 面积计算和比较
            - 覆盖区域估计
            - 资源分配问题

        使用示例::

            from planar_geometry import Circle, Point2D
            import math

            # 半径为 1 的圆，面积应该是 π
            circle = Circle(Point2D(0, 0), 1.0)
            assert abs(circle.area() - math.pi) < 1e-9

            # 半径为 5 的圆，面积应该是 25π
            circle2 = Circle(Point2D(0, 0), 5.0)
            assert abs(circle2.area() - 25 * math.pi) < 1e-9
        """
        return math.pi * self.radius * self.radius

    def perimeter(self) -> float:
        """
        计算圆形的周长（周长与圆周长相同）

        数学定义:
            圆的周长（也称圆周长或圆周率）公式为：

            .. math::

                C = 2\\pi r = \\pi d

            其中 r 是半径，d = 2r 是直径。

        重要性质:
            - 周长与直径的比为常数 π
            - 周长是圆的边界长度

        返回:
            float: 周长值（非负）

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 周长计算
            - 运动轨迹长度
            - 材料用量估计

        使用示例::

            from planar_geometry import Circle, Point2D
            import math

            # 半径为 1 的圆，周长应该是 2π
            circle = Circle(Point2D(0, 0), 1.0)
            assert abs(circle.perimeter() - 2 * math.pi) < 1e-9

            # 半径为 5 的圆，周长应该是 10π
            circle2 = Circle(Point2D(0, 0), 5.0)
            assert abs(circle2.perimeter() - 10 * math.pi) < 1e-9
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

        数学定义:
            点 P 在圆内（或圆上）当且仅当点到圆心的距离小于等于半径。

            设圆心为 C，半径为 r，则点 P 在圆内：

            .. math::

                |P - C| \\leq r

            考虑浮点误差，引入容差 tolerance：

            .. math::

                |P - C| \\leq r + \\text{tolerance}

        判定规则:
            - 距离 < r：点在圆内部
            - 距离 = r（容差内）：点在圆周上
            - 距离 > r：点在圆外

        参数:
            point (Point2D): 待检测点

        返回:
            bool: True 表示点在圆内或圆上

        复杂度:
            O(1) - 常数时间操作

        应用场景:
            - 圆与点的碰撞检测
            - 区域包含关系判定
            - 圆形掩码生成

        使用示例::

            from planar_geometry import Circle, Point2D

            # 以原点为圆心，半径为 5 的圆
            circle = Circle(Point2D(0, 0), 5.0)

            # 圆心在圆内
            assert circle.contains_point(Point2D(0, 0))

            # 圆周上的点 (5, 0)
            assert circle.contains_point(Point2D(5, 0))

            # 圆内的点 (3, 4)
            assert circle.contains_point(Point2D(3, 4))

            # 圆外的点 (6, 0)
            assert not circle.contains_point(Point2D(6, 0))
        """
        distance = point.distance_to(self.center)
        return distance <= self.radius + self.TOLERANCE

    def get_circumference(self) -> float:
        """
        获取圆的周长（别名方法）

        说明:
            这是 `perimeter()` 方法的别名。在几何学中，"周长"和"圆周长"
            通常用来指代同一个概念。

        数学定义:
            与 `perimeter()` 相同：

            .. math::

                C = 2\\pi r

        返回:
            float: 圆的周长值（与 perimeter() 结果相同）

        复杂度:
            O(1) - 常数时间操作

        使用示例::

            from planar_geometry import Circle, Point2D
            import math

            circle = Circle(Point2D(0, 0), 3.0)

            # 周长和圆周长相同
            assert abs(circle.get_circumference() - circle.perimeter()) < 1e-9

            # 都等于 6π
            assert abs(circle.get_circumference() - 6 * math.pi) < 1e-9
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
