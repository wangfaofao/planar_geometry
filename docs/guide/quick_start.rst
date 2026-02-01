Quick Start
===========

Basic Usage
-----------

Creating Points
~~~~~~~~~~~~~~~

::

    from planar_geometry.point import Point
    
    # Create points
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    
    print(f"Point: {p1}")
    print(f"Distance: {p1.distance_to(p2)}")

Working with Vectors
~~~~~~~~~~~~~~~~~~~~~

::

    from planar_geometry.vector import Vector
    
    # Create vectors
    v1 = Vector(1, 0)
    v2 = Vector(0, 1)
    
    # Vector operations
    v3 = v1 + v2
    dot_product = v1.dot(v2)
    magnitude = v1.magnitude()

Lines and Circles
~~~~~~~~~~~~~~~~~

::

    from planar_geometry.line import Line
    from planar_geometry.circle import Circle
    from planar_geometry.point import Point
    
    # Create a line
    line = Line(Point(0, 0), Point(1, 1))
    
    # Create a circle
    circle = Circle(center=Point(0, 0), radius=5)
    
    # Check if point is on circle
    point = Point(3, 4)
    is_on_circle = circle.contains_point(point)

Next Steps
----------

- :doc:`basic_usage` - More detailed examples
- :doc:`advanced` - Advanced geometric operations
- :doc:`../api/points` - Complete API reference for Points
