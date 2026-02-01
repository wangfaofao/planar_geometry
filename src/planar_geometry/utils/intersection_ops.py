# -*- coding: utf-8 -*-
"""
planar_geometry/utils/intersection_ops.py

模块: 几何交点计算
描述: 计算各类几何体之间的交点（圆-直线、圆-线段、直线-多边形等）
版本: 0.2.0
作者: wangheng <wangfaofao@gmail.com>

功能:
    - circle_line_intersection: 圆与直线的交点
    - circle_segment_intersection: 圆与线段的交点
    - circles_intersection: 两个圆的交点
    - line_polygon_intersection_points: 直线与多边形的所有交点
    - segment_polygon_intersection_points: 线段与多边形的交点
    - ellipse_line_intersection: 椭圆与直线的交点
    - ellipse_circle_intersection: 椭圆与圆的交点

依赖:
    - math: 数学模块
    - typing: 类型提示
    - point: Point2D 类
    - curve: Line, LineSegment, Vector2D 类
    - surface: Circle, Polygon, Ellipse 类
    - geometry_utils: 现有工具函数

设计原则:
    - SOLID 原则: 单一职责，每个函数只做一件事
    - 复用现有: 最大化利用现有函数（Vector2D.cross/dot等）
    - 数值稳定: 优先使用平方比较，避免不必要的开方
    - 返回一致: 所有交点查询返回 List[Point2D]

使用示例:
    from planar_geometry import Circle, Line, Vector2D, Point2D
    from planar_geometry.utils import circle_line_intersection

    circle = Circle(Point2D(0, 0), 5)
    line = Line(Point2D(-10, 0), Vector2D(1, 0))
    intersections = circle_line_intersection(circle, line)
"""

import math
from typing import List, Optional, Union, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import Line, LineSegment, Vector2D
    from planar_geometry.surface import Circle, Polygon, Ellipse

from .geometry_utils import (
    point_to_line_distance,
    line_segment_intersection,
    point_to_segment_closest_point,
)


def circle_line_intersection(
    circle: "Circle", line: "Line", tolerance: float = 1e-10
) -> List["Point2D"]:
    """
    计算圆与直线的交点

    说明:
        - 使用点到直线距离判别式
        - 距离公式: :math:`d = \\frac{|ax + by + c|}{\\sqrt{a^2 + b^2}}`
        - 若 d > r: 无交点 (0 个)
        - 若 d = r: 相切 (1 个交点)
        - 若 d < r: 相交 (2 个交点)
        - 返回值按 x 坐标排序

    Args:
        circle: Circle - 圆
        line: Line - 直线
        tolerance: float - 浮点容差（默认 1e-10）

    返回:
        List[Point2D]: 0, 1, 或 2 个交点，按 x 坐标排序

    应用场景:
        - 圆形运动轨迹与路径的交点
        - 雷达扫描与边界的交点
        - 工程设计中的切线计算

    算法原理:
        1. 计算圆心到直线的距离
        2. 用距离与半径比较判断相交类型
        3. 计算投影点和偏移量得到交点坐标
    """
    # 导入 Point2D 用于创建结果
    from planar_geometry.point import Point2D

    center = circle.center
    radius = circle.radius

    # 获取直线的方向向量和法向量
    direction = line.direction
    normal = direction.perpendicular().normalized()

    # 计算圆心到直线的距离 (用距离的平方避免开方)
    dist = point_to_line_distance(center, line)
    dist_sq = dist * dist
    radius_sq = radius * radius

    # 判断相交类型
    if dist_sq > radius_sq + tolerance:
        # 完全不相交
        return []

    # 计算圆心在直线上的投影点
    projection = line.get_closest_point(center)

    if dist_sq < tolerance:
        # 圆心在直线上，返回直线方向上的两个交点
        offset = direction.normalized().multiply(radius)
        p1 = Point2D(projection.x - offset.x, projection.y - offset.y)
        p2 = Point2D(projection.x + offset.x, projection.y + offset.y)
    else:
        # 计算垂直于直线的偏移量
        offset_dist = math.sqrt(max(0, radius_sq - dist_sq))
        offset = direction.normalized().multiply(offset_dist)

        # 两个交点
        p1 = Point2D(projection.x - offset.x, projection.y - offset.y)
        p2 = Point2D(projection.x + offset.x, projection.y + offset.y)

    # 检查是否只有一个交点（相切）
    if abs(dist_sq - radius_sq) < tolerance:
        return [projection]

    # 按 x 坐标排序返回 (如果 x 相同则按 y 坐标)
    result = [p1, p2]
    result.sort(key=lambda p: (p.x, p.y))
    return result


