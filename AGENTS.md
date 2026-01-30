# planar_geometry - 平面几何计算库

**版本**: 0.1.0  
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
        ├── Circle (圆形 - 接口预留)
        │   * area() 返回 πr²
        │   * perimeter() 返回 2πr
        │
        └── Polygon (多边形 - 接口预留)
            * area() 返回多边形面积
            * perimeter() 返回多边形周长
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
# 可计算度量根抽象类
class Measurable(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

# 可计算长度抽象类
class Measurable1D(Measurable, ABC):
    @abstractmethod
    def length(self) -> float:
        pass

# 可计算面积抽象类
class Measurable2D(Measurable1D, ABC):
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
    
    def length(self) -> float:
        return 0.0
    
    def distance_to(self, other: 'Point2D') -> float:
        """计算到另一个点的欧几里得距离"""
    
    def __add__(self, other: tuple) -> 'Point2D':
        """点 + (x, y) = 新点"""
    
    def __sub__(self, other: 'Point2D') -> tuple:
        """点 - 点 = (x, y)"""
    
    def __mul__(self, scalar: float) -> 'Point2D':
        """点 * 标量 = 新点"""
```

### 3.3 curve.py - 曲线模块

```python
class Curve(Measurable1D, ABC):
    """曲线抽象基类"""
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
        """获取线段中点"""

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

class Vector2D(Curve):
    """二维向量类"""
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def angle(self) -> float:
        """计算向量角度（度）"""
    
    def normalized(self) -> 'Vector2D':
        """返回归一化向量"""
    
    def dot(self, other: 'Vector2D') -> float:
        """点积"""
    
    def cross(self, other: 'Vector2D') -> float:
        """叉积（二维，标量）"""
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
    def from_center_and_size(
        center: Point2D,
        size: float,
        direction: Vector2D
    ) -> 'Rectangle':
        """工厂方法：从中心点创建矩形"""
    
    def area(self) -> float:
        return width * height
    
    def perimeter(self) -> float:
        return 2.0 * (width + height)
    
    def get_bounds(self) -> tuple:
        """获取轴对齐边界框 (AABB)"""
    
    def get_edges(self) -> List[tuple]:
        """获取4条边"""
    
    def get_center(self) -> Point2D:
        """获取矩形中心点"""
    
    def contains_point(self, point: Point2D) -> bool:
        """判断点是否在矩形内或边界上"""

class Circle(Surface):
    """圆形类（接口预留）"""
    def __init__(self, center: Point2D, radius: float) -> None:
        pass

class Polygon(Surface):
    """多边形类（接口预留）"""
    def __init__(self, vertices: List[Point2D]) -> None:
        pass
```

### 3.5 geometry_utils.py - 工具函数模块

```python
def line_segment_intersection(
    s1: LineSegment,
    s2: LineSegment,
    tolerance: float = 1e-9
) -> Optional[Point2D]:
    """计算两条线段的交点"""

def line_intersection(
    l1: Line,
    l2: Line,
    tolerance: float = 1e-9
) -> Optional[Point2D]:
    """计算两条直线的交点"""

def rectangle_intersection_points(
    r1: Rectangle,
    r2: Rectangle,
    tolerance: float = 1e-6
) -> List[Point2D]:
    """计算两个矩形边界的所有交点"""
```

---

## 4. Cython 改造规范

### 4.1 基本数据类型约定

| Python 类型 | Cython 等价 | 使用场景 |
|-------------|-------------|---------|
| `float` | `double` | 坐标、长度、面积 |
| `tuple` | `tuple` 或结构体 | 坐标对 (x, y) |

### 4.2 设计约束

1. **避免复杂 Python 类型作为参数**
   - 优先使用 `float` 而非 `List[float]`
   - 优先使用 `tuple` 而非 `List[Point2D]`（如需性能）

2. **直接暴露属性**
   - 使用 `point.x` 而非 `point.get_x()`
   - 便于 Cython 直接访问

3. **减少抽象层开销**
   - 抽象基类在 Cython 中仍有开销
   - 核心计算路径尽量使用具体类

---

## 5. 项目结构

```
planar_geometry/
├── src/planar_geometry/
│   ├── __init__.py              # 模块导出
│   ├── measurable.py            # 抽象基类
│   ├── point.py                 # Point2D
│   ├── curve.py                 # Curve, LineSegment, Line, Vector2D
│   ├── surface.py               # Surface, Rectangle, Circle, Polygon
│   └── geometry_utils.py        # 独立函数
├── tests/
│   └── test_*.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 6. 开发规范

### 6.1 代码风格

- **行长度**: 100 字符
- **缩进**: 4 空格
- **编码**: UTF-8

### 6.2 测试要求

- 每个模块需有对应的测试文件
- 使用 `unittest` 框架
- 覆盖核心功能和边界情况

### 6.3 提交规范

```
feat: 添加新功能
fix: 修复bug
refactor: 重构代码
docs: 更新文档
test: 添加测试
chore: 其他修改
```

---

## 7. 后续扩展

### 7.1 计划添加的几何元素

- **Triangle**: 三角形类
- **Ellipse**: 椭圆类
- **Path**: 路径类（多段线）
- **Transform**: 2D 变换（平移、旋转、缩放）

### 7.2 性能优化

- 使用 `cdef class` 重写核心类
- 添加 `nogil` 区域用于并行计算
- 使用内存视图优化数组操作

---

## 8. 使用示例

### 基本使用

```python
from planar_geometry import Point2D, Vector2D, Rectangle

# 创建点
p1 = Point2D(0, 0)
p2 = Point2D(3, 4)

# 计算距离
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
```

### 几何运算

```python
from planar_geometry import (
    Point2D, LineSegment, Line,
    line_segment_intersection, line_intersection
)

# 线段交点
s1 = LineSegment(Point2D(0, 0), Point2D(2, 2))
s2 = LineSegment(Point2D(0, 2), Point2D(2, 0))
intersection = line_segment_intersection(s1, s2)  # Point2D(1, 1)

# 直线交点
l1 = Line(Point2D(0, 0), Vector2D(1, 1))
l2 = Line(Point2D(0, 2), Vector2D(1, -1))
intersection = line_intersection(l1, l2)  # Point2D(1, 1)
```

---

**文档完成**  
**下一步**: 编写单元测试，完善各模块实现
