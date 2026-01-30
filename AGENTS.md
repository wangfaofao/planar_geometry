# planar_geometry - 平面几何计算库

**版本**: 0.1.0  
**状态**: 稳定版本（完全实现）

---

## 1. 项目概述

### 1.1 简介

`planar_geometry` 是一个基于 SOLID 原则设计的 Python 平面几何库，专为高性能计算优化，支持后续 Cython 改造。

### 1.2 设计目标

- **SOLID 架构**: 清晰的抽象层次和职责分离
- **Cython 友好**: 使用基本数据类型，便于后续性能优化
- **可测试性**: 每个组件可独立测试
- **可扩展性**: 易于添加新的几何元素

---

## 2. 架构设计

### 2.1 抽象基类层次

```
Measurable (可计算度量根抽象类)
│
├── Measurable1D (可计算长度)
│   │
│   ├── Point2D (二维点 - 零维几何元素)
│   │   * length() 返回 0.0
│   │
│   └── Curve (曲线抽象基类)
│       │
│       ├── LineSegment (线段)
│       │   * 由两个端点定义的有限线段
│       │
│       ├── Line (直线 - 无限延伸)
│       │   * length() 返回 float('inf')
│       │
│       └── Vector2D (二维向量)
│           * length() 返回模长
│
└── Measurable2D (可计算面积 - 继承 Measurable1D)
    │
    └── Surface (曲面/平面图形抽象基类)
        │
        ├── Rectangle (矩形)
        │   * area() 返回面积
        │   * perimeter() 返回周长
        │   * length() 默认返回 perimeter()
        │
        ├── Circle (圆形)
        │   * area() 返回 πr²
        │   * perimeter() 返回 2πr
        │
        └── Polygon (多边形)
            * area() 返回多边形面积（鞋带公式）
            * perimeter() 返回多边形周长
            * contains_point() 射线投射算法
            * is_convex() 凸性判断
            * is_simple() 简单性判断
            * is_regular() 正则性判断
            * get_convex_hull() Graham Scan 凸包
```

### 2.2 SOLID 原则体现

| 原则 | 体现 |
|------|------|
| **单一职责 (SRP)** | 每个类只负责一种几何元素 |
| **开放封闭 (OCP)** | 新增几何元素只需继承对应抽象类 |
| **里氏替换 (LSP)** | 子类可替换基类使用 |
| **接口隔离 (ISP)** | Measurable1D/2D 分离长度和面积接口 |
| **依赖倒置 (DIP)** | 依赖抽象基类，不依赖具体实现 |

---

## 3. 模块说明

### 3.1 abstracts/ - 抽象基类模块

模块位置：`planar_geometry/abstracts/__init__.py`

**功能**: 定义所有几何元素的抽象基类层次结构

```python
class Measurable(ABC):
    """可计算度量根抽象类 - 所有几何元素的基础"""
    @abstractmethod
    def __repr__(self) -> str:
        """字符串表示"""

class Measurable1D(Measurable, ABC):
    """可计算长度抽象类 - 具有长度的几何元素"""
    @abstractmethod
    def length(self) -> float:
        """返回长度值"""

class Measurable2D(Measurable1D, ABC):
    """可计算面积抽象类 - 二维几何元素"""
    @abstractmethod
    def area(self) -> float:
        """返回面积值"""
    
    @abstractmethod
    def perimeter(self) -> float:
        """返回周长值"""
    
    def length(self) -> float:
        """二维图形的长度即周长"""
        return self.perimeter()

class Curve(Measurable1D, ABC):
    """曲线抽象基类 - 一维几何元素"""
    @abstractmethod
    def length(self) -> float:
        """返回曲线长度"""

class Surface(Measurable2D, ABC):
    """曲面/平面图形抽象基类 - 二维几何元素"""
    @abstractmethod
    def area(self) -> float:
        """返回图形面积"""
    
    @abstractmethod
    def perimeter(self) -> float:
        """返回图形周长"""
```

