# -*- coding: utf-8 -*-
"""
planar_geometry/utils/coordinate_ops.py

模块: 坐标系统转换
描述: 在笛卡尔坐标系和极坐标系之间转换，以及点集的几何关系计算
版本: 0.2.0
作者: wangheng <wangfaofao@gmail.com>

功能:
    - cartesian_to_polar: 笛卡尔坐标转极坐标
    - polar_to_cartesian: 极坐标转笛卡尔坐标
    - sort_points_by_angle: 按极角排序点集
    - are_collinear: 判断多点是否共线

依赖:
    - math: 数学模块
    - typing: 类型提示
    - point: Point2D 类
    - curve: Vector2D 类

设计原则:
    - SOLID 原则: 单一职责，每个函数只做一件事
    - 复用现有: 使用 Vector2D 的角度方法
    - 坐标约定: 笛卡尔 (x, y)，极坐标 (距离, 角度度数)
    - 稳定计算: 使用 atan2 处理所有象限

使用示例:
    from planar_geometry import Point2D
    from planar_geometry.utils import cartesian_to_polar, polar_to_cartesian

    # 笛卡尔到极坐标
    distance, angle = cartesian_to_polar(Point2D(1, 0), Point2D(0, 0))
    # distance=1.0, angle=0.0

    # 极坐标到笛卡尔
    point = polar_to_cartesian(1.0, 90.0, reference=Point2D(0, 0))
    # point ≈ Point2D(0, 1)
"""

import math
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import Vector2D


def cartesian_to_polar(
    point: "Point2D", reference: "Point2D" = None, tolerance: float = 1e-10
) -> Tuple[float, float]:
    r"""
    笛卡尔坐标转极坐标

    说明:
        - 返回 (距离, 角度度数)
        - 距离始终 >= 0
        - 角度范围 [0, 360) 度
        - 0° 表示正右方向，逆时针增大

    Args:
        point: Point2D - 目标点
        reference: Point2D - 参考点 (默认为原点)
        tolerance: float - 浮点容差 (默认 1e-10)

    返回:
        Tuple[float, float]: (距离, 角度度数)

    应用场景:
        - 极坐标系统表示
        - 旋转和角度计算
        - 雷达/方向数据

    算法原理:
        1. 计算向量 :math:`\vec{v} = \text{point} - \text{reference}`
        2. 距离 = :math:`|\vec{v}|`
        3. 角度 = :math:`\text{atan2}(\vec{v}_y, \vec{v}_x)` 转换为度数
    """
    from planar_geometry.curve import Vector2D
    from planar_geometry.point import Point2D as Point2DClass

    if reference is None:
        reference = Point2DClass(0, 0)

    # 构造向量
    v = Vector2D(point.x - reference.x, point.y - reference.y)

    # 计算距离
    distance = v.length()

    # 计算角度（若距离为0，返回角度0）
    if distance < tolerance:
        return (0.0, 0.0)

    # 使用 atan2 计算弧度，转换为度数
    angle_rad = math.atan2(v.y, v.x)
    angle_deg = math.degrees(angle_rad)

    # 范围化到 [0, 360)
    if angle_deg < 0:
        angle_deg += 360.0

    return (distance, angle_deg)


def polar_to_cartesian(distance: float, angle_deg: float, reference: "Point2D" = None) -> "Point2D":
    """
    极坐标转笛卡尔坐标

    说明:
        - 输入角度单位为度数
        - 0° 表示正右方向，逆时针增大
        - 返回相对于参考点的笛卡尔坐标

    Args:
        distance: float - 距离 (>= 0)
        angle_deg: float - 角度 (度数)
        reference: Point2D - 参考点 (默认为原点)

    返回:
        Point2D: 转换后的笛卡尔坐标

    应用场景:
        - 极坐标数据的笛卡尔化
        - 方向和距离的转换
        - 圆周运动轨迹

    算法原理:
        1. 将角度转换为弧度
        2. x = reference.x + distance * cos(angle)
        3. y = reference.y + distance * sin(angle)
    """
    from planar_geometry.point import Point2D as Point2DClass

    if reference is None:
        reference = Point2DClass(0, 0)

    # 角度转换为弧度
    angle_rad = math.radians(angle_deg)

    # 计算笛卡尔坐标
    x = reference.x + distance * math.cos(angle_rad)
    y = reference.y + distance * math.sin(angle_rad)

    return Point2DClass(x, y)


