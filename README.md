# planar_geometry

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)

**高性能平面几何计算库** | 遵循 SOLID 原则 | 为 Cython 优化设计

[快速开始](#快速开始) • [API 文档](#api-文档) • [功能](#主要功能) • [示例](#使用示例)

</div>

---

## 概述

**planar_geometry** 是一个现代化的 Python 平面几何计算库，采用 SOLID 原则设计，专为高性能计算优化，为后续 Cython 改造做准备。库中包含完整的 2D 几何元素（点、线、面）和丰富的几何算法，零依赖，易于集成。

### 核心特性

- ✅ **SOLID 架构** - 清晰的继承层次，职责分离
- ✅ **零依赖** - 无任何外部依赖，轻量级设计
- ✅ **高性能** - 使用基础数据类型，便于 Cython 优化
- ✅ **完整算法** - 包含交点、距离、角度、凸包等常用几何算法
- ✅ **完善测试** - 187+ 个测试用例，覆盖率完整
- ✅ **类型安全** - 完整的类型标注，支持类型检查

---

## 快速开始

### 安装

```bash
pip install planar_geometry
```

或从源码安装：

```bash
git clone https://github.com/wangfaofao/planar_geometry.git
cd planar_geometry
pip install -e .
```

### 基础使用

```python
from planar_geometry import Point2D, Vector2D, Rectangle, Circle, Polygon

# 创建点
p1 = Point2D(0, 0)
p2 = Point2D(3, 4)
distance = p1.distance_to(p2)  # 5.0

# 创建向量
v = Vector2D(3, 4)
print(v.length())  # 5.0
print(v.normalized())  # Vector2D(0.6, 0.8)

# 创建矩形
rect = Rectangle.from_center_and_size(
    center=Point2D(0, 0),
    size=2.0,
    direction=Vector2D(1, 0)
)
print(rect.area())      # 4.0
print(rect.perimeter()) # 8.0

# 创建圆形
circle = Circle(Point2D(0, 0), 5.0)
print(circle.area())      # 78.54
print(circle.perimeter()) # 31.42

# 创建多边形
poly = Polygon.from_points([
    Point2D(0, 0),
    Point2D(4, 0),
    Point2D(4, 3),
    Point2D(0, 3)
])
print(poly.area())       # 12.0
print(poly.perimeter())  # 14.0
print(poly.is_convex())  # True
```

---

## 主要功能

| 类别 | 功能 | 说明 |
|------|------|------|
| **基础元素** | Point2D, Vector2D | 二维点和向量 |
| **线性元素** | LineSegment, Line | 线段和直线 |
| **面积元素** | Rectangle, Circle, Polygon, Triangle, Ellipse | 矩形、圆、多边形、三角形、椭圆 |
| **几何算法** | 交点、距离、角度、凸包 | 完整的 2D 几何算法 |

---

## API 文档

### 基础类 - Point2D（二维点）

二维平面上的点，是所有几何元素的构建基础。

#### 构造函数

```python
Point2D(x: float, y: float)  # 创建点 (x, y)
Point2D.origin()              # 创建原点 (0, 0)
Point2D.from_tuple(data)      # 从元组创建点
```

#### 核心方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `distance_to(other)` | 计算到另一个点的距离 | `float` |
| `distance_squared_to(other)` | 计算距离平方（避免开方） | `float` |
| `midpoint_to(other)` | 计算两点中点 | `Point2D` |
| `add(dx, dy)` | 平移点 | `Point2D` |
| `multiply(scalar)` | 缩放点坐标 | `Point2D` |
| `negate()` | 取反坐标 | `Point2D` |
| `equals(other, tolerance)` | 判断两点是否相等 | `bool` |
| `is_zero(tolerance)` | 判断是否为原点 | `bool` |
| `to_tuple()` | 转换为元组 | `tuple` |
| `length()` | 获取长度（始终为 0） | `float` |

#### 运算符重载

```python
p1 = Point2D(1, 2)
p2 = Point2D(3, 4)

p1 + (2, 3)      # 点 + 元组 = 新点
p1 - p2          # 点 - 点 = 向量
p1 * 2           # 点 * 标量 = 新点
p1 / 2           # 点 / 标量 = 新点
p1 == p2         # 比较是否相等
```

---

### 向量类 - Vector2D（二维向量）

二维向量，支持各种向量运算。

#### 构造函数

```python
Vector2D(x: float, y: float)       # 创建向量
Vector2D.zero()                    # 零向量
Vector2D.unit_x()                  # x轴单位向量 (1, 0)
Vector2D.unit_y()                  # y轴单位向量 (0, 1)
Vector2D.from_tuple(data)          # 从元组创建
```

#### 核心方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `length()` | 向量的模（长度） | `float` |
| `length_squared()` | 模的平方 | `float` |
| `angle()` | 向量角度（0-360°） | `float` |
| `angle_rad()` | 向量角度（0-2π） | `float` |
| `normalized()` | 单位化向量 | `Vector2D` |
| `dot(other)` | 点积 | `float` |
| `cross(other)` | 叉积（二维标量） | `float` |
| `perpendicular()` | 垂直向量（逆时针旋转90°） | `Vector2D` |
| `rotated(angle_deg)` | 旋转向量 | `Vector2D` |
| `projection(other)` | 投影到另一向量 | `Vector2D` |
| `component(direction)` | 在指定方向的分量 | `float` |
| `equals(other, tolerance)` | 判断是否相等 | `bool` |
| `is_zero(tolerance)` | 判断是否为零向量 | `bool` |

#### 运算符重载

```python
v1 = Vector2D(1, 0)
v2 = Vector2D(0, 1)

v1 + v2           # 向量加法
v1 - v2           # 向量减法
v1 * 2            # 向量缩放
v1 / 2            # 向量缩放（除法）
v1 == v2          # 向量比较
v1.dot(v2)        # 点积（返回 0）
v1.cross(v2)      # 叉积（返回 1）
```

---

### 线性元素 - LineSegment（线段）

由两个端点定义的有限线段。

#### 构造函数

```python
LineSegment(start: Point2D, end: Point2D)  # 创建线段
```

#### 核心方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `length()` | 计算线段长度 | `float` |
| `midpoint()` | 获取中点 | `Point2D` |
| `direction()` | 获取方向向量（单位化） | `Vector2D` |
| `contains_point(point, tolerance)` | 判断点是否在线段上 | `bool` |
| `get_parameter(point)` | 获取点在直线上的参数 t | `float` |
| `get_closest_point(point)` | 获取线段上离点最近的点 | `Point2D` |
| `get_distance_to_point(point)` | 计算点到线段的距离 | `float` |

---

### 线性元素 - Line（直线）

无限延伸的直线。

#### 构造函数

```python
Line(point: Point2D, direction: Vector2D)  # 创建直线
```

#### 核心方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `length()` | 直线长度（始终为 ∞） | `float` |
| `contains_point(point, tolerance)` | 判断点是否在直线上 | `bool` |
| `get_intersection(other)` | 计算与另一直线的交点 | `Point2D \| None` |
| `get_closest_point(point)` | 获取直线上离点最近的点（垂足） | `Point2D` |
| `get_distance_to_point(point)` | 计算点到直线的距离 | `float` |

---

### 面积元素 - Rectangle（矩形）

轴对齐或任意方向的矩形。

#### 构造函数

```python
Rectangle(vertices: List[Point2D])          # 从4个顶点创建
Rectangle.from_center_and_size(center, size, direction)  # 从中心创建
Rectangle.from_bounds(x_min, y_min, x_max, y_max)       # 从边界框创建
```

#### 核心方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `area()` | 计算面积 | `float` |
| `perimeter()` | 计算周长 | `float` |
| `get_bounds()` | 获取轴对齐边界框 | `tuple` |
| `get_center()` | 获取中心点 | `Point2D` |
| `get_edges()` | 获取4条边 | `List[tuple]` |
| `contains_point(point)` | 判断点是否在矩形内 | `bool` |
| `is_square()` | 判断是否为正方形 | `bool` |
| `get_vertex_count()` | 获取顶点数 | `int` |
| `get_edge_count()` | 获取边数 | `int` |

---

### 面积元素 - Circle（圆）

圆形，由中心点和半径定义。

#### 构造函数

```python
Circle(center: Point2D, radius: float)      # 创建圆
Circle.from_diameter(p1: Point2D, p2: Point2D)  # 从直径端点创建
```

#### 核心方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `area()` | 计算面积（π·r²） | `float` |
| `perimeter()` | 计算周长（2π·r） | `float` |
| `get_center()` | 获取圆心 | `Point2D` |
| `get_bounds()` | 获取外接正方形边界 | `tuple` |
| `contains_point(point)` | 判断点是否在圆内 | `bool` |
| `get_circumference()` | 获取圆周长（别名） | `float` |
| `equals(other, tolerance)` | 判断两圆是否相等 | `bool` |

---

### 面积元素 - Polygon（多边形）

任意多边形，支持凸性检测、凸包计算等。

#### 构造函数

```python
Polygon(vertices: List[Point2D])            # 从顶点创建
Polygon.from_points(points: List[Point2D])  # 工厂方法
Polygon.regular(n, center, radius, rotation)  # 创建正多边形
Polygon.triangle(p1, p2, p3)                # 创建三角形
Polygon.rectangle(p1, p2, p3, p4)           # 创建四边形
```

#### 核心方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `area()` | 计算面积（鞋带公式） | `float` |
| `perimeter()` | 计算周长 | `float` |
| `get_center()` | 获取中心点 | `Point2D` |
| `centroid()` | 获取质心 | `Point2D` |
| `get_bounds()` | 获取边界框 | `tuple` |
| `get_edges()` | 获取所有边 | `List[tuple]` |
| `get_vertex(index)` | 获取指定顶点 | `Point2D` |
| `get_edge(index)` | 获取指定边 | `tuple` |
| `get_vertex_count()` | 获取顶点数 | `int` |
| `get_edge_count()` | 获取边数 | `int` |
| `contains_point(point)` | 判断点是否在多边形内（射线投射） | `bool` |
| `is_convex()` | 判断是否为凸多边形 | `bool` |
| `is_simple()` | 判断是否为简单多边形（无自交） | `bool` |
| `is_regular()` | 判断是否为正多边形 | `bool` |
| `get_convex_hull()` | 计算凸包（Graham Scan） | `Polygon` |

---

### 面积元素 - Triangle（三角形）

特殊的三角形类，支持圆心、内心、垂心等特殊点计算。

#### 构造函数

```python
Triangle.from_points(vertices: List[Point2D])      # 从3个顶点创建
Triangle.from_sides(a: float, b: float, c: float)  # 从三边长创建
Triangle.triangle(p1, p2, p3)                      # 工厂方法
```

#### 核心方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `area()` | 计算面积 | `float` |
| `perimeter()` | 计算周长 | `float` |
| `get_side_lengths()` | 获取三边长度 | `tuple` |
| `get_angles()` | 获取三个内角（度） | `tuple` |
| `centroid()` | 获取重心 | `Point2D` |
| `incenter()` | 获取内心 | `Point2D` |
| `circumcenter()` | 获取外心（外接圆圆心） | `Point2D` |
| `orthocenter()` | 获取垂心 | `Point2D` |
| `inradius()` | 获取内切圆半径 | `float` |
| `circumradius()` | 获取外接圆半径 | `float` |
| `get_incicle()` | 获取内切圆 | `Circle` |
| `get_circumcircle()` | 获取外接圆 | `Circle` |
| `is_equilateral()` | 判断是否为等边三角形 | `bool` |
| `is_isosceles()` | 判断是否为等腰三角形 | `bool` |
| `is_right_angled()` | 判断是否为直角三角形 | `bool` |

---

### 面积元素 - Ellipse（椭圆）

椭圆，由中心、长轴和短轴定义。

#### 构造函数

```python
Ellipse(center: Point2D, a: float, b: float, rotation: float = 0.0)  # 创建椭圆
Ellipse.from_center_and_axes(center, major_axis, minor_axis, rotation)  # 从轴创建
Ellipse.from_foci_and_point(f1: Point2D, f2: Point2D, point: Point2D)   # 从焦点创建
```

#### 核心方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `area()` | 计算面积（π·a·b） | `float` |
| `perimeter()` | 计算周长（近似值） | `float` |
| `get_center()` | 获取椭圆中心 | `Point2D` |
| `get_bounds()` | 获取边界框 | `tuple` |
| `foci()` | 获取两个焦点 | `tuple` |
| `focal_distance()` | 获取焦距 | `float` |
| `eccentricity()` | 获取离心率 | `float` |
| `get_major_axis_endpoints()` | 获取长轴端点 | `tuple` |
| `get_minor_axis_endpoints()` | 获取短轴端点 | `tuple` |
| `contains_point(point)` | 判断点是否在椭圆内 | `bool` |
| `equals(other, tolerance)` | 判断两椭圆是否相等 | `bool` |

---

### 工具函数 - geometry_utils

#### 交点计算

```python
# 线段交点
line_segment_intersection(s1, s2, tolerance=1e-9) -> Point2D | None

# 直线交点
line_intersection(l1, l2, tolerance=1e-9) -> Point2D | None

# 矩形交点
rectangle_intersection_points(r1, r2, tolerance=1e-6) -> List[Point2D]

# 多边形交点
polygon_intersection_points(poly1, poly2, tolerance=1e-6) -> List[Point2D]
```

#### 距离计算

```python
# 点到线段距离
point_to_segment_distance(point, segment) -> float
point_to_segment_closest_point(point, segment) -> Point2D

# 点到直线距离
point_to_line_distance(point, line) -> float
point_to_line_closest_point(point, line) -> Point2D

# 点到面距离
point_to_rectangle_distance(point, rect) -> float
point_to_polygon_distance(point, poly) -> float

# 线段间距离
segments_distance(s1, s2) -> float
segments_closest_points(s1, s2) -> Tuple[Point2D, Point2D]
```

#### 角度计算

```python
# 向量夹角
angle_between(v1, v2) -> float          # 返回角度（度）
angle_between_rad(v1, v2) -> float      # 返回角度（弧度）

# 向量关系判断
are_perpendicular(v1, v2, tolerance=1e-6) -> bool  # 垂直
are_parallel(v1, v2, tolerance=1e-6) -> bool       # 平行
```

#### 点集工具

```python
# 边界框
bounding_box(points: List[Point2D]) -> Tuple[float, float, float, float]

# 重心/质心
centroid(points: List[Point2D]) -> Point2D
```

---

## 使用示例

### 示例 1：计算两条直线的交点

```python
from planar_geometry import Point2D, Vector2D, Line, line_intersection

# 创建两条直线
line1 = Line(Point2D(0, 0), Vector2D(1, 1))
line2 = Line(Point2D(0, 2), Vector2D(1, -1))

# 计算交点
intersection = line_intersection(line1, line2)
print(f"交点: {intersection}")  # Point2D(1, 1)
```

### 示例 2：计算多边形面积和周长

```python
from planar_geometry import Point2D, Polygon

# 创建五边形
vertices = [
    Point2D(0, 0),
    Point2D(4, 0),
    Point2D(5, 3),
    Point2D(2, 5),
    Point2D(-1, 3)
]
polygon = Polygon.from_points(vertices)

print(f"面积: {polygon.area():.2f}")
print(f"周长: {polygon.perimeter():.2f}")
print(f"是否为凸多边形: {polygon.is_convex()}")
print(f"中心点: {polygon.get_center()}")
```

### 示例 3：判断点是否在矩形内

```python
from planar_geometry import Point2D, Rectangle

# 创建矩形
rect = Rectangle.from_bounds(0, 0, 10, 10)

# 判断点
p1 = Point2D(5, 5)
p2 = Point2D(15, 15)

print(f"点 (5, 5) 在矩形内: {rect.contains_point(p1)}")     # True
print(f"点 (15, 15) 在矩形内: {rect.contains_point(p2)}")   # False
```

### 示例 4：计算三角形的特殊点

```python
from planar_geometry import Point2D, Triangle

# 创建三角形
triangle = Triangle.from_points([
    Point2D(0, 0),
    Point2D(4, 0),
    Point2D(2, 3)
])

print(f"面积: {triangle.area():.2f}")
print(f"周长: {triangle.perimeter():.2f}")
print(f"重心: {triangle.centroid()}")
print(f"外心: {triangle.circumcenter()}")
print(f"内心: {triangle.incenter()}")
print(f"垂心: {triangle.orthocenter()}")
print(f"内切圆: {triangle.get_incicle()}")
print(f"外接圆: {triangle.get_circumcircle()}")
print(f"是否为等边三角形: {triangle.is_equilateral()}")
```

### 示例 5：向量运算

```python
from planar_geometry import Vector2D
import math

# 创建向量
v1 = Vector2D(3, 4)
v2 = Vector2D(1, 0)

# 基本运算
print(f"v1 的模: {v1.length()}")           # 5.0
print(f"v1 的单位向量: {v1.normalized()}")  # Vector2D(0.6, 0.8)

# 点积和叉积
print(f"点积: {v1.dot(v2)}")               # 3.0
print(f"叉积: {v1.cross(v2)}")             # 4.0

# 角度
angle = v1.angle()
print(f"v1 的角度: {angle:.2f}°")

# 旋转
v_rotated = v1.rotated(90)
print(f"旋转90°: {v_rotated}")
```

### 示例 6：凸包计算

```python
from planar_geometry import Point2D, Polygon

# 创建点集
points = [
    Point2D(0, 0),
    Point2D(1, 1),
    Point2D(2, 2),
    Point2D(0, 2),
    Point2D(2, 0),
    Point2D(1, 0),
]

poly = Polygon.from_points(points)

# 计算凸包
convex_hull = poly.get_convex_hull()
print(f"凸包顶点数: {convex_hull.get_vertex_count()}")
print(f"凸包面积: {convex_hull.area():.2f}")
```

---

## 项目结构

```
planar_geometry/
├── src/planar_geometry/           # 源代码
│   ├── __init__.py                # 模块导出
│   ├── measurable.py              # 抽象基类
│   ├── point.py                   # Point2D 类
│   ├── curve.py                   # Curve, LineSegment, Line, Vector2D
│   ├── surface.py                 # Surface, Rectangle, Circle, Polygon, Triangle, Ellipse
│   └── geometry_utils.py          # 工具函数
├── tests/                         # 测试套件
│   ├── test_point.py
│   ├── test_curve.py
│   ├── test_surface.py
│   ├── test_triangle_ellipse.py
│   └── test_geometry_utils.py
├── AGENTS.md                      # 架构设计文档
├── README.md                      # 项目说明（本文件）
├── pyproject.toml                 # 包配置
└── LICENSE                        # MIT 许可
```

---

## 测试

项目包含 187+ 个测试用例，全部通过。

```bash
# 安装测试依赖
pip install pytest

# 运行所有测试
pytest tests/

# 查看覆盖率
pytest tests/ --cov=src/planar_geometry

# 运行特定测试
pytest tests/test_point.py -v
```

---

## 性能优化

库采用以下优化策略：

1. **Cython 友好** - 使用基础数据类型（float, int），避免复杂对象
2. **避免不必要开方** - 提供 `distance_squared_to()` 等平方版本
3. **参数重用** - 避免重复计算
4. **类型标注** - 便于 JIT 编译优化

---

## 后续计划

- [ ] Cython 性能优化（3x-10x 性能提升）
- [ ] 3D 几何扩展
- [ ] 高级算法（Delaunay 三角剖分、Voronoi 图）
- [ ] 变换矩阵支持
- [ ] 空间索引（KD-Tree）
- [ ] 更多特殊几何形状

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 联系方式

- 作者: wangheng
- 邮箱: wangfaofao@gmail.com
- GitHub: [@wangfaofao](https://github.com/wangfaofao)

---

## 致谢

感谢所有贡献者和使用者的支持！

---

**Made with ❤️ for geometry lovers**
