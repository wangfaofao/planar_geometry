# 快速开始指南

## 📌 文档导航

| 文档 | 用途 | 适合读者 |
|------|------|---------|
| **README.md** | 项目使用指南 + API参考 | 所有用户 |
| **AGENTS.md** | 项目架构 + 设计文档 | 开发者/架构师 |
| **QUICK_START.md** | 本文档，快速上手 | 新手用户 |

---

## 🚀 快速安装

```bash
# 从源码安装
git clone https://github.com/wangfaofao/planar_geometry.git
cd planar_geometry
pip install -e .
```

---

## 💡 5分钟上手

### 1. 最简单的例子

```python
from planar_geometry import Point2D, Vector2D

# 创建两个点
p1 = Point2D(0, 0)
p2 = Point2D(3, 4)

# 计算距离
distance = p1.distance_to(p2)
print(f"距离: {distance}")  # 5.0
```

### 2. 使用基本形状

```python
from planar_geometry import Rectangle, Circle

# 创建矩形
rect = Rectangle.from_bounds(0, 0, 4, 3)
print(f"面积: {rect.area()}")        # 12.0
print(f"周长: {rect.perimeter()}")   # 14.0

# 创建圆
circle = Circle(p1, radius=5)
print(f"面积: {circle.area()}")      # 78.54
```

### 3. 几何计算

```python
from planar_geometry import (
    LineSegment,
    line_segment_intersection,
    angle_between
)

# 计算交点
seg1 = LineSegment(Point2D(0, 0), Point2D(2, 2))
seg2 = LineSegment(Point2D(0, 2), Point2D(2, 0))
intersection = line_segment_intersection(seg1, seg2)
print(f"交点: {intersection}")  # Point2D(1, 1)

# 计算夹角
v1 = Vector2D(1, 0)
v2 = Vector2D(0, 1)
angle = angle_between(v1, v2)
print(f"夹角: {angle}°")  # 90.0
```

---

## 🎯 常见任务

### 📍 点的操作
```python
from planar_geometry import Point2D

p = Point2D(2, 3)

# 距离计算
distance = p.distance_to(Point2D(5, 7))

# 中点
midpoint = p.midpoint_to(Point2D(4, 5))

# 平移
p_moved = p.add(1, 2)  # Point2D(3, 5)

# 运算符
p_sum = p + (1, 2)     # Point2D(3, 5)
p_scaled = p * 2       # Point2D(4, 6)
```

### 📐 向量操作
```python
from planar_geometry import Vector2D

v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)

# 基本属性
length = v1.length()           # 5.0
angle = v1.angle()             # 度数

# 向量运算
dot = v1.dot(v2)               # 11.0（点积）
cross = v1.cross(v2)           # 2.0（叉积）
normalized = v1.normalized()   # Vector2D(0.6, 0.8)

# 几何操作
rotated = v1.rotated(45)       # 旋转45度
perpendicular = v1.perpendicular()  # 垂直向量
```

### 🔲 形状操作
```python
from planar_geometry import Polygon, Triangle, Rectangle

# 创建多边形
vertices = [
    Point2D(0, 0),
    Point2D(4, 0),
    Point2D(4, 3),
    Point2D(0, 3)
]
poly = Polygon(vertices)

# 几何性质
print(poly.area())              # 12.0
print(poly.perimeter())         # 14.0
print(poly.is_convex())         # True
print(poly.contains_point(Point2D(2, 1.5)))  # True

# 特殊多边形
rect = Rectangle.from_bounds(0, 0, 10, 5)
triangle = Triangle.from_sides(3, 4, 5)

# 三角形特有功能
circumcircle = triangle.get_circumcircle()  # 外接圆
incircle = triangle.get_incicle()           # 内切圆
```

---

## 📚 查找 API 文档

所有详细的 API 文档都在 **README.md** 的 API 文档部分。

按类查找：

| 类 | 行数 | 功能 |
|-----|------|------|
| Point2D | 521-527 | 二维点 |
| Vector2D | 528-535 | 二维向量 |
| LineSegment | 536-541 | 线段 |
| Line | 542-547 | 直线 |
| Rectangle | 548-553 | 矩形 |
| Circle | 554-559 | 圆形 |
| Polygon | 560-567 | 多边形 |
| Triangle | 568-575 | 三角形 |
| Ellipse | 576-583 | 椭圆 |

---

## 🔧 三种导入方式

### 方式1: 顶级导入（最简单）
```python
from planar_geometry import Point2D, Vector2D, Rectangle, Circle
```

### 方式2: 包级导入（按需）
```python
from planar_geometry.point import Point2D
from planar_geometry.curve import Vector2D, LineSegment
from planar_geometry.surface import Rectangle, Circle
```

### 方式3: 细粒度导入（灵活）
```python
from planar_geometry.point.point2d import Point2D
from planar_geometry.curve.vector2d import Vector2D
```

---

## 🧪 运行测试

```bash
# 运行所有测试
python -m unittest discover tests/ -v

# 或使用 pytest
pytest tests/ -v

# 预期: 231 个测试全部通过 ✅
```

---

## 📖 学习路径

1. **基础** (10分钟)
   - 读本快速开始
   - 试试常见任务部分

2. **进阶** (30分钟)
   - 阅读 README.md 的使用示例
   - 学习三种导入方式
   - 查阅 API 文档

3. **深入** (1小时)
   - 阅读 AGENTS.md 了解架构
   - 研究 SOLID 原则体现
   - 查看源代码学习实现

---

## ❓ 常见问题

**Q: 如何计算两条线段是否相交？**
```python
from planar_geometry import line_segment_intersection

intersection = line_segment_intersection(seg1, seg2)
if intersection is not None:
    print(f"相交于: {intersection}")
else:
    print("不相交")
```

**Q: 如何判断点是否在多边形内？**
```python
if polygon.contains_point(point):
    print("点在多边形内")
```

**Q: 如何计算凸包？**
```python
hull = polygon.get_convex_hull()
print(f"凸包面积: {hull.area()}")
```

**Q: 如何批量计算距离？**
```python
from planar_geometry import bounding_box, centroid

# 边界框
bounds = bounding_box(points)  # (x_min, y_min, x_max, y_max)

# 重心
center = centroid(points)
```

---

## 🤝 获取帮助

- 📖 查阅完整的 README.md
- 🏗️ 查看 AGENTS.md 了解架构
- 🔍 搜索 API 文档表格
- 💻 查看源代码（详细注释）
- 🧪 运行测试用例学习

---

## ✨ 特色功能

- ✅ 9个核心几何类
- ✅ 136个公开方法
- ✅ 18个工具函数
- ✅ 231个单元测试
- ✅ 完整的类型标注
- ✅ SOLID 原则设计

---

**需要更多帮助？查看完整的 README.md 或 AGENTS.md！**