def sort_points_by_angle(
    points: List["Point2D"], reference: "Point2D" = None, clockwise: bool = False
) -> List["Point2D"]:
    """
    按极角排序点集

    说明:
        - 相对于参考点的极角排序
        - 默认逆时针排序 (从0°开始，按递增极角)
        - 若 clockwise=True，则顺时针排序
        - 相同极角的点按距离排序

    Args:
        points: List[Point2D] - 点集
        reference: Point2D - 参考点 (默认为原点)
        clockwise: bool - 是否顺时针排序 (默认逆时针)

    返回:
        List[Point2D]: 排序后的点集

    应用场景:
        - 凸包计算 (Graham Scan)
        - 点集按方向排序
        - 角度扫描算法

    算法原理:
        1. 计算每个点相对于参考点的极坐标 (距离, 角度)
        2. 按角度排序 (相同角度按距离排序)
        3. 若顺时针，则反向排序
    """
    from planar_geometry.point import Point2D as Point2DClass

    if reference is None:
        reference = Point2DClass(0, 0)

    if not points:
        return []

    # 计算每个点的 (极角, 距离, 原点) 三元组
    angle_distance_point = []
    for point in points:
        distance, angle = cartesian_to_polar(point, reference)
        angle_distance_point.append((angle, distance, point))

    # 按角度和距离排序
    angle_distance_point.sort(key=lambda x: (x[0], x[1]))

    # 若顺时针，则反向排序
    if clockwise:
        angle_distance_point.reverse()

    # 提取点集
    sorted_points = [item[2] for item in angle_distance_point]

    return sorted_points


def are_collinear(points: List["Point2D"], tolerance: float = 1e-10) -> bool:
    """
    判断多点是否共线

    说明:
        - 返回 True 如果所有点都在同一条直线上
        - 若点数 < 2，返回 True (定义为共线)
        - 使用叉积判断：对于任意三点，若叉积=0则共线

    Args:
        points: List[Point2D] - 点集
        tolerance: float - 浮点容差 (默认 1e-10)

    返回:
        bool: True 如果共线，False 否则

    应用场景:
        - 点集合法性检查
        - 退化多边形检测
        - 几何约束验证

    算法原理:
        1. 若点数 < 3，返回 True
        2. 用前两个点建立基准向量
        3. 对所有其他点，计算叉积
        4. 若所有叉积都接近0，则共线
    """
    from planar_geometry.curve import Vector2D

    if len(points) < 3:
        return True

    # 基准向量：第一点到第二点
    v_base = Vector2D(points[1].x - points[0].x, points[1].y - points[0].y)

    # 若前两点重合，继续找不同的点
    base_length = v_base.length()
    if base_length < tolerance:
        # 找第一个与第一点不同的点
        base_idx = 1
        while base_idx < len(points):
            v_base = Vector2D(points[base_idx].x - points[0].x, points[base_idx].y - points[0].y)
            if v_base.length() >= tolerance:
                break
            base_idx += 1

        # 若所有点都相同
        if v_base.length() < tolerance:
            return True

    # 检查所有其他点是否与基准向量共线
    for i in range(2, len(points)):
        v = Vector2D(points[i].x - points[0].x, points[i].y - points[0].y)

        # 计算叉积 v_base × v
        cross_product = v_base.cross(v)

        # 若叉积不为0，则不共线
        if abs(cross_product) > tolerance:
            return False

    return True
