# planar_geometry

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Tests](https://img.shields.io/badge/tests-231%2F231%20passing-brightgreen.svg)

**高性能平面几何计算库** | 遵循 SOLID 原则 | 模块化架构 | Cython 友好

[快速开始](#快速开始) • [API 文档](#api-文档) • [架构](#项目架构) • [示例](#使用示例) • [测试](#测试)

</div>

---

## 概述

**planar_geometry** 是一个现代化的 Python 平面几何计算库，采用 SOLID 原则设计，具有模块化架构，专为高性能计算优化，为后续 Cython 改造做好准备。库中包含完整的 2D 几何元素（点、线、面）和丰富的几何算法，**零依赖**，易于集成。

### 🎯 核心特性

- ✅ **SOLID 架构** - 清晰的继承层次，职责分离，易于扩展
- ✅ **模块化设计** - 细粒度包结构，按需导入，快速启动
- ✅ **零依赖** - 无任何外部依赖，轻量级设计（仅标准库）
- ✅ **高性能** - 使用基础数据类型，便于 Cython 编译优化
- ✅ **完整算法** - 交点、距离、角度、凸包、点包含等常用算法
- ✅ **完善测试** - 231 个单元测试，100% 通过率
- ✅ **完整文档** - 详细的中英文文档和 API 说明
- ✅ **类型安全** - 完整的类型标注，支持类型检查

---

## 项目架构

### 📦 模块结构

```
planar_geometry/
├── abstracts/          # 抽象基类 (5个)
│   └── Measurable → Measurable1D → Measurable2D, Curve, Surface
│
├── point/              # 点模块
│   └── Point2D (17个方法)
│
├── curve/              # 曲线模块
│   ├── Vector2D (27个方法)
│   ├── LineSegment (10个方法)
│   └── Line (9个方法)
│
├── surface/            # 曲面模块
│   ├── Rectangle (15个方法)
│   ├── Circle (12个方法)
│   ├── Polygon (23个方法)
│   ├── Triangle (36个方法)
│   └── Ellipse (17个方法)
│
└── utils/              # 工具函数 (18个)
    ├── 交点计算 (4个)
    ├── 距离计算 (8个)
    ├── 角度计算 (4个)
    └── 点集工具 (2个)
```

### 📊 功能统计

| 指标 | 数值 |
|------|------|
| 核心类 | 9 个 |
| 公开方法 | 136 个 |
| 工具函数 | 18 个 |
| 总测试数 | 231 个 |
| 代码行数 | 2,380 行 |
| 测试通过率 | 100% ✅ |

---

## 快速开始

### 安装

```bash
# 使用 pip 安装（待发布到 PyPI）
pip install planar_geometry

# 或从源码安装
git clone https://github.com/wangfaofao/planar_geometry.git
cd planar_geometry
pip install -e .
```

### 基础使用

#### 1️⃣ 点和向量

```python
from planar_geometry import Point2D, Vector2D

# 创建点
p1 = Point2D(0, 0)
p2 = Point2D(3, 4)

# 点的距离
distance = p1.distance_to(p2)  # 5.0

# 创建向量
v1 = Vector2D(1, 0)
v2 = Vector2D(0, 1)

# 向量运算
dot_product = v1.dot(v2)  # 0.0
magnitude = v1.length()   # 1.0
normalized = v1.normalized()  # Vector2D(1, 0)
```

#### 2️⃣ 线段和直线

```python
from planar_geometry import LineSegment, Line, Vector2D, Point2D

# 创建线段
seg = LineSegment(Point2D(0, 0), Point2D(3, 4))
seg_length = seg.length()  # 5.0
midpoint = seg.midpoint()  # Point2D(1.5, 2.0)

# 创建直线
line = Line(Point2D(0, 0), Vector2D(1, 1))
distance = line.get_distance_to_point(Point2D(1, 0))
```

#### 3️⃣ 基本形状

```python
from planar_geometry import Rectangle, Circle, Polygon, Triangle

# 矩形
rect = Rectangle.from_bounds(0, 0, 4, 3)
print(f"面积: {rect.area()}")      # 12.0
print(f"周长: {rect.perimeter()}")  # 14.0

# 圆形
circle = Circle(Point2D(0, 0), 5)
print(f"面积: {circle.area()}")      # 78.54
print(f"周长: {circle.perimeter()}")  # 31.42

# 多边形
vertices = [Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)]
poly = Polygon(vertices)
print(f"是否凸多边形: {poly.is_convex()}")  # True

# 三角形（继承自Polygon）
tri = Triangle.from_sides(3, 4, 5)
circumcircle = tri.get_circumcircle()  # 获取外接圆
incircle = tri.get_incicle()           # 获取内切圆
```

#### 4️⃣ 几何算法

```python
from planar_geometry import (
    line_segment_intersection,
    point_to_segment_distance,
    angle_between,
    bounding_box,
    centroid
)

# 线段交点
seg1 = LineSegment(Point2D(0, 0), Point2D(2, 2))
seg2 = LineSegment(Point2D(0, 2), Point2D(2, 0))
intersection = line_segment_intersection(seg1, seg2)  # Point2D(1, 1)

# 点到线段的距离
point = Point2D(2, 3)
segment = LineSegment(Point2D(0, 0), Point2D(4, 0))
dist = point_to_segment_distance(point, segment)  # 3.0

# 向量夹角
v1 = Vector2D(1, 0)
v2 = Vector2D(0, 1)
angle = angle_between(v1, v2)  # 90.0°

# 点集工具
points = [Point2D(0, 0), Point2D(4, 3), Point2D(2, 5)]
bounds = bounding_box(points)  # (0, 0, 4, 5)
center = centroid(points)      # Point2D(2.0, 2.67)
```

---

## 导入方式

### 📌 方式 1: 顶级导入（推荐）

```python
# 导入所有常用类和函数
from planar_geometry import (
    # 点和向量
    Point2D, Vector2D,
    # 曲线
    LineSegment, Line,
    # 曲面
    Rectangle, Circle, Polygon, Triangle, Ellipse,
    # 抽象类（可选）
    Measurable, Measurable1D, Measurable2D, Curve, Surface,
    # 工具函数
    line_segment_intersection,
    angle_between,
    bounding_box,
    centroid
)
```

### 📌 方式 2: 包级导入

```python
# 按模块导入
from planar_geometry.point import Point2D
from planar_geometry.curve import Vector2D, LineSegment, Line
from planar_geometry.surface import Rectangle, Circle, Polygon, Triangle, Ellipse
from planar_geometry.utils import (
    line_segment_intersection,
    angle_between,
    bounding_box
)
```

### 📌 方式 3: 细粒度导入

```python
# 直接从子模块导入
from planar_geometry.point.point2d import Point2D
from planar_geometry.curve.vector2d import Vector2D
from planar_geometry.surface.rectangle import Rectangle
from planar_geometry.utils.geometry_utils import line_segment_intersection
```

---

## API 文档

### 🔷 Point2D（二维点）

| 方法 | 说明 |
|------|------|
| `distance_to(other)` | 计算到另一点的距离 |
| `midpoint_to(other)` | 计算中点 |
| `add(dx, dy)` | 平移点 |
| `multiply(scalar)` | 缩放点 |
| `equals(other, tolerance)` | 相等性判断 |
| `to_tuple()` | 转换为元组 |

### 🔷 Vector2D（二维向量）

| 方法 | 说明 |
|------|------|
| `length()` | 计算向量模长 |
| `angle()` | 计算角度（度） |
| `normalized()` | 归一化 |
| `dot(other)` | 点积 |
| `cross(other)` | 叉积（标量） |
| `rotated(angle)` | 旋转 |
| `projection(other)` | 投影 |

### 🔷 LineSegment（线段）

| 方法 | 说明 |
|------|------|
| `length()` | 计算线段长度 |
| `midpoint()` | 获取中点 |
| `direction()` | 获取方向向量 |
| `contains_point(point)` | 判断点是否在线段上 |
| `get_closest_point(point)` | 获取最近的点 |

### 🔷 Line（直线）

| 方法 | 说明 |
|------|------|
| `length()` | 返回 ∞ |
| `get_intersection(other)` | 计算交点 |
| `get_distance_to_point(point)` | 点到直线距离 |
| `contains_point(point)` | 判断点是否在直线上 |

### 🔷 Rectangle（矩形）

| 方法 | 说明 |
|------|------|
| `area()` | 计算面积 |
| `perimeter()` | 计算周长 |
| `contains_point(point)` | 点包含检测 |
| `is_square()` | 是否为正方形 |
| `from_bounds()` | 工厂方法：从边界创建 |
| `from_center_and_size()` | 工厂方法：从中心创建 |

### 🔷 Circle（圆）

| 方法 | 说明 |
|------|------|
| `area()` | 计算面积 |
| `perimeter()` | 计算周长 |
| `contains_point(point)` | 点包含检测 |
| `from_diameter()` | 工厂方法：从直径创建 |

### 🔷 Polygon（多边形）

| 方法 | 说明 |
|------|------|
| `area()` | 计算面积（鞋带公式） |
| `perimeter()` | 计算周长 |
| `contains_point(point)` | 射线投射判断 |
| `is_convex()` | 是否为凸多边形 |
| `is_simple()` | 是否为简单多边形 |
| `get_convex_hull()` | Graham Scan 凸包 |
| `regular(n, center, radius)` | 工厂方法：正多边形 |

### 🔷 Triangle（三角形）

| 方法 | 说明 |
|------|------|
| 继承所有 Polygon 方法 | + |
| `get_circumcircle()` | 获取外接圆 |
| `get_incicle()` | 获取内切圆 |
| `from_sides(a, b, c)` | 工厂方法：从边长创建 |
| `circumradius()` | 外接圆半径 |
| `inradius()` | 内切圆半径 |

### 🔷 Ellipse（椭圆）

| 方法 | 说明 |
|------|------|
| `area()` | 计算面积 |
| `perimeter()` | 计算周长 |
| `contains_point(point)` | 点包含检测 |
| `get_point_at(t)` | 参数方程求点 |

### 🔷 工具函数

#### 交点计算
- `line_segment_intersection(seg1, seg2)` - 线段交点
- `line_intersection(line1, line2)` - 直线交点
- `rectangle_intersection_points(rect1, rect2)` - 矩形交点集
- `polygon_intersection_points(poly1, poly2)` - 多边形交点集

#### 距离计算
- `point_to_segment_distance(point, segment)` - 点到线段距离
- `point_to_segment_closest_point(point, segment)` - 线段上最近的点
- `point_to_line_distance(point, line)` - 点到直线距离
- `point_to_line_closest_point(point, line)` - 直线上最近的点
- `point_to_rectangle_distance(point, rect)` - 点到矩形距离
- `point_to_polygon_distance(point, poly)` - 点到多边形距离
- `segments_distance(seg1, seg2)` - 线段间距离
- `segments_closest_points(seg1, seg2)` - 线段最近点对

#### 角度计算
- `angle_between(v1, v2)` - 向量夹角（度）
- `angle_between_rad(v1, v2)` - 向量夹角（弧度）
- `are_perpendicular(v1, v2)` - 是否垂直
- `are_parallel(v1, v2)` - 是否平行

#### 点集工具
- `bounding_box(points)` - 轴对齐边界框
- `centroid(points)` - 点集重心

---

## 测试

项目包含 **231 个单元测试**，覆盖所有核心功能：

```bash
# 运行所有测试
python -m unittest discover tests/ -v

# 或使用 pytest
pytest tests/ -v

# 测试统计
# test_point.py ........... 33 个测试 ✅
# test_curve.py ........... 54 个测试 ✅
# test_surface.py ......... 50 个测试 ✅
# test_geometry_utils.py .. 31 个测试 ✅
# test_geometry.py ........ 29 个测试 ✅
# test_triangle_ellipse.py  34 个测试 ✅
# ─────────────────────────────────────
# 总计 ................... 231 个测试 ✅
```

---

## 设计原则

项目严格遵循 **SOLID 原则**：

### S - Single Responsibility Principle（单一职责）
- 每个类只负责一种几何元素
- 每个模块只负责一类功能

### O - Open/Closed Principle（开放封闭）
- 对扩展开放：新增几何类只需创建新模块
- 对修改关闭：现有代码不需要修改

### L - Liskov Substitution Principle（里氏替换）
- 所有子类可替换基类使用
- 抽象类保证契约

### I - Interface Segregation Principle（接口隔离）
- `Measurable1D` 提供长度接口
- `Measurable2D` 提供面积接口
- 避免"胖接口"

### D - Dependency Inversion Principle（依赖倒置）
- 依赖抽象类，不依赖具体实现
- 高层模块不依赖低层模块

---

## 性能优化

### 当前优化
- ✅ 使用基础数据类型（float, int）
- ✅ 避免不必要的对象创建
- ✅ 使用高效的算法（例如 Graham Scan 凸包）

### 后续计划
- 🔄 Cython 编译（3-10x 性能提升）
- 🔄 NumPy 集成（批量计算）
- 🔄 JIT 编译（使用 Numba）

---

## 使用场景

- 🎮 **游戏开发** - 碰撞检测、物体变换
- 🗺️ **地理信息** - 坐标转换、距离计算
- 🔬 **科学计算** - 几何分析、数据可视化
- 🏗️ **计算几何** - 凸包、三角剖分、路径规划
- 📊 **数据可视化** - 图形变换、坐标计算
- 🤖 **机器人学** - 运动规划、传感器处理

---

## 项目结构

```
planar_geometry/
├── src/planar_geometry/           # 源代码
│   ├── __init__.py                # 主导出
│   ├── abstracts/                 # 抽象基类
│   ├── point/                     # 点模块
│   ├── curve/                     # 曲线模块
│   ├── surface/                   # 曲面模块
│   └── utils/                     # 工具函数
│
├── tests/                         # 单元测试
│   ├── test_point.py
│   ├── test_curve.py
│   ├── test_surface.py
│   ├── test_geometry_utils.py
│   ├── test_geometry.py
│   └── test_triangle_ellipse.py
│
├── AGENTS.md                      # 项目设计文档
├── README.md                      # 项目说明
├── pyproject.toml                 # 包配置
└── .gitignore                     # Git 忽略

```

---

## 贡献

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 代码规范

- 遵循 PEP 8
- 添加类型标注
- 编写单元测试
- 更新文档

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 作者

- **wangheng** - [wangfaofao@gmail.com](mailto:wangfaofao@gmail.com)

---

## 更新日志

### v0.1.0 (2026-01-31)
- ✅ 完成模块化架构重构
- ✅ 实现 9 个核心类，136 个公开方法
- ✅ 实现 18 个工具函数
- ✅ 通过 231 个单元测试
- ✅ 完整的中英文文档

### 下一步计划
- 🔄 性能优化（Cython）
- 🔄 功能扩展（Path, Transform）
- 🔄 发布到 PyPI
- 🔄 完整的 API 文档

---

<div align="center">

**Made with ❤️ in 2026**

[⬆ 回到顶部](#planar_geometry)

</div>