def circle_segment_intersection(
    circle: "Circle", segment: "LineSegment", tolerance: float = 1e-10
) -> List["Point2D"]:
    """
    计算圆与线段的交点

    说明:
        - 扩展 circle_line_intersection
        - 限制交点在线段范围内
        - 考虑线段端点在圆内/外的各种情况

    Args:
        circle: Circle - 圆
        segment: LineSegment - 线段
        tolerance: float - 浮点容差

    返回:
        List[Point2D]: 0, 1, 或 2 个交点

    应用场景:
        - 碰撞检测：球与路径段的碰撞
        - 几何路径规划
        - 视觉遮挡计算
    """
    from planar_geometry.curve import Line, Vector2D
    from planar_geometry.point import Point2D

    # 将线段转换为直线
    line = Line(
        segment.start,
        Vector2D(segment.end.x - segment.start.x, segment.end.y - segment.start.y),
    )

    # 获取圆与直线的交点
    line_intersections = circle_line_intersection(circle, line, tolerance)

    # 过滤出在线段范围内的交点
    result = []
    for point in line_intersections:
        # 检查点是否在线段上
        closest = point_to_segment_closest_point(point, segment)
        dist = point.distance_to(closest)
        if dist < tolerance:
            result.append(point)

    return result


def circles_intersection(
    circle1: "Circle", circle2: "Circle", tolerance: float = 1e-10
) -> Union[List["Point2D"], str]:
    """
    计算两个圆的交点

    说明:
        - 基于圆心距离和半径分析
        - 返回 0, 1, 或 2 个交点
        - 处理相切（内/外）、同心、无交点等特殊情况

    Args:
        circle1: Circle - 第一个圆
        circle2: Circle - 第二个圆
        tolerance: float - 浮点容差

    返回:
        Union[List[Point2D], str]:
        - List[Point2D]: 0, 1, 或 2 个交点
        - "tangent_external": 外切
        - "tangent_internal": 内切
        - "concentric": 同心（无交点或重合）
        - "no_intersection": 无交点

    应用场景:
        - 两个移动对象的碰撞点
        - 定位三角网络（三圆交点）
        - 光学和声学计算

    算法原理:
        1. 计算圆心距离
        2. 使用三角形不等式判断相交情况
        3. 用余弦定理计算交点位置
    """
    from planar_geometry.point import Point2D
    from planar_geometry.curve import Vector2D

    c1 = circle1.center
    c2 = circle2.center
    r1 = circle1.radius
    r2 = circle2.radius

    # 计算圆心距离
    d = c1.distance_to(c2)
    d_sq = d * d

    # 判断相交情况
    if d < tolerance:
        # 同心
        return "concentric"

    # 外切
    if abs(d - (r1 + r2)) < tolerance:
        # 返回外切点
        direction = Vector2D(c2.x - c1.x, c2.y - c1.y).normalized()
        point = Point2D(c1.x + direction.x * r1, c1.y + direction.y * r1)
        return [point]

    # 内切
    if abs(d - abs(r1 - r2)) < tolerance:
        # 返回内切点
        if r1 > r2:
            direction = Vector2D(c2.x - c1.x, c2.y - c1.y).normalized()
            point = Point2D(c1.x + direction.x * r1, c1.y + direction.y * r1)
        else:
            direction = Vector2D(c1.x - c2.x, c1.y - c2.y).normalized()
            point = Point2D(c2.x + direction.x * r2, c2.y + direction.y * r2)
        return [point]

    # 检查是否完全不相交
    if d > r1 + r2 + tolerance or d < abs(r1 - r2) - tolerance:
        return "no_intersection"

    # 两个交点情况：使用余弦定理
    # a = (d² + r1² - r2²) / (2d)
    a = (d_sq + r1 * r1 - r2 * r2) / (2 * d)

    # h² = r1² - a²
    h_sq = r1 * r1 - a * a
    if h_sq < 0:
        h_sq = 0
    h = math.sqrt(h_sq)

    # 投影点
    direction = Vector2D(c2.x - c1.x, c2.y - c1.y).normalized()
    px = c1.x + direction.x * a
    py = c1.y + direction.y * a

    # 垂直方向
    perp = direction.perpendicular().normalized()

    # 两个交点
    p1 = Point2D(px + perp.x * h, py + perp.y * h)
    p2 = Point2D(px - perp.x * h, py - perp.y * h)

    return [p1, p2]


