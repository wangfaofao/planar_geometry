# planar_geometry - 平面几何计算库

**版本**: 0.01  
**状态**: 开发中

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

### 3.1 measurable.py - 抽象基类模块

```python
class Measurable(ABC):
    """可计算度量根抽象类"""
    @abstractmethod
    def __repr__(self) -> str:
        pass

class Measurable1D(Measurable, ABC):
    """可计算长度抽象类"""
    @abstractmethod
    def length(self) -> float:
        pass

class Measurable2D(Measurable1D, ABC):
    """可计算面积抽象类"""
    @abstractmethod
    def area(self) -> float:
        pass
    
    def length(self) -> float:
        """二维图形的长度即周长"""
        return self.perimeter()
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
```

### 3.2 point.py - 点模块

```python
class Point2D(Measurable1D):
    """二维点类"""
    
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    # 度量接口
    def length(self) -> float:
        return 0.0
    
    # 距离计算
    def distance_to(self, other: 'Point2D') -> float:
        return math.sqrt(dx*dx + dy*dy)
    
    def distance_squared_to(self, other: 'Point2D') -> float:
        return dx*dx + dy*dy
    
    def midpoint_to(self, other: 'Point2D') -> 'Point2D':
        return Point2D((self.x + other.x) / 2, (self.y + other.y) / 2)
    
    # 算术运算
    def add(self, dx: float, dy: float) -> 'Point2D':
        return Point2D(self.x + dx, self.y + dy)
    
    def multiply(self, scalar: float) -> 'Point2D':
        return Point2D(self.x * scalar, self.y * scalar)
    
    def negate(self) -> 'Point2D':
        return Point2D(-self.x, -self.y)
    
    def equals(self, other: 'Point2D', tolerance: float = 1e-9) -> bool:
        return abs(self.x - other.x) < tolerance and abs(self.y - other.y) < tolerance
    
    def is_zero(self, tolerance: float = 1e-9) -> bool:
        return abs(self.x) < tolerance and abs(self.y) < tolerance
    
    # 转换方法
    def to_tuple(self) -> tuple:
        return (self.x, self.y)
    
    @staticmethod
    def from_tuple(data: tuple) -> 'Point2D':
        return Point2D(data[0], data[1])
    
    @staticmethod
    def origin() -> 'Point2D':
        return Point2D(0.0, 0.0)
    
    # 运算符重载
    def __add__(self, other: tuple) -> 'Point2D': ...
    def __sub__(self, other: 'Point2D') -> tuple: ...
    def __mul__(self, scalar: float) -> 'Point2D': ...
    def __rmul__(self, scalar: float) -> 'Point2D': ...
    def __truediv__(self, scalar: float) -> 'Point2D': ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self) -> str: ...
```

### 3.3 curve.py - 曲线模块

