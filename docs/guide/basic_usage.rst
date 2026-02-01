Basic Usage
===========

This guide covers the fundamental operations with planar_geometry.

Points
------

Creating and Using Points
~~~~~~~~~~~~~~~~~~~~~~~~~~

Points are the basic building blocks. They represent locations in 2D space.

::

    from planar_geometry.point import Point
    
    # Create points
    origin = Point(0, 0)
    p1 = Point(3, 4)
    p2 = Point(1, 2)
    
    # Access coordinates
    x, y = p1.x, p1.y
    
    # Distance between points
    dist = p1.distance_to(p2)
    print(f"Distance: {dist}")
    
    # Midpoint
    mid = p1.midpoint_to(p2)
    print(f"Midpoint: {mid}")

Vectors
-------

Vector Operations
~~~~~~~~~~~~~~~~~

Vectors represent directions and magnitudes.

::

    from planar_geometry.vector import Vector
    from planar_geometry.point import Point
    
    # Create vectors
    v1 = Vector(1, 0)  # Unit vector in x direction
    v2 = Vector(0, 1)  # Unit vector in y direction
    
    # Vector arithmetic
    v3 = v1 + v2  # Addition
    v4 = v1.scale(2)  # Scaling
    
    # Dot product
    dot = v1.dot(v2)  # Perpendicular vectors have dot product = 0
    
    # Magnitude
    mag = v1.magnitude()  # Length of vector
    
    # Normalization
    normalized = v1.normalize()

Lines
-----

Working with Lines
~~~~~~~~~~~~~~~~~~~

::

    from planar_geometry.line import Line
    from planar_geometry.point import Point
    
    # Create a line from two points
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    line = Line(p1, p2)
    
    # Check if point is on line
    p3 = Point(1.5, 2)
    if line.contains_point(p3):
        print("Point is on the line")
    
    # Find intersection with another line
    line2 = Line(Point(0, 4), Point(4, 0))
    intersection = line.intersection(line2)
    print(f"Intersection: {intersection}")

Circles
-------

Circle Operations
~~~~~~~~~~~~~~~~~

::

    from planar_geometry.circle import Circle
    from planar_geometry.point import Point
    
    # Create a circle
    center = Point(0, 0)
    circle = Circle(center, radius=5)
    
    # Check if point is inside, on, or outside circle
    p1 = Point(3, 4)  # On the circle (distance = 5)
    p2 = Point(2, 2)  # Inside the circle
    p3 = Point(10, 0)  # Outside the circle
    
    print(f"p1 on circle: {circle.contains_point(p1)}")
    print(f"Area: {circle.area()}")
    print(f"Circumference: {circle.circumference()}")

Polygons
--------

Working with Polygons
~~~~~~~~~~~~~~~~~~~~~

::

    from planar_geometry.polygon import Polygon
    from planar_geometry.point import Point
    
    # Create a triangle
    vertices = [
        Point(0, 0),
        Point(3, 0),
        Point(3, 4)
    ]
    triangle = Polygon(vertices)
    
    # Basic properties
    print(f"Perimeter: {triangle.perimeter()}")
    print(f"Area: {triangle.area()}")
    
    # Check if point is inside
    p = Point(1, 1)
    if triangle.contains_point(p):
        print("Point is inside the polygon")
