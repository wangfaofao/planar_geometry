# -*- coding: utf-8 -*-
"""
planar_geometry/utils/query_ops.py

模块: 几何关系查询
描述: 几何体之间的关系判断和高级查询
版本: 0.2.0
作者: wangheng <wangfaofao@gmail.com>

功能:
    - point_side_of_segment: 点相对于线段的方向（左/右/在线上）
    - circle_polygon_intersect: 圆与多边形的精确相交检测
    - minimum_distance: 两个几何体间的最小距离
    - within_distance: 检测两个几何体是否在指定距离内

依赖:
    - typing: 类型提示
    - projection_ops: 投影查询

使用示例:
    from planar_geometry import Point2D, LineSegment
    from planar_geometry.utils import point_side_of_segment

    point = Point2D(1, 1)
    segment = LineSegment(Point2D(0, 0), Point2D(2, 0))
    side = point_side_of_segment(point, segment)
    print(side)  # 输出: 1 (左侧)
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import LineSegment
    from planar_geometry.surface import Circle, Polygon

from .projection_ops import nearest_point_on_geometry


def point_side_of_segment(
    point: "Point2D", segment: "LineSegment", tolerance: float = 1e-10
) -> int:
    """
    判断点相对于线段的方向（左/右/在线上）

    说明:
        - 使用叉积判断
        - 返回值：1 表示左侧，-1 表示右侧，0 表示在线上
        - 方向定义：从线段起点指向终点为正方向

    Args:
        point: Point2D - 查询点
        segment: LineSegment - 线段
        tolerance: float - 浮点容差

    返回:
        int: 1 (左侧), -1 (右侧), 0 (在线上)

    应用场景:
        - 多边形内点检测的基础
        - 碰撞检测中的方向判断
        - 凸性检测
        - Graham 扫描算法

    算法原理:
        使用向量叉积判断方向：
        v1 = segment.end - segment.start
        v2 = point - segment.start
        cross = v1.cross(v2)
        - cross > 0: 点在左侧
        - cross < 0: 点在右侧
        - cross = 0: 点在直线上

    示例:
        >>> from planar_geometry import Point2D, LineSegment
        >>> segment = LineSegment(Point2D(0, 0), Point2D(2, 0))
        >>> left_point = Point2D(1, 1)
        >>> right_point = Point2D(1, -1)
        >>> on_line_point = Point2D(1, 0)
        >>> print(point_side_of_segment(left_point, segment))  # 1
        >>> print(point_side_of_segment(right_point, segment))  # -1
        >>> print(point_side_of_segment(on_line_point, segment))  # 0
    """
    # 获取向量
    v1_x = segment.end.x - segment.start.x
    v1_y = segment.end.y - segment.start.y

    v2_x = point.x - segment.start.x
    v2_y = point.y - segment.start.y

    # 计算叉积 (2D 标量形式)
    cross = v1_x * v2_y - v1_y * v2_x

    if abs(cross) < tolerance:
        return 0  # 在线上
    elif cross > 0:
        return 1  # 左侧
    else:
        return -1  # 右侧


def circle_polygon_intersect(
    circle: "Circle", polygon: "Polygon", tolerance: float = 1e-10
) -> bool:
    """
    检测圆与多边形是否精确相交

    说明:
        - 比简单的"任一点在内"更精确
        - 考虑圆与多边形边界的相交
        - 返回 True 表示圆与多边形有重叠

    Args:
        circle: Circle - 圆
        polygon: Polygon - 多边形
        tolerance: float - 浮点容差

    返回:
        bool: True 表示相交，False 表示不相交

    应用场景:
        - 精确碰撞检测
        - 覆盖面积计算
        - 可视化区域检测

    算法原理:
        1. 检查圆心是否在多边形内
        2. 如果在内，必然相交
        3. 如果在外，检查圆与多边形任一边的最小距离
        4. 如果最小距离 <= 半径，则相交
    """
    # 检查圆心是否在多边形内
    if polygon.contains_point(circle.center):
        return True

    # 检查圆与多边形各边的距离
    for edge in polygon.get_edges():
        closest, distance = nearest_point_on_geometry(circle.center, edge, tolerance)
        if distance <= circle.radius + tolerance:
            return True

    return False


def minimum_distance(geom1, geom2, tolerance: float = 1e-10) -> float:
    """
    计算两个几何体间的最小距离

    说明:
        - 统一接口支持所有几何类型组合
        - 对于重叠的几何体返回 0

    Args:
        geom1: 第一个几何对象
        geom2: 第二个几何对象
        tolerance: float - 浮点容差

    返回:
        float: 两个几何体间的最小距离

    应用场景:
        - 碰撞检测
        - 接近度分析
        - 物体对齐

    示例:
        >>> from planar_geometry import Point2D, Circle
        >>> point = Point2D(10, 0)
        >>> circle = Circle(Point2D(0, 0), 5)
        >>> dist = minimum_distance(point, circle)
        >>> print(dist)  # 5.0
    """
    # 使用投影查询函数
    nearest_p1, dist1 = nearest_point_on_geometry(geom1, geom2, tolerance)
    nearest_p2, dist2 = nearest_point_on_geometry(geom2, geom1, tolerance)

    # 返回最小距离
    return min(dist1, dist2)


def within_distance(geom1, geom2, distance: float, tolerance: float = 1e-10) -> bool:
    """
    检测两个几何体是否在指定距离内

    说明:
        - 快速的相交/接近检测
        - 比精确相交检测快（提前退出）
        - 用于广泛排除肯定不碰撞的对象

    Args:
        geom1: 第一个几何对象
        geom2: 第二个几何对象
        distance: float - 距离阈值
        tolerance: float - 浮点容差

    返回:
        bool: True 表示两个几何体距离 <= distance

    应用场景:
        - 快速碰撞检测（AABB 之后的二级检测）
        - 范围查询
        - 性能优化

    示例:
        >>> from planar_geometry import Point2D, Circle
        >>> point = Point2D(7, 0)
        >>> circle = Circle(Point2D(0, 0), 5)
        >>> print(within_distance(point, circle, 3))  # True (距离 2 < 3)
        >>> print(within_distance(point, circle, 1))  # False (距离 2 > 1)
    """
    min_dist = minimum_distance(geom1, geom2, tolerance)
    return min_dist <= distance + tolerance