```python
class Curve(Measurable1D, ABC):
    """曲线抽象基类（一维几何元素）"""
    @abstractmethod
    def length(self) -> float:
        pass

class LineSegment(Curve):
    """线段类"""
    
    def __init__(self, start: Point2D, end: Point2D) -> None:
        self.start = start
        self.end = end
    
    def length(self) -> float:
        return self.start.distance_to(self.end)
    
    def midpoint(self) -> Point2D:
        return self.start.midpoint_to(self.end)
    
    def direction(self) -> Vector2D:
        """获取线段方向向量（归一化）"""
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        v = Vector2D(dx, dy)
        return v.normalized()
    
    def contains_point(self, point: Point2D, tolerance: float = 1e-9) -> bool:
        """判断点是否在线段上（含端点）"""
    
    def get_parameter(self, point: Point2D) -> float:
        """获取点在直线上的参数 t"""
    
    def get_closest_point(self, point: Point2D) -> Point2D:
        """获取线段上离给定点最近的点"""
    
    def get_distance_to_point(self, point: Point2D) -> float:
        """计算点到线段的最短距离"""

class Line(Curve):
    """直线类（无限延伸）"""
    
    def __init__(self, point: Point2D, direction: Vector2D) -> None:
        self.point = point
        self.direction = direction.normalized()
    
    def length(self) -> float:
        return float('inf')
    
    def get_intersection(self, other: 'Line') -> Point2D:
        """计算与另一条直线的交点"""
    
    def get_distance_to_point(self, point: Point2D) -> float:
        """计算点到直线的距离"""
    
    def get_closest_point(self, point: Point2D) -> Point2D:
        """获取直线上离给定点最近的点（垂足）"""
    
    def contains_point(self, point: Point2D, tolerance: float = 1e-9) -> bool:
        """判断点是否在直线上"""

class Vector2D(Curve):
    """二维向量类"""
    
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def length(self) -> float:
        return math.sqrt(self.x*self.x + self.y*self.y)
    
    def length_squared(self) -> float:
        return self.x*self.x + self.y*self.y
    
    def angle(self) -> float:
        """计算向量角度（度）[0, 360)"""
    
    def angle_rad(self) -> float:
        """计算向量角度（弧度）[0, 2π)"""
    
    def normalized(self) -> 'Vector2D':
        """返回归一化向量"""
    
    def dot(self, other: 'Vector2D') -> float:
        """点积"""
    
    def cross(self, other: 'Vector2D') -> float:
        """叉积（二维，标量）"""
    
    def perpendicular(self) -> 'Vector2D':
        """获取垂直向量（逆时针旋转90度）"""
    
    def rotated(self, angle_deg: float) -> 'Vector2D':
        """旋转向量"""
    
    def projection(self, other: 'Vector2D') -> 'Vector2D':
        """投影到另一向量"""
    
    def component(self, direction: 'Vector2D') -> float:
        """获取在指定方向上的分量（标量投影）"""
    
    def is_zero(self, tolerance: float = 1e-9) -> bool:
        return abs(self.x) < tolerance and abs(self.y) < tolerance
    
    def equals(self, other: 'Vector2D', tolerance: float = 1e-9) -> bool:
        return abs(self.x - other.x) < tolerance and abs(self.y - other.y) < tolerance
    
    @staticmethod
    def zero() -> 'Vector2D':
        return Vector2D(0, 0)
    
    @staticmethod
    def unit_x() -> 'Vector2D':
        return Vector2D(1, 0)
    
    @staticmethod
    def unit_y() -> 'Vector2D':
        return Vector2D(0, 1)
```

### 3.4 surface.py - 曲面模块