### 3.2 point/ - 点模块

模块位置：`planar_geometry/point/point2d.py`

**类**: Point2D（二维点）  
**方法数**: 17个  
**继承自**: Measurable1D

**核心方法**:
- `distance_to()` - 计算到另一点的距离
- `distance_squared_to()` - 计算距离的平方
- `midpoint_to()` - 计算中点
- `add(dx, dy)` - 平移点
- `multiply(scalar)` - 缩放点
- `negate()` - 取反
- `equals()` - 相等性判断
- `is_zero()` - 是否为原点
- `to_tuple()` / `from_tuple()` - 元组转换
- 运算符重载：`+`, `-`, `*`, `/`, `==`, `hash`

### 3.3 curve/ - 曲线模块

模块位置：`planar_geometry/curve/`

#### 3.3.1 LineSegment（线段）
**类**: LineSegment  
**方法数**: 10个  
**继承自**: Curve

**核心方法**:
- `length()` - 线段长度
- `midpoint()` - 中点
- `direction()` - 方向向量（归一化）
- `contains_point()` - 点在线段上判断
- `get_closest_point()` - 获取最近的点
- `get_distance_to_point()` - 点到线段距离
- `get_parameter()` - 参数 t 值

#### 3.3.2 Line（直线）
**类**: Line  
**方法数**: 9个  
**继承自**: Curve

**核心方法**:
- `length()` - 返回 ∞
- `get_intersection()` - 与另一直线的交点
- `get_distance_to_point()` - 点到直线距离
- `get_closest_point()` - 垂足
- `contains_point()` - 点在直线上判断

#### 3.3.3 Vector2D（二维向量）
**类**: Vector2D  
**方法数**: 27个  
**继承自**: Curve

**核心方法**:
- `length()` / `length_squared()` - 向量模长
- `angle()` / `angle_rad()` - 角度（度/弧度）
- `normalized()` - 归一化
- `dot()` - 点积
- `cross()` - 叉积（2D标量）
- `perpendicular()` - 垂直向量
- `rotated()` - 旋转
- `projection()` - 投影到另一向量
- `component()` - 在指定方向的分量
- `is_zero()` / `equals()` - 相等性判断
- 静态方法：`zero()`, `unit_x()`, `unit_y()`
- 运算符重载

### 3.4 surface/ - 曲面模块

模块位置：`planar_geometry/surface/`

#### 3.4.1 Rectangle（矩形）
**类**: Rectangle  
**方法数**: 15个  
**继承自**: Surface

**核心方法**:
- `area()` - 面积
- `perimeter()` - 周长
- `contains_point()` - 点包含检测
- `is_square()` - 是否为正方形
- `get_center()` - 中心点
- `get_bounds()` - 轴对齐边界框
- 工厂方法：`from_bounds()`, `from_center_and_size()`

#### 3.4.2 Circle（圆）
**类**: Circle  
**方法数**: 12个  
**继承自**: Surface

**核心方法**:
- `area()` - 面积（πr²）
- `perimeter()` - 周长（2πr）
- `contains_point()` - 点包含检测
- `get_center()` - 圆心
- `get_bounds()` - 边界框
- `get_circumference()` - 周长别名
- `equals()` - 相等性判断
- 工厂方法：`from_diameter()`

#### 3.4.3 Polygon（多边形）
**类**: Polygon  
**方法数**: 23个  
**继承自**: Surface

**核心方法**:
- `area()` - 面积（鞋带公式）
- `perimeter()` - 周长
- `contains_point()` - 射线投射判断
- `is_convex()` - 凸性检测
- `is_simple()` - 简单性检测（不自交）
- `is_regular()` - 正多边形判断
- `get_convex_hull()` - Graham Scan 凸包
- `get_center()` / `centroid()` - 中心/质心
- `get_edges()` / `get_vertices()` - 边和顶点
- 工厂方法：`from_points()`, `regular()`, `triangle()`, `rectangle()`

