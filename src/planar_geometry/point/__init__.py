# -*- coding: utf-8 -*-
"""
planar_geometry/point/__init__.py

包: 二维点模块
======================================

描述:
    包含二维点的定义和操作，是平面几何中的基本元素。
    Point2D 是一个零维几何元素，实现了 Measurable1D 接口。

版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

类:
    Point2D: 二维点类 - 定义和操作平面上的点

功能:
    - 点的创建与表示
    - 距离计算（到其他点）
    - 中点计算
    - 算术运算（平移、缩放、取反）
    - 点的相等性判断
    - 元组转换

使用示例:
    from planar_geometry.point import Point2D
    # 或
    from planar_geometry import Point2D

    # 创建点
    p1 = Point2D(0, 0)
    p2 = Point2D(3, 4)

    # 距离计算
    dist = p1.distance_to(p2)  # 5.0

    # 算术运算
    p3 = p1.add(2, 3)  # Point2D(2, 3)
    p4 = p2.multiply(2)  # Point2D(6, 8)

    # 特殊点
    origin = Point2D.origin()  # Point2D(0, 0)

相关模块:
    - planar_geometry.curve: 使用 Point2D 定义曲线（线段、直线）
    - planar_geometry.surface: 使用 Point2D 定义曲面（矩形、圆、多边形）
    - planar_geometry.utils: 点集工具函数
"""

from planar_geometry.point.point2d import Point2D

__all__ = ["Point2D"]
