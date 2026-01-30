# -*- coding: utf-8 -*-
"""
planar_geometry/curve/__init__.py

包: 曲线模块
======================================

描述:
    包含一维几何元素（曲线）的定义和操作。
    所有曲线类实现 Measurable1D 接口，支持长度计算。

版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

类:
    LineSegment: 线段类 - 由两个端点定义的有限线段
    Line: 直线类 - 无限延伸的直线
    Vector2D: 二维向量类 - 方向和大小的组合

功能:
    - 线段：端点、长度、方向、点包含判断、最近点
    - 直线：无限延伸、方向向量、点到直线距离、交点
    - 向量：模长、角度、点积、叉积、旋转、投影、归一化

使用示例:
    from planar_geometry.curve import LineSegment, Line, Vector2D
    # 或
    from planar_geometry import LineSegment, Line, Vector2D

    # 线段
    seg = LineSegment(Point2D(0, 0), Point2D(3, 4))
    length = seg.length()  # 5.0
    mid = seg.midpoint()  # Point2D(1.5, 2.0)

    # 直线
    line = Line(Point2D(0, 0), Vector2D(1, 1))

    # 向量
    v1 = Vector2D(1, 0)
    v2 = Vector2D(0, 1)
    dot = v1.dot(v2)  # 0.0
    cross = v1.cross(v2)  # 1.0

相关模块:
    - planar_geometry.point: 使用 Point2D 作为端点
    - planar_geometry.surface: 使用向量定义方向
    - planar_geometry.utils: 曲线的相交、距离计算

子模块:
    - line_segment: LineSegment 类实现
    - line: Line 类实现
    - vector2d: Vector2D 类实现
"""

from planar_geometry.curve.line import Line
from planar_geometry.curve.line_segment import LineSegment
from planar_geometry.curve.vector2d import Vector2D

__all__ = ["LineSegment", "Line", "Vector2D"]
