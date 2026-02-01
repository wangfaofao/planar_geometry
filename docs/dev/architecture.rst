Architecture
=============

Project Structure
-----------------

::

    planar_geometry/
    ├── src/planar_geometry/       # Source code
    │   ├── __init__.py
    │   ├── point.py               # Point class
    │   ├── vector.py              # Vector class
    │   ├── line.py                # Line class
    │   ├── circle.py              # Circle class
    │   ├── polygon.py             # Polygon class
    │   └── ...
    ├── tests/                     # Unit tests
    ├── docs/                      # Documentation
    ├── pyproject.toml             # Project metadata
    ├── Makefile                   # Development tasks
    ├── tox.ini                    # Testing configuration
    └── ...

Design Principles
-----------------

SOLID Principles
~~~~~~~~~~~~~~~~

The planar_geometry library follows SOLID principles:

**Single Responsibility**
- Each class has one reason to change
- Point handles point operations
- Vector handles vector operations
- etc.

**Open/Closed**
- Open for extension via inheritance
- Closed for modification of existing code
- New geometric shapes can extend base classes

**Liskov Substitution**
- Derived classes can substitute base classes
- Consistent interface across all geometric objects

**Interface Segregation**
- Clients depend only on interfaces they use
- Each class provides focused, cohesive methods

**Dependency Inversion**
- Depend on abstractions, not concrete classes
- Use abstract base classes where appropriate

Core Concepts
-------------

Basic Types
~~~~~~~~~~~

**Point**
- Represents a location in 2D space (x, y)
- Immutable value object
- Supports distance calculations

**Vector**
- Represents direction and magnitude
- Supports arithmetic operations
- Can be rotated, scaled, normalized

**Line**
- Represents an infinite line through two points
- Supports intersection tests
- Can contain points

**Circle**
- Represents a circle with center and radius
- Supports containment and distance tests
- Can intersect with other circles

**Polygon**
- Represents a closed shape with vertices
- Supports area and perimeter calculations
- Can contain points and check convexity

Mathematical Operations
~~~~~~~~~~~~~~~~~~~~~~~

Distance calculations use the Euclidean distance formula:

::

    distance = sqrt((x2 - x1)² + (y2 - y1)²)

Area calculations use standard formulas:

- Triangle: Shoelace formula
- Polygon: Shoelace formula
- Circle: πr²

Intersection detection uses geometric algorithms:

- Line-line: Parametric form intersection
- Circle-circle: Distance-based intersection
- Point-in-polygon: Ray casting algorithm

Zero Dependencies Philosophy
-----------------------------

planar_geometry intentionally has zero external dependencies:

- Uses only Python standard library
- Improves reliability and maintainability
- Reduces installation size
- Simplifies dependency management

This is achieved by:

- Using pure Python implementations
- Focusing on geometric fundamentals
- Avoiding matrix libraries (numpy)
- Not using plotting libraries (matplotlib)

Performance Considerations
--------------------------

For better performance:

- Avoid repeated distance calculations
- Cache expensive computations
- Use appropriate data structures
- Consider using Cython for critical paths (future)

Testing Strategy
----------------

- Unit tests for all public methods
- Edge case coverage
- Integration tests for complex operations
- 100% code coverage target

See :doc:`contributing` for testing details.