#### 3.4.4 Triangle（三角形）
**类**: Triangle  
**方法数**: 36个  
**继承自**: Polygon

**特殊方法**:
- `get_circumcircle()` - 外接圆
- `get_incicle()` - 内切圆
- `circumradius()` - 外接圆半径
- `inradius()` - 内切圆半径
- `circumcenter()` - 外心
- `incenter()` - 内心
- 边长计算、角度判断
- 工厂方法：`from_sides()`

#### 3.4.5 Ellipse（椭圆）
**类**: Ellipse  
**方法数**: 17个  
**继承自**: Surface

**核心方法**:
- `area()` - 面积
- `perimeter()` - 周长（数值近似）
- `contains_point()` - 点包含检测
- `get_center()` - 中心
- `get_bounds()` - 边界框
- `get_point_at()` - 参数方程求点
- `get_tangent_at()` - 切线向量

### 3.5 utils/ - 工具函数模块

模块位置：`planar_geometry/utils/geometry_utils.py`

**函数数**: 18个

#### 3.5.1 交点计算（4个函数）
```python
line_segment_intersection(seg1, seg2, tolerance)  # 线段交点
line_intersection(line1, line2, tolerance)         # 直线交点
rectangle_intersection_points(rect1, rect2, ...)   # 矩形交点集
polygon_intersection_points(poly1, poly2, ...)     # 多边形交点集
```

#### 3.5.2 距离计算（8个函数）
```python
point_to_segment_distance(point, segment)          # 点到线段距离
point_to_segment_closest_point(point, segment)     # 线段上最近的点
point_to_line_distance(point, line)                # 点到直线距离
point_to_line_closest_point(point, line)           # 直线上最近的点
point_to_rectangle_distance(point, rect)           # 点到矩形距离
point_to_polygon_distance(point, poly)             # 点到多边形距离
segments_distance(seg1, seg2)                      # 线段间距离
segments_closest_points(seg1, seg2)                # 线段最近点对
```

#### 3.5.3 角度计算（4个函数）
```python
angle_between(v1, v2)                              # 向量夹角（度）
angle_between_rad(v1, v2)                          # 向量夹角（弧度）
are_perpendicular(v1, v2, tolerance)               # 垂直性判断
are_parallel(v1, v2, tolerance)                    # 平行性判断
```

#### 3.5.4 点集工具（2个函数）
```python
bounding_box(points)                               # 轴对齐边界框
centroid(points)                                   # 点集重心
```



## 4. 项目结构

### 4.1 新的模块化架构

