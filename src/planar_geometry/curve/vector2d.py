# -*- coding: utf-8 -*-
"""
planar_geometry/curve/vector2_d.py

模块: Vector2D
描述: Vector2D类的实现
版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

依赖:
    - planar_geometry.abstracts: 抽象基类
    - planar_geometry.point: Point2D类

使用示例:
    from planar_geometry.curve import Vector2D
"""

import math
from typing import TYPE_CHECKING, Optional

from planar_geometry.abstracts import Curve

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve.vector2d import Vector2D


class Vector2D(Curve):
    """
    二维欧几里得向量

    数学定义:
        向量是具有方向和大小的几何对象，表示为有序对 :math:`\\vec{v} = (x, y) \\in \\mathbb{R}^2`

    几何性质:
        - **模长**: :math:`|\\vec{v}| = \\sqrt{x^2 + y^2}`
        - **方向**: 由 :math:`\\theta = \\arctan2(y, x)` 确定
        - **归一化**: :math:`\\hat{\\vec{v}} = \\frac{\\vec{v}}{|\\vec{v}|}`

    属性:
        x (float): 向量的x分量
        y (float): 向量的y分量

    使用示例::

        # 创建向量
        v1 = Vector2D(3, 4)
        v2 = Vector2D(1, 2)

        # 基本运算
        dot_product = v1.dot(v2)        # 点积: 11
        cross_product = v1.cross(v2)    # 叉积: 2
        normalized = v1.normalized()    # 归一化: (0.6, 0.8)

        # 向量运算
        v_sum = v1.add(v2)              # (4, 6)
        v_diff = v1.subtract(v2)        # (2, 2)
        v_scaled = v1.multiply(2)       # (6, 8)
    """

    def __init__(self, x: float, y: float) -> None:
        """
        初始化二维向量

        Args:
            x: float - x分量
            y: float - y分量
        """
        self.x = x
        self.y = y

    def length(self) -> float:
        """
        计算向量的欧几里得范数（模长）

        数学定义:
            向量 :math:`\\vec{v} = (x, y)` 的模长为：

            .. math::

                |\\vec{v}| = \\sqrt{x^2 + y^2}

        返回:
            float: 向量的模长，始终非负

        复杂度:
            O(1) - 常数时间操作（包含一次平方根计算）

        使用示例::

            v = Vector2D(3, 4)
            length = v.length()  # 返回 5.0
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def length_squared(self) -> float:
        """
        计算向量模长的平方

        数学定义:
            .. math::

                |\\vec{v}|^2 = x^2 + y^2

        说明:
            避免平方根运算，性能优于 :meth:`length` 方法
            常用于距离比较场景（如判断距离大小时，可直接比较平方值）

        返回:
            float: 模长的平方值（≥0）

        复杂度:
            O(1) - 避免了平方根计算

        使用示例::

            v = Vector2D(3, 4)
            len_sq = v.length_squared()  # 返回 25.0
            # 比 v.length() 更高效

            # 距离比较示例
            if v1.length_squared() < v2.length_squared():
                print("v1 更短")  # 无需计算平方根
        """
        return self.x * self.x + self.y * self.y

    def angle(self) -> float:
        """
        计算向量的极角（度）

        数学定义:
            向量与x轴正向的夹角，通过反正切函数计算：

            .. math::

                \\theta = \\arctan2(y, x) \\cdot \\frac{180}{\\pi}

        说明:
            - 使用 atan2 函数确保正确处理所有象限
            - 返回值范围：[0, 360)
            - 按标准数学约定：0° 指向正x方向，逆时针为正

        返回:
            float: 极角，单位为度，范围 [0, 360)

        复杂度:
            O(1)

        使用示例::

            v1 = Vector2D(1, 0)     # 返回 0.0 度
            v2 = Vector2D(0, 1)     # 返回 90.0 度
            v3 = Vector2D(-1, 0)    # 返回 180.0 度
            v4 = Vector2D(0, -1)    # 返回 270.0 度
        """
        angle_rad = math.atan2(self.y, self.x)
        return math.degrees(angle_rad) % 360.0

    def angle_rad(self) -> float:
        """
        计算向量的极角（弧度）

        数学定义:
            向量与x轴正向的夹角（弧度制）：

            .. math::

                \\theta = \\arctan2(y, x)

        说明:
            - 使用标准的 atan2 函数
            - 返回值范围：[0, 2π)
            - 用于数值计算和三角函数操作时效率更高

        返回:
            float: 极角，单位为弧度，范围 [0, 2π)

        复杂度:
            O(1)

        使用示例::

            import math
            v = Vector2D(1, 1)
            angle = v.angle_rad()  # 返回 π/4 ≈ 0.785 弧度
            assert abs(angle - math.pi / 4) < 1e-9
        """
        return math.atan2(self.y, self.x) % (2 * math.pi)

    def normalized(self) -> "Vector2D":
        """
        返回单位向量（归一化）

        数学定义:
            给定向量 :math:`\\vec{v}` 的单位向量为：

            .. math::

                \\hat{\\vec{v}} = \\frac{\\vec{v}}{|\\vec{v}|} = \\left( \\frac{x}{|\\vec{v}|}, \\frac{y}{|\\vec{v}|} \\right)

        说明:
            - 零向量没有良定义的方向，返回零向量 (0, 0)
            - 归一化向量的模长恒为1
            - 常用于方向计算和光线追踪

        返回:
            Vector2D: 单位向量，模长为1；若输入为零向量，返回 (0, 0)

        复杂度:
            O(1)

        使用示例::

            v = Vector2D(3, 4)
            u = v.normalized()  # 返回 (0.6, 0.8)
            assert abs(u.length() - 1.0) < 1e-9

            # 零向量处理
            zero = Vector2D(0, 0)
            zero_normalized = zero.normalized()  # 返回 (0, 0)
        """
        length = self.length()
        if length > 0:
            return Vector2D(self.x / length, self.y / length)
        return Vector2D(0, 0)

    def dot(self, other: "Vector2D") -> float:
        """
        计算两向量的点积（数量积）

        数学定义:
            设 :math:`\\vec{u} = (x_1, y_1)` 和 :math:`\\vec{v} = (x_2, y_2)`，则点积为：

            .. math::

                \\vec{u} \\cdot \\vec{v} = x_1 x_2 + y_1 y_2 = |\\vec{u}| |\\vec{v}| \\cos(\\theta)

            其中 :math:`\\theta` 是两向量的夹角。

        几何意义:
            - 若点积 > 0：两向量夹角为锐角 (:math:`\\theta < 90°`)
            - 若点积 = 0：两向量正交 (:math:`\\theta = 90°`)
            - 若点积 < 0：两向量夹角为钝角 (:math:`\\theta > 90°`)

        参数:
            other (Vector2D): 另一向量

        返回:
            float: 点积结果

        复杂度:
            O(1)

        应用场景:
            - 计算向量间的夹角
            - 投影长度计算
            - 光照计算（Lambert's law）
            - 射线与平面的交点判断

        使用示例::

            u = Vector2D(3, 4)
            v = Vector2D(1, 2)
            dot_result = u.dot(v)  # 返回 3*1 + 4*2 = 11

            # 正交性检验
            a = Vector2D(1, 0)
            b = Vector2D(0, 1)
            assert a.dot(b) == 0  # 正交向量

            # 夹角判断
            c = Vector2D(1, 1)
            if u.dot(c) > 0:
                print("夹角为锐角")
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: "Vector2D") -> float:
        """
        计算两向量的叉积（外积，在2D中为标量）

        数学定义:
            设 :math:`\\vec{u} = (x_1, y_1)` 和 :math:`\\vec{v} = (x_2, y_2)`，则2D叉积为：

            .. math::

                \\vec{u} \\times \\vec{v} = x_1 y_2 - y_1 x_2

            这是三维叉积在z分量上的结果：:math:`|\\vec{u}| |\\vec{v}| \\sin(\\theta)`

        几何意义:
            - 结果的绝对值等于两向量构成的平行四边形面积
            - 若结果 > 0：:math:`\\vec{v}` 在 :math:`\\vec{u}` 的逆时针方向 (:math:`\\theta > 0`)
            - 若结果 = 0：两向量平行或反向平行
            - 若结果 < 0：:math:`\\vec{v}` 在 :math:`\\vec{u}` 的顺时针方向 (:math:`\\theta < 0`)

        参数:
            other (Vector2D): 另一向量

        返回:
            float: 叉积结果（标量）

        复杂度:
            O(1)

        应用场景:
            - 判断点在线段的左/右侧
            - 凸包算法（Graham Scan）
            - 计算多边形的有向面积
            - 判断线段是否相交
            - 求解点到直线的有向距离

        使用示例::

            u = Vector2D(3, 4)
            v = Vector2D(1, 2)
            cross_result = u.cross(v)  # 返回 3*2 - 4*1 = 2

            # 方向判断
            a = Vector2D(1, 0)
            b = Vector2D(0, 1)
            assert a.cross(b) > 0  # b在a的逆时针方向

            # 平行性检验
            c = Vector2D(2, 0)
            assert a.cross(c) == 0  # 平行向量的叉积为0

            # 多边形面积计算
            # 三角形 (0,0), (3,0), (0,4) 的面积 = |叉积|/2 = 6
            edge1 = Vector2D(3, 0)
            edge2 = Vector2D(0, 4)
            area = abs(edge1.cross(edge2)) / 2  # 6.0
        """
        return self.x * other.y - self.y * other.x

    def perpendicular(self) -> "Vector2D":
        """
        获取垂直向量（逆时针旋转90度）

        数学定义:
            对于向量 :math:`\\vec{v} = (x, y)`，其逆时针垂直向量为：

            .. math::

                \\vec{v}_{\\perp} = (-y, x)

        说明:
            - 垂直向量与原向量的点积为0：:math:`\\vec{v} \\cdot \\vec{v}_{\\perp} = 0`
            - 垂直向量的模长等于原向量：:math:`|\\vec{v}_{\\perp}| = |\\vec{v}|`
            - 等价于旋转90度：相当于 :math:`\\text{rotated}(90°)`

        返回:
            Vector2D: 垂直向量

        复杂度:
            O(1)

        使用示例::

            v = Vector2D(3, 4)
            perp = v.perpendicular()  # 返回 (-4, 3)

            # 验证正交性
            assert v.dot(perp) == 0
            assert abs(v.length() - perp.length()) < 1e-9

            # 单位向量的垂直向量
            u = Vector2D(1, 0)
            u_perp = u.perpendicular()  # 返回 (0, 1)
        """
        return Vector2D(-self.y, self.x)

    def rotated(self, angle_deg: float) -> "Vector2D":
        """
        将向量旋转指定角度

        数学定义:
            使用2D旋转矩阵，将向量 :math:`\\vec{v} = (x, y)` 旋转 :math:`\\theta` 角度：

            .. math::

                \\begin{pmatrix} x' \\\\ y' \\end{pmatrix} = 
                \\begin{pmatrix} \\cos(\\theta) & -\\sin(\\theta) \\\\ 
                \\sin(\\theta) & \\cos(\\theta) \\end{pmatrix}
                \\begin{pmatrix} x \\\\ y \\end{pmatrix}

            因此：

            .. math::

                x' = x \\cos(\\theta) - y \\sin(\\theta)
                
                y' = x \\sin(\\theta) + y \\cos(\\theta)

        性质:
            - 旋转不改变向量的模长：:math:`|\\vec{v}'| = |\\vec{v}|`
            - 旋转是可组合的：多次旋转等价于一次旋转
            - 旋转逆变换：旋转 -θ 角度

        参数:
            angle_deg (float): 旋转角度，单位为度
                - 正值：逆时针旋转
                - 负值：顺时针旋转

        返回:
            Vector2D: 旋转后的向量

        复杂度:
            O(1)

        应用场景:
            - 几何变换（缩放、旋转、平移）
            - 物体转向和朝向计算
            - 2D图形旋转

        使用示例::

            v = Vector2D(1, 0)
            
            # 逆时针旋转90度
            v90 = v.rotated(90)  # 返回 (0, 1)
            
            # 顺时针旋转45度
            v45 = v.rotated(-45)
            
            # 旋转360度应得到原向量
            v360 = v.rotated(360)
            assert v360.equals(v)
            
            # 模长保持不变
            original_len = v.length()
            rotated_len = v.rotated(30).length()
            assert abs(original_len - rotated_len) < 1e-9
        """
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Vector2D(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a)

    def projection(self, other: "Vector2D") -> "Vector2D":
        """
        计算向量在另一向量上的投影

        数学定义:
            设 :math:`\\vec{u}` 和 :math:`\\vec{v}` 为两个向量，:math:`\\vec{u}` 在 :math:`\\vec{v}` 上的投影为：

            .. math::

                \\text{proj}_{\\vec{v}}(\\vec{u}) = \\left( \\frac{\\vec{u} \\cdot \\vec{v}}{|\\vec{v}|^2} \\right) \\vec{v}

            或等价地：

            .. math::

                \\text{proj}_{\\vec{v}}(\\vec{u}) = (|\\vec{u}| \\cos(\\theta)) \\hat{\\vec{v}}

            其中 :math:`\\theta` 是两向量的夹角，:math:`\\hat{\\vec{v}}` 是单位向量。

        几何意义:
            - 投影是 :math:`\\vec{u}` 在 :math:`\\vec{v}` 方向上的分解
            - 投影向量方向与 :math:`\\vec{v}` 相同
            - 投影的模长 = :math:`|\\vec{u}| \\cos(\\theta)`

        参数:
            other (Vector2D): 目标向量（投影的方向）

        返回:
            Vector2D: 投影向量；若目标向量为零向量，返回零向量 (0, 0)

        复杂度:
            O(1)

        应用场景:
            - 力的分解（物理学）
            - 光线与表面的相互作用
            - 运动学中的速度分解
            - 在某方向上的有效分量计算

        使用示例::

            u = Vector2D(3, 4)
            v = Vector2D(1, 0)  # x轴方向

            proj = u.projection(v)  # 返回 (3, 0)
            assert proj.x == 3

            # 在对角线方向上的投影
            v_diag = Vector2D(1, 1)
            proj_diag = u.projection(v_diag)
            # 投影长度 = (3*1 + 4*1) / sqrt(2) = 7/sqrt(2)

            # 零向量投影
            zero = Vector2D(0, 0)
            proj_zero = u.projection(zero)  # 返回 (0, 0)
        """
        dot = self.dot(other)
        other_len_sq = other.length_squared()
        if other_len_sq == 0:
            return Vector2D(0, 0)
        scalar = dot / other_len_sq
        return Vector2D(other.x * scalar, other.y * scalar)

    def component(self, direction: "Vector2D") -> float:
        """
        获取在指定方向上的分量（标量投影）

        Args:
            direction: Vector2D - 方向向量

        返回:
            float: 分量值（标量）
        """
        dir_norm = direction.normalized()
        return self.dot(dir_norm)

    def add(self, other: "Vector2D") -> "Vector2D":
        """
        向量加法

        Args:
            other: Vector2D - 另一向量

        返回:
            Vector2D: 结果向量
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def subtract(self, other: "Vector2D") -> "Vector2D":
        """
        向量减法

        Args:
            other: Vector2D - 另一向量

        返回:
            Vector2D: 结果向量
        """
        return Vector2D(self.x - other.x, self.y - other.y)

    def multiply(self, scalar: float) -> "Vector2D":
        """
        标量乘法

        Args:
            scalar: float - 标量

        返回:
            Vector2D: 结果向量
        """
        return Vector2D(self.x * scalar, self.y * scalar)

    def divide(self, scalar: float) -> "Vector2D":
        """
        标量除法

        Args:
            scalar: float - 标量

        返回:
            Vector2D: 结果向量

        异常:
            ZeroDivisionError: 标量为0
        """
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Vector2D(self.x / scalar, self.y / scalar)

    def negate(self) -> "Vector2D":
        """
        取负

        返回:
            Vector2D: 取负后的向量
        """
        return Vector2D(-self.x, -self.y)

    def is_zero(self, tolerance: float = 1e-9) -> bool:
        """
        判断是否为零向量

        Args:
            tolerance: float - 容差

        返回:
            bool: 是否为零向量
        """
        return abs(self.x) < tolerance and abs(self.y) < tolerance

    def equals(self, other: "Vector2D", tolerance: float = 1e-9) -> bool:
        """
        判断与另一向量是否相等

        Args:
            other: Vector2D - 比较对象
            tolerance: float - 容差

        返回:
            bool: 是否相等
        """
        return abs(self.x - other.x) < tolerance and abs(self.y - other.y) < tolerance

    def to_tuple(self) -> tuple:
        """
        转换为元组

        返回:
            tuple: (x, y)
        """
        return (self.x, self.y)

    @staticmethod
    def from_tuple(data: tuple) -> "Vector2D":
        """
        从元组创建向量

        Args:
            data: tuple - (x, y) 元组

        返回:
            Vector2D: 创建的向量
        """
        return Vector2D(data[0], data[1])

    @staticmethod
    def zero() -> "Vector2D":
        """
        创建零向量

        返回:
            Vector2D: 零向量 (0, 0)
        """
        return Vector2D(0, 0)

    @staticmethod
    def unit_x() -> "Vector2D":
        """
        创建X轴单位向量

        返回:
            Vector2D: (1, 0)
        """
        return Vector2D(1, 0)

    @staticmethod
    def unit_y() -> "Vector2D":
        """
        创建Y轴单位向量

        返回:
            Vector2D: (0, 1)
        """
        return Vector2D(0, 1)

    def __add__(self, other: "Vector2D") -> "Vector2D":
        """
        向量加法（中缀运算符）

        数学定义:
            :math:`(x_1, y_1) + (x_2, y_2) = (x_1 + x_2, y_1 + y_2)`

        使用示例::

            v1 = Vector2D(1, 2)
            v2 = Vector2D(3, 4)
            result = v1 + v2  # Vector2D(4, 6)
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        """
        向量与标量的乘法（右乘）

        数学定义:
            :math:`k \\cdot \\vec{v} = (k \\cdot x, k \\cdot y)`

        说明:
            - 标量乘法改变向量的模长，但不改变方向（k>0时）
            - 若 k=0，结果为零向量
            - 若 k<0，方向反向

        使用示例::

            v = Vector2D(2, 3)
            result = v * 2  # Vector2D(4, 6)
        """
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2D":
        """
        向量与标量的乘法（左乘）

        数学定义:
            :math:`\\vec{v} \\cdot k = (x \\cdot k, y \\cdot k)`

        说明:
            - 与右乘结果相同（乘法交换律）
            - 用于 `scalar * vector` 的表达式

        使用示例::

            v = Vector2D(2, 3)
            result = 2 * v  # Vector2D(4, 6)
            # 与 v * 2 结果相同
        """
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> "Vector2D":
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector2D(self.x / scalar, self.y / scalar)

    def __eq__(self, other: object) -> bool:
        """
        向量相等性判断

        说明:
            - 使用浮点容差比较（`math.isclose`）
            - 避免直接相等比较导致的浮点精度问题
            - 默认相对容差为 1e-9

        参数:
            other: 比较对象（应为 Vector2D 类型）

        返回:
            bool: 两向量是否相等（在容差范围内）

        使用示例::

            v1 = Vector2D(1.0, 2.0)
            v2 = Vector2D(1.0, 2.0)
            v3 = Vector2D(1.000000001, 2.0)

            assert v1 == v2  # True
            assert v1 == v3  # True（容差内）
            assert v1 != Vector2D(1.1, 2.0)  # False
        """
        if not isinstance(other, Vector2D):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __hash__(self) -> int:
        return hash((round(self.x, 9), round(self.y, 9)))

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


from planar_geometry.point import Point2D