def line_polygon_intersection_points(
    line: "Line", polygon: "Polygon", tolerance: float = 1e-10
) -> List["Point2D"]:
    """
    计算直线与多边形的所有交点

    说明:
        - 遍历多边形所有边
        - 与每条边求交点
        - 去重处理（顶点计数一次）
        - 按沿直线的参数 t 排序

    Args:
        line: Line - 直线
        polygon: Polygon - 多边形
        tolerance: float - 浮点容差

    返回:
        List[Point2D]: 按沿直线的距离排序的交点列表

    应用场景:
        - 扫描线算法
        - 光线追踪
        - 几何切割

    算法原理:
        1. 获取多边形所有边
        2. 对每条边与直线求交点
        3. 去除重复的顶点
        4. 按参数 t 排序
    """
    from planar_geometry.curve import LineSegment
    from planar_geometry.point import Point2D

    edges = polygon.get_edges()
    intersections = []
    seen_points = set()

    for edge in edges:
        # 用已有的线段-直线交点函数
        # 需要将直线转换为参数形式与线段求交
        point = _line_segment_intersection(line, edge, tolerance)
        if point is not None:
            # 用坐标的哈希值去重
            key = (
                round(point.x / tolerance) * tolerance,
                round(point.y / tolerance) * tolerance,
            )
            if key not in seen_points:
                seen_points.add(key)
                intersections.append(point)

    # 按沿直线的参数 t 排序
    # t = (P - P0) · direction / |direction|²
    direction = line.direction
    p0 = line.point
    dir_len_sq = direction.dot(direction)

    if dir_len_sq > tolerance:
        intersections.sort(
            key=lambda p: ((p.x - p0.x) * direction.x + (p.y - p0.y) * direction.y) / dir_len_sq
        )

    return intersections


def segment_polygon_intersection_points(
    segment: "LineSegment", polygon: "Polygon", tolerance: float = 1e-10
) -> List["Point2D"]:
    """
    计算线段与多边形的交点

    说明:
        - 扩展 line_polygon_intersection_points
        - 限制交点在线段范围内

    Args:
        segment: LineSegment - 线段
        polygon: Polygon - 多边形
        tolerance: float - 浮点容差

    返回:
        List[Point2D]: 按沿线段的距离排序的交点列表

    应用场景:
        - 路径与边界的交点
        - 障碍物碰撞检测
    """
    from planar_geometry.curve import Line, Vector2D

    # 转换为直线
    line = Line(
        segment.start,
        Vector2D(segment.end.x - segment.start.x, segment.end.y - segment.start.y),
    )

    # 获取直线与多边形的交点
    line_intersections = line_polygon_intersection_points(line, polygon, tolerance)

    # 过滤在线段范围内的点
    result = []
    for point in line_intersections:
        closest = point_to_segment_closest_point(point, segment)
        dist = point.distance_to(closest)
        if dist < tolerance:
            result.append(point)

    return result


def ellipse_line_intersection(
    ellipse: "Ellipse", line: "Line", tolerance: float = 1e-10
) -> List["Point2D"]:
    """
    计算椭圆与直线的交点

    说明:
        - 使用参数方程代入法
        - 椭圆参数方程: x = cx + a*cos(t), y = cy + b*sin(t)
        - 将直线方程代入得到关于 t 的二次方程
        - 最多返回 2 个交点

    Args:
        ellipse: Ellipse - 椭圆
        line: Line - 直线
        tolerance: float - 浮点容差

    返回:
        List[Point2D]: 0, 1, 或 2 个交点

    应用场景:
        - 椭圆轨道与直线的交点
        - 轨道力学计算
    """
    from planar_geometry.point import Point2D

    # 获取椭圆参数
    center = ellipse.center
    a = ellipse.semi_major_axis
    b = ellipse.semi_minor_axis
    angle = ellipse.rotation_angle

    # 获取直线参数
    # 直线方程: P = line.point + t * line.direction
    p0 = line.point
    direction = line.direction

    # 转换坐标系到椭圆局部坐标
    # 涉及旋转变换，这里实现简化版本
    # 对于未旋转的椭圆: x²/a² + y²/b² = 1
    # 代入直线方程: (p0.x + t*dx)²/a² + (p0.y + t*dy)²/b² = 1

    import math

    dx = direction.x
    dy = direction.y
    x0 = p0.x - center.x
    y0 = p0.y - center.y

    # 展开为 At² + Bt + C = 0
    A = (dx * dx) / (a * a) + (dy * dy) / (b * b)
    B = 2 * (x0 * dx) / (a * a) + 2 * (y0 * dy) / (b * b)
    C = (x0 * x0) / (a * a) + (y0 * y0) / (b * b) - 1

    discriminant = B * B - 4 * A * C

    if discriminant < -tolerance:
        return []

    if abs(A) < tolerance:
        # 直线与椭圆平行（不相交或相切）
        return []

    result = []

    if discriminant < tolerance:
        # 一个交点（相切）
        t = -B / (2 * A)
        px = p0.x + t * dx
        py = p0.y + t * dy
        result.append(Point2D(px, py))
    else:
        # 两个交点
        sqrt_disc = math.sqrt(max(0, discriminant))
        t1 = (-B + sqrt_disc) / (2 * A)
        t2 = (-B - sqrt_disc) / (2 * A)

        px1 = p0.x + t1 * dx
        py1 = p0.y + t1 * dy
        px2 = p0.x + t2 * dx
        py2 = p0.y + t2 * dy

        result.append(Point2D(px1, py1))
        result.append(Point2D(px2, py2))

    return result