```python
class Surface(Measurable2D, ABC):
    """曲面/平面图形抽象基类"""
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass

class Rectangle(Surface):
    """矩形类"""
    
    def __init__(self, vertices: List[Point2D]) -> None:
        if len(vertices) != 4:
            raise ValueError("矩形必须有4个顶点")
        self.vertices = vertices
    
    @staticmethod
    def from_center_and_size(center: Point2D, size: float, direction: Vector2D) -> 'Rectangle':
        """工厂方法：从中心点创建矩形"""
    
    @staticmethod
    def from_bounds(x_min: float, y_min: float, x_max: float, y_max: float) -> 'Rectangle':
        """工厂方法：从边界框创建矩形"""
    
    def area(self) -> float:
        return width * height
    
    def perimeter(self) -> float:
        return 2.0 * (width + height)
    
    def get_bounds(self) -> tuple:
        """获取轴对齐边界框 (AABB)"""
    
    def get_edges(self) -> List[tuple]:
        """获取4条边"""
    
    def get_edge_count(self) -> int:
        return 4
    
    def get_vertex_count(self) -> int:
        return 4
    
    def get_center(self) -> Point2D:
        """获取矩形中心点"""
    
    def contains_point(self, point: Point2D) -> bool:
        """判断点是否在矩形内或边界上"""
    
    def is_square(self, tolerance: float = 1e-6) -> bool:
        """判断是否为正方形"""

class Circle(Surface):
    """圆形类"""
    
    def __init__(self, center: Point2D, radius: float) -> None:
        if radius < 0:
            raise ValueError("半径不能为负数")
        self.center = center
        self.radius = radius
    
    @staticmethod
    def from_diameter(p1: Point2D, p2: Point2D) -> 'Circle':
        """工厂方法：从直径创建圆形"""
    
    def area(self) -> float:
        return math.pi * self.radius * self.radius
    
    def perimeter(self) -> float:
        return 2.0 * math.pi * self.radius
    
    def get_bounds(self) -> tuple:
        return (center.x - radius, center.y - radius, center.x + radius, center.y + radius)
    
    def get_center(self) -> Point2D:
        return self.center
    
    def contains_point(self, point: Point2D) -> bool:
        """判断点是否在圆内或圆上"""
    
    def get_circumference(self) -> float:
        """获取圆周长（别名）"""
    
    def equals(self, other: 'Circle', tolerance: float = 1e-6) -> bool:
        """判断与另一圆是否相等"""

class Polygon(Surface):
    """多边形类"""
    
    def __init__(self, vertices: List[Point2D]) -> None:
        if len(vertices) < 3:
            raise ValueError("多边形至少有3个顶点")
        self.vertices = vertices
    
    @staticmethod
    def from_points(points: List[Point2D]) -> 'Polygon':
        """工厂方法：从点列表创建"""
    
    @staticmethod
    def regular(n: int, center: Point2D, radius: float, rotation: float = 0.0) -> 'Polygon':
        """工厂方法：创建正多边形"""
    
    @staticmethod
    def triangle(p1: Point2D, p2: Point2D, p3: Point2D) -> 'Polygon':
        """工厂方法：从三个点创建三角形"""
    
    @staticmethod
    def rectangle(p1: Point2D, p2: Point2D, p3: Point2D, p4: Point2D) -> 'Polygon':
        """工厂方法：从四个点创建四边形"""
    
    def area(self) -> float:
        """鞋带公式计算面积"""
    
    def perimeter(self) -> float:
        """计算周长"""
    
    def get_bounds(self) -> tuple:
        """获取轴对齐边界框 (AABB)"""
    
    def get_center(self) -> Point2D:
        """获取多边形中心（重心）"""
    
    def centroid(self) -> Point2D:
        """获取多边形质心"""
    
    def get_edges(self) -> List[tuple]:
        """获取所有边"""
    
    def get_edge_count(self) -> int:
        return len(self.vertices)
    
    def get_vertex_count(self) -> int:
        return len(self.vertices)
    
    def get_vertex(self, index: int) -> Point2D:
        """获取指定索引的顶点"""
    
    def get_edge(self, index: int) -> tuple:
        """获取指定索引的边"""
    
    def contains_point(self, point: Point2D) -> bool:
        """射线投射算法判断点是否在多边形内"""
    
    def is_convex(self) -> bool:
        """判断是否为凸多边形"""
    
    def is_simple(self) -> bool:
        """判断是否为简单多边形（不自交）"""
    
    def is_regular(self) -> bool:
        """判断是否为正多边形"""
    
    def get_convex_hull(self) -> 'Polygon':
        """Graham Scan 算法计算凸包"""
```

### 3.5 geometry_utils.py - 工具函数模块

