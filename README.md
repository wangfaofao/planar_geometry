# planar_geometry

A planar geometry library with SOLID principles, designed for Cython optimization.

## Installation

```bash
cd ~/Desktop/planar_geometry
pip install -e .
```

## Usage

```python
from planar_geometry import Point2D, Vector2D, Rectangle

# Create points
p1 = Point2D(0, 0)
p2 = Point2D(3, 4)

# Calculate distance
distance = p1.distance_to(p2)  # 5.0

# Create vector
v = Vector2D(3, 4)
print(v.length())  # 5.0

# Create rectangle
rect = Rectangle.from_center_and_size(
    center=Point2D(0, 0),
    size=2.0,
    direction=Vector2D(1, 0)
)
print(rect.area())      # 4.0
print(rect.perimeter()) # 8.0
```

## Development

```bash
# Run tests
pytest tests/

# Format code
black src/ tests/
```

## License

MIT