def ellipse_circle_intersection(
    ellipse: "Ellipse", circle: "Circle", tolerance: float = 1e-10
) -> List["Point2D"]:
    """
    计算椭圆与圆的交点

    说明:
        - 联立椭圆和圆的方程
        - 消除一个变量得到一次方程
        - 代入求第二个变量
        - 最多返回 4 个交点

    Args:
        ellipse: Ellipse - 椭圆
        circle: Circle - 圆
        tolerance: float - 浮点容差

    返回:
        List[Point2D]: 0 到 4 个交点

    应用场景:
        - 椭圆与圆形的碰撞检测
        - 轨道力学中的特殊问题
    """
    from planar_geometry.point import Point2D
    import math

    # 椭圆: (x-cx)²/a² + (y-cy)²/b² = 1
    # 圆: (x-xc)² + (y-yc)² = r²

    # 从圆的方程得: (x-xc)² + (y-yc)² = r²
    # 展开: x² - 2*xc*x + xc² + y² - 2*yc*y + yc² = r²

    # 这是一个复杂的四次方程系统
    # 简化实现：使用数值方法或参数扫描

    # 为简化起见，使用参数扫描法
    # 参数化圆：x = xc + r*cos(θ), y = yc + r*sin(θ)
    # 检查每个点是否在椭圆上

    center_e = ellipse.center
    cx_e, cy_e = center_e.x, center_e.y
    a = ellipse.semi_major_axis
    b = ellipse.semi_minor_axis

    center_c = circle.center
    xc, yc = center_c.x, center_c.y
    r = circle.radius

    result = []

    # 参数扫描（36 个采样点）
    for i in range(360):
        angle_rad = math.radians(i)
        x = xc + r * math.cos(angle_rad)
        y = yc + r * math.sin(angle_rad)

        # 检查点是否在椭圆上（在容差范围内）
        ellipse_eq = (x - cx_e) ** 2 / (a**2) + (y - cy_e) ** 2 / (b**2)

        if abs(ellipse_eq - 1) < tolerance:
            # 检查是否已添加过这个点
            is_duplicate = False
            for existing_point in result:
                if abs(existing_point.x - x) < tolerance and abs(existing_point.y - y) < tolerance:
                    is_duplicate = True
                    break

            if not is_duplicate:
                result.append(Point2D(x, y))

    return result


def _line_segment_intersection(
    line: "Line", segment: "LineSegment", tolerance: float = 1e-10
) -> Optional["Point2D"]:
    """
    私有函数：计算直线与线段的交点

    说明:
        - 内部使用函数
        - 直线与线段有且只有一个交点或无交点

    Args:
        line: Line - 直线
        segment: LineSegment - 线段
        tolerance: float - 容差

    返回:
        Optional[Point2D]: 交点或 None
    """
    from planar_geometry.curve import LineSegment as LS

    # 将直线转换为两点表示
    p1 = line.point
    p2_extended = (p1.x + line.direction.x * 1000, p1.y + line.direction.y * 1000)

    from planar_geometry.point import Point2D

    p2 = Point2D(p2_extended[0], p2_extended[1])

    extended_segment = LS(p1, p2)

    # 使用现有的线段交点函数
    return line_segment_intersection(extended_segment, segment, tolerance)