```python
# 线段交点
def line_segment_intersection(s1: LineSegment, s2: LineSegment, tolerance: float = 1e-9) -> Optional[Point2D]:
    """计算两条线段的交点"""

# 直线交点
def line_intersection(l1: Line, l2: Line, tolerance: float = 1e-9) -> Optional[Point2D]:
    """计算两条直线的交点"""

# 矩形交点
def rectangle_intersection_points(r1: Rectangle, r2: Rectangle, tolerance: float = 1e-6) -> List[Point2D]:
    """计算两个矩形边界的所有交点"""

# 多边形交点
def polygon_intersection_points(poly1: Polygon, poly2: Polygon, tolerance: float = 1e-6) -> List[Point2D]:
    """计算两个多边形边界的所有交点"""

# 点到线距离
def point_to_segment_distance(point: Point2D, segment: LineSegment) -> float:
    """计算点到线段的最短距离"""

def point_to_segment_closest_point(point: Point2D, segment: LineSegment) -> Point2D:
    """计算线段上离给定点最近的点"""

def point_to_line_distance(point: Point2D, line: Line) -> float:
    """计算点到直线的距离"""

def point_to_line_closest_point(point: Point2D, line: Line) -> Point2D:
    """计算直线上离给定点最近的点（垂足）"""

# 点到面距离
def point_to_rectangle_distance(point: Point2D, rect: Rectangle) -> float:
    """计算点到矩形的最短距离"""

def point_to_polygon_distance(point: Point2D, poly: Polygon) -> float:
    """计算点到多边形的最短距离"""

# 向量角度
def angle_between(v1: Vector2D, v2: Vector2D) -> float:
    """计算两个向量之间的夹角（度）"""

def angle_between_rad(v1: Vector2D, v2: Vector2D) -> float:
    """计算两个向量之间的夹角（弧度）"""

def are_perpendicular(v1: Vector2D, v2: Vector2D, tolerance: float = 1e-6) -> bool:
    """判断两个向量是否垂直"""

def are_parallel(v1: Vector2D, v2: Vector2D, tolerance: float = 1e-6) -> bool:
    """判断两个向量是否平行"""

# 线段距离
def segments_distance(s1: LineSegment, s2: LineSegment) -> float:
    """计算两条线段之间的最短距离"""

def segments_closest_points(s1: LineSegment, s2: LineSegment) -> Tuple[Point2D, Point2D]:
    """计算两条线段之间的最近点对"""

# 点集工具
def bounding_box(points: List[Point2D]) -> Tuple[float, float, float, float]:
    """计算点集的轴对齐边界框"""

def centroid(points: List[Point2D]) -> Point2D:
    """计算点集的重心"""
```

---

## 4. 项目结构

```
planar_geometry/
├── src/planar_geometry/
│   ├── __init__.py              # 模块导出（27个导出项）
│   ├── measurable.py            # 抽象基类（3个类）
│   ├── point.py                 # Point2D（33个方法）
│   ├── curve.py                 # Curve, LineSegment, Line, Vector2D（54个方法）
│   ├── surface.py               # Surface, Rectangle, Circle, Polygon（50+方法）
│   └── geometry_utils.py        # 独立函数（20个函数）
├── tests/
│   ├── test_point.py            # 33个测试
│   ├── test_curve.py            # 54个测试
│   ├── test_surface.py          # 50个测试
│   └── test_geometry_utils.py   # 31个测试
├── AGENTS.md                    # 设计文档
├── README.md                    # 项目说明
└── pyproject.toml               # Python包配置
```

---

## 5. 测试统计

| 测试文件 | 测试数 | 状态 |
|---------|-------|------|
| test_point.py | 33 | ✅ 全部通过 |
| test_curve.py | 54 | ✅ 全部通过 |
| test_surface.py | 50 | ✅ 全部通过 |
| test_geometry_utils.py | 31 | ✅ 全部通过 |
| **总计** | **187** | **✅ 187/187 通过** |

---

## 6. GitHub 仓库

- **仓库地址**: git@github.com:wangfaofao/planar_geometry.git
- **可见性**: Private
- **分支**: main

---

## 7. 开发进度

### 已完成功能

| 阶段 | 模块 | 功能数 | 测试数 |
|------|------|-------|-------|
| 1 | measurable + point | 33 | 33 |
| 2 | curve (Vector2D, LineSegment, Line) | 54 | 54 |
| 3 | surface (Rectangle, Circle, Polygon) | 50+ | 50 |
| 4 | geometry_utils (跨对象关系) | 20 | 31 |

### 下一步计划

1. **第五阶段**: 更新 AGENTS.md 文档
2. **后续扩展**:
   - 添加 Triangle（三角形）类
   - 添加 Ellipse（椭圆）类
   - 添加 Path（路径）类
   - 添加 Transform（2D变换）模块
   - Cython 性能优化

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

**文档更新**: 2026-01-30  
**下一步**: 继续添加更多几何元素和优化性能
