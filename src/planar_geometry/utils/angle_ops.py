# -*- coding: utf-8 -*-
"""
planar_geometry/utils/angle_ops.py

模块: 几何角度计算
描述: 计算点、向量和几何体之间的角度关系
版本: 0.2.0
作者: wangheng <wangfaofao@gmail.com>

功能:
    - angle_between_three_points: 三点确定的有向角 (中心点处的角度)
    - polygon_vertex_angles: 多边形各顶点处的内角
    - point_polar_angle: 点相对于参考点的极角 (0-360度)

依赖:
    - math: 数学模块
    - typing: 类型提示
    - point: Point2D 类
    - curve: Vector2D 类
    - surface: Polygon 类

设计原则:
    - SOLID 原则: 单一职责，每个函数只做一件事
    - 复用现有: 最大化利用 Vector2D 的角度方法
    - 角度约定: 所有返回角度单位均为度数 (0-360)
    - 稳定计算: 使用反正切函数处理边界情况

使用示例:
    from planar_geometry import Point2D, Polygon
    from planar_geometry.utils import angle_between_three_points, polygon_vertex_angles

    p1 = Point2D(0, 0)
    p2 = Point2D(1, 0)
    p3 = Point2D(1, 1)

    angle = angle_between_three_points(p1, p2, p3)  # 90度

    poly = Polygon([Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(0, 2)])
    angles = polygon_vertex_angles(poly)  # [90, 90, 90, 90]
"""

import math
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import Vector2D
    from planar_geometry.surface import Polygon


def angle_between_three_points(
    p1: "Point2D", p2: "Point2D", p3: "Point2D", tolerance: float = 1e-10
) -> float:
    """
    计算三点确定的有向角 (中心点 p2 处的角度)

    说明:
        - 计算从 p2->p1 到 p2->p3 的夹角（逆时针正方向）
        - 返回值范围 [0, 360) 度
        - 逆时针方向为正
        - 若 p1=p2 或 p3=p2，返回 0
        - 注意：这计算的是外角（从p1-p2-p3逆时针扫过的角度）
        - 对于多边形内角，请使用结果的补角 (360 - angle) 或使用 polygon_vertex_angles()

    Args:
        p1: Point2D - 第一个点
        p2: Point2D - 中心点 (角度顶点)
        p3: Point2D - 第三个点
        tolerance: float - 浮点容差 (默认 1e-10)

    返回:
        float: 夹角大小，单位为度数 [0, 360)

    应用场景:
        - 三点构成的角度计算 (如射线夹角)
        - 有向角度计算（逆时针为正）
        - 导航和方向判断

    算法原理:
        1. 计算两个向量 v1 = p1 - p2, v2 = p3 - p2
        2. 使用 atan2 计算两向量的极角
        3. 计算角度差，范围化到 [0, 360)
    """
    from planar_geometry.curve import Vector2D

    # 构造向量
    v1 = Vector2D(p1.x - p2.x, p1.y - p2.y)
    v2 = Vector2D(p3.x - p2.x, p3.y - p2.y)

    # 检查退化情况
    if v1.length() < tolerance or v2.length() < tolerance:
        return 0.0

    # 获取两向量的极角
    angle1 = v1.angle_rad()  # 弧度
    angle2 = v2.angle_rad()  # 弧度

    # 计算夹角 (逆时针为正)
    angle_diff = math.degrees(angle2 - angle1)

    # 范围化到 [0, 360)
    while angle_diff < 0:
        angle_diff += 360.0
    while angle_diff >= 360.0:
        angle_diff -= 360.0

    return angle_diff


def polygon_vertex_angles(polygon: "Polygon", tolerance: float = 1e-10) -> List[float]:
    """
    计算多边形各顶点处的内角

    说明:
        - 对每个顶点计算其前一个、当前、后一个顶点确定的内角
        - 返回列表顺序与顶点顺序相同
        - 对于凸多边形（顶点逆时针排列），所有内角之和应接近 (n-2)*180
        - 对于凹多边形，某些"内角"可能大于180度

    Args:
        polygon: Polygon - 多边形
        tolerance: float - 浮点容差 (默认 1e-10)

    返回:
        List[float]: 各顶点内角，单位为度数

    应用场景:
        - 多边形凹凸性分析
        - 多边形角度分布统计
        - 形状识别 (如检测正多边形)

    算法原理:
        1. 遍历每个顶点
        2. 获取前一个顶点、当前顶点、后一个顶点
        3. 计算有向角，然后取其补角得到内角
        4. 内角 = 360 - 有向角
    """
    vertices = polygon.vertices
    n = len(vertices)

    if n < 3:
        return []

    angles = []
    for i in range(n):
        prev_idx = (i - 1) % n
        next_idx = (i + 1) % n

        # 计算从 prev_idx 经过 i 到 next_idx 的有向角
        # 由于多边形顶点通常逆时针排列，有向角是外角
        # 内角 = 360 - 有向角
        exterior_angle = angle_between_three_points(
            vertices[prev_idx], vertices[i], vertices[next_idx], tolerance
        )

        # 内角是补角
        interior_angle = 360.0 - exterior_angle

        # 范围化到 [0, 360)
        while interior_angle >= 360.0:
            interior_angle -= 360.0

        angles.append(interior_angle)

    return angles


def point_polar_angle(
    point: "Point2D", reference: "Point2D" = None, tolerance: float = 1e-10
) -> float:
    """
    计算点相对于参考点的极角

    说明:
        - 计算 point - reference 向量的极角
        - 返回值范围 [0, 360) 度
        - 0° 表示正右方向，逆时针增大
        - 若 point = reference，返回 0

    Args:
        point: Point2D - 目标点
        reference: Point2D - 参考点 (默认为原点)
        tolerance: float - 浮点容差 (默认 1e-10)

    返回:
        float: 极角，单位为度数 [0, 360)

    应用场景:
        - 极坐标系统中的角度表示
        - 点相对于中心的方向判断
        - 旋转和变换计算

    算法原理:
        1. 构造向量 v = point - reference
        2. 使用 atan2 计算极角
        3. 范围化到 [0, 360)
    """
    from planar_geometry.curve import Vector2D
    from planar_geometry.point import Point2D as Point2DClass

    if reference is None:
        reference = Point2DClass(0, 0)

    # 构造向量
    v = Vector2D(point.x - reference.x, point.y - reference.y)

    # 若向量为零向量
    if v.length() < tolerance:
        return 0.0

    # 获取极角（弧度）并转换为度数
    angle_rad = v.angle_rad()
    angle_deg = math.degrees(angle_rad)

    # 范围化到 [0, 360)
    while angle_deg < 0:
        angle_deg += 360.0
    while angle_deg >= 360.0:
        angle_deg -= 360.0

    return angle_deg
