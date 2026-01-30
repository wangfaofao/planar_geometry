# -*- coding: utf-8 -*-
"""
planar_geometry/surface/__init__.py

包: 曲面模块
======================================

描述:
    包含二维几何元素（曲面/平面图形）的定义和操作。
    所有曲面类实现 Measurable2D 接口，支持面积和周长计算。

版本: 0.1.0
作者: wangheng <wangfaofao@gmail.com>

类:
    Rectangle: 矩形类 - 由四个顶点定义
    Circle: 圆形类 - 由圆心和半径定义
    Polygon: 多边形类 - 由顶点序列定义
    Triangle: 三角形类 - 特殊的三边多边形
    Ellipse: 椭圆类 - 由中心、长轴和短轴定义

功能:
    - 面积计算（各种公式）
    - 周长/圆周长计算
    - 边界框 (AABB) 获取
    - 中心/重心计算
    - 点包含判断（点在形状内/边界上）
    - 凸性、简单性、正则性判断
    - 特殊计算（三角形的外接圆、内切圆等）
    - 边和顶点的访问

使用示例:
    from planar_geometry.surface import Rectangle, Circle, Polygon, Triangle, Ellipse
    # 或
    from planar_geometry import Rectangle, Circle, Polygon, Triangle, Ellipse

    # 矩形
    rect = Rectangle.from_bounds(0, 0, 4, 3)
    area = rect.area()  # 12.0

    # 圆
    circle = Circle(Point2D(0, 0), 5.0)
    area = circle.area()  # 78.54

    # 多边形
    poly = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)])
    area = poly.area()  # 12.0
    is_convex = poly.is_convex()  # True

    # 三角形
    tri = Triangle.from_sides(3, 4, 5)
    circle = tri.get_circumcircle()

    # 椭圆
    ellipse = Ellipse(Point2D(0, 0), 5, 3, 0)
    area = ellipse.area()  # 47.12

相关模块:
    - planar_geometry.point: 使用 Point2D 作为顶点
    - planar_geometry.curve: 使用向量定义方向和边
    - planar_geometry.utils: 形状的相交、距离计算

子模块:
    - rectangle: Rectangle 类实现
    - circle: Circle 类实现
    - polygon: Polygon 类实现
    - triangle: Triangle 类实现
    - ellipse: Ellipse 类实现
"""

from planar_geometry.surface.rectangle import Rectangle
from planar_geometry.surface.circle import Circle
from planar_geometry.surface.polygon import Polygon
from planar_geometry.surface.triangle import Triangle
from planar_geometry.surface.ellipse import Ellipse

__all__ = ["Rectangle", "Circle", "Polygon", "Triangle", "Ellipse"]