```
planar_geometry/
├── src/planar_geometry/
│   ├── __init__.py                      # 主导出（40个导出项）
│   │
│   ├── abstracts/                       # 抽象基类包
│   │   └── __init__.py                  # 5个抽象类
│   │       ├── Measurable               # 根抽象类
│   │       ├── Measurable1D             # 一维测量接口
│   │       ├── Measurable2D             # 二维测量接口
│   │       ├── Curve                    # 曲线抽象类
│   │       └── Surface                  # 曲面抽象类
│   │
│   ├── point/                           # 点模块包
│   │   ├── __init__.py                  # 导出入口
│   │   └── point2d.py                   # Point2D 类（33个方法）
│   │
│   ├── curve/                           # 曲线模块包（3个子模块）
│   │   ├── __init__.py                  # 导出入口
│   │   ├── line_segment.py              # LineSegment 类（7个方法）
│   │   ├── line.py                      # Line 类（5个方法）
│   │   └── vector2d.py                  # Vector2D 类（39个方法）
│   │
│   ├── surface/                         # 曲面模块包（5个子模块）
│   │   ├── __init__.py                  # 导出入口
│   │   ├── rectangle.py                 # Rectangle 类（8个方法）
│   │   ├── circle.py                    # Circle 类（7个方法）
│   │   ├── polygon.py                   # Polygon 类（18个方法）
│   │   ├── triangle.py                  # Triangle 类（14个方法）
│   │   └── ellipse.py                   # Ellipse 类（11个方法）
│   │
│   └── utils/                           # 工具函数包
│       ├── __init__.py                  # 导出入口（18个函数）
│       └── geometry_utils.py            # 所有工具函数实现
│           ├── 交点计算: 4 个函数
│           ├── 距离计算: 8 个函数
│           ├── 角度计算: 4 个函数
│           └── 点集工具: 2 个函数
│
├── tests/
│   ├── test_point.py                    # Point2D 测试（33个）
│   ├── test_curve.py                    # Curve 模块测试（54个）
│   ├── test_surface.py                  # Surface 模块测试（50个）
│   ├── test_geometry_utils.py           # 工具函数测试（31个）
│   ├── test_geometry.py                 # 集成测试
│   └── test_triangle_ellipse.py         # 三角形/椭圆测试
│
├── AGENTS.md                            # 项目设计文档
├── README.md                            # 项目说明文档
└── pyproject.toml                       # Python 包配置
```

### 4.2 模块化优势

| 优势 | 说明 |
|------|------|
| **单一职责** | 每个模块只负责一类几何元素 |
| **易于维护** | 代码分散在多个小文件中，每个文件清晰 |
| **快速导入** | 按需加载，可以只导入需要的模块 |
| **扩展性强** | 新增几何类只需在相应包中新增模块 |
| **Cython 友好** | 细粒度模块便于编译优化 |
| **向后兼容** | 保持顶级导入不变，现有代码无需修改 |

### 4.3 导入方式

**方式1: 顶级导入（推荐，向后兼容）**
```python
from planar_geometry import (
    Point2D, Vector2D,
    LineSegment, Line,
    Rectangle, Circle, Polygon, Triangle, Ellipse,
    line_segment_intersection,
    bounding_box,
    centroid
)
```

**方式2: 包级导入**
```python
from planar_geometry.point import Point2D
from planar_geometry.curve import Vector2D, LineSegment, Line
from planar_geometry.surface import Rectangle, Circle, Polygon, Triangle, Ellipse
from planar_geometry.utils import line_segment_intersection, bounding_box, centroid
```

**方式3: 细粒度导入**
```python
from planar_geometry.point.point2d import Point2D
from planar_geometry.curve.vector2d import Vector2D
from planar_geometry.surface.rectangle import Rectangle
from planar_geometry.utils.geometry_utils import line_segment_intersection
```



## 5. 测试统计

| 测试文件 | 测试数 | 状态 |
|---------|-------|------|
| test_point.py | 33 | ✅ 全部通过 |
| test_curve.py | 54 | ✅ 全部通过 |
| test_surface.py | 50 | ✅ 全部通过 |
| test_geometry_utils.py | 31 | ✅ 全部通过 |
| test_geometry.py | 29 | ✅ 全部通过 |
| test_triangle_ellipse.py | 34 | ✅ 全部通过 |
| **总计** | **231** | **✅ 231/231 通过** |

---

## 6. GitHub 仓库

- **仓库地址**: git@github.com:wangfaofao/planar_geometry.git
- **可见性**: Private
- **分支**: main

---

## 7. 开发进度

### 已完成功能

| 阶段 | 模块 | 功能数 | 测试数 | 状态 |
|------|------|-------|-------|------|
| 1 | measurable + point | 33 | 33 | ✅ 完成 |
| 2 | curve (Vector2D, LineSegment, Line) | 54 | 54 | ✅ 完成 |
| 3 | surface (Rectangle, Circle, Polygon) | 50+ | 50 | ✅ 完成 |
| 4 | geometry_utils (跨对象关系) | 20 | 31 | ✅ 完成 |
| 5 | Triangle + Ellipse | 25 | 34 | ✅ 完成 |
| 6 | 项目模块化重构 | - | 231 | ✅ 完成 |
| 7 | 修复导入问题 & 完善文档 | - | 231 | ✅ 完成 |

### 最新更新 (2026-01-31)

**模块化架构重构完成**
- ✅ 创建模块化目录结构（abstracts, point, curve, surface, utils 5个包）
- ✅ 修复所有导入问题，解决循环依赖
- ✅ 为每个包添加详细的中英文文档
- ✅ 所有 231 个单元测试通过
- ✅ 保持 100% 向后兼容（顶级导入方式不变）

**修复的问题**
- 创建缺失的 surface/__init__.py
- 修复 Triangle, Rectangle, Circle, Ellipse 的运行时导入
- 解决 Polygon 和 geometry_utils 之间的循环导入
- 修复 Line.get_intersection() 处理平行线的行为

### 下一步计划

1. **性能优化**:
   - 添加 Cython 编译配置
   - 性能基准测试
   - 优化热点代码

2. **功能扩展**:
   - 添加 Path（路径）类
   - 添加 Transform（2D变换）模块
   - 添加更多集何算法

3. **生态建设**:
   - 编写完整的 API 文档
   - 创建快速入门教程
   - 发布到 PyPI

---

## 8. 使用示例

### 基本使用

```python
from planar_geometry import Point2D, Vector2D, Rectangle, Circle, Polygon

# 创建点
p1 = Point2D(0, 0)
p2 = Point2D(3, 4)
distance = p1.distance_to(p2)  # 5.0

# 创建向量
v = Vector2D(3, 4)
v.length()  # 5.0
v.normalized()  # Vector2D(0.6, 0.8)

# 创建矩形
rect = Rectangle.from_center_and_size(
    center=Point2D(0, 0),
    size=2.0,
    direction=Vector2D(1, 0)
)
rect.area()      # 4.0
rect.perimeter() # 8.0

# 创建圆形
circle = Circle(Point2D(0, 0), 5.0)
circle.area()      # 78.54
circle.perimeter() # 31.42

# 创建多边形
poly = Polygon([
    Point2D(0, 0),
    Point2D(4, 0),
    Point2D(4, 3),
    Point2D(0, 3)
])
poly.area()       # 12.0
poly.perimeter()  # 14.0
poly.is_convex()  # True
```

### 几何运算

```python
from planar_geometry import (
    Point2D, LineSegment, Line, Vector2D,
    line_segment_intersection,
    point_to_segment_distance,
    angle_between,
    segments_distance,
    bounding_box,
    centroid
)

# 线段交点
s1 = LineSegment(Point2D(0, 0), Point2D(2, 2))
s2 = LineSegment(Point2D(0, 2), Point2D(2, 0))
intersection = line_segment_intersection(s1, s2)  # Point2D(1, 1)

# 点到线段距离
segment = LineSegment(Point2D(0, 0), Point2D(4, 0))
distance = point_to_segment_distance(Point2D(2, 3), segment)  # 3.0

# 向量夹角
v1 = Vector2D(1, 0)
v2 = Vector2D(0, 1)
angle = angle_between(v1, v2)  # 90.0

# 线段间距离
s1 = LineSegment(Point2D(0, 0), Point2D(2, 0))
s2 = LineSegment(Point2D(0, 2), Point2D(2, 2))
dist = segments_distance(s1, s2)  # 2.0

# 点集边界框
points = [Point2D(0, 0), Point2D(4, 3), Point2D(2, 5)]
bounds = bounding_box(points)  # (0, 0, 4, 5)

# 点集重心
center = centroid(points)  # Point2D(2.0, 2.67)
```

---

**文档更新**: 2026-01-31  
**项目状态**: 模块化架构完成，所有 231 个测试通过，生产就绪 ✅

