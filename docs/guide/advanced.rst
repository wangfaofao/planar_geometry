Advanced Usage
==============

Geometric Transformations
--------------------------

Rotation
~~~~~~~~

::

    from planar_geometry.point import Point
    from planar_geometry.vector import Vector
    from math import pi
    
    # Rotate a vector
    v = Vector(1, 0)
    rotated = v.rotate(pi / 4)  # Rotate 45 degrees
    
    # Rotate a point around origin
    p = Point(1, 0)
    # Use vector representation
    v = Vector(p.x, p.y)
    rotated_v = v.rotate(pi / 4)
    rotated_p = Point(rotated_v.x, rotated_v.y)

Reflection
~~~~~~~~~~

::

    from planar_geometry.line import Line
    from planar_geometry.point import Point
    
    # Reflect a point across a line
    line = Line(Point(0, 0), Point(1, 0))  # x-axis
    point = Point(1, 1)
    reflected = point.reflect_across(line)

Composition of Operations
--------------------------

Working with Multiple Geometric Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from planar_geometry.point import Point
    from planar_geometry.polygon import Polygon
    from planar_geometry.circle import Circle
    
    # Create complex shapes
    triangle = Polygon([
        Point(0, 0),
        Point(4, 0),
        Point(2, 3)
    ])
    
    # Find relationships
    center = triangle.centroid()
    circle = Circle(center, radius=5)
    
    # Check intersections
    for vertex in triangle.vertices:
        if not circle.contains_point(vertex):
            print(f"Vertex {vertex} is outside circle")

Intersection Detection
----------------------

Line Intersections
~~~~~~~~~~~~~~~~~~~

::

    from planar_geometry.line import Line
    from planar_geometry.point import Point
    
    line1 = Line(Point(0, 0), Point(2, 2))
    line2 = Line(Point(0, 2), Point(2, 0))
    
    intersection = line1.intersection(line2)
    if intersection:
        print(f"Lines intersect at: {intersection}")
    else:
        print("Lines are parallel")

Circle Intersections
~~~~~~~~~~~~~~~~~~~~~

::

    from planar_geometry.circle import Circle
    from planar_geometry.point import Point
    
    circle1 = Circle(Point(0, 0), 5)
    circle2 = Circle(Point(6, 0), 5)
    
    intersections = circle1.intersection(circle2)
    for point in intersections:
        print(f"Intersection point: {point}")

Polygon Operations
------------------

Advanced Polygon Methods
~~~~~~~~~~~~~~~~~~~~~~~~

::

    from planar_geometry.polygon import Polygon
    from planar_geometry.point import Point
    
    # Create a quadrilateral
    quad = Polygon([
        Point(0, 0),
        Point(4, 0),
        Point(4, 3),
        Point(0, 3)
    ])
    
    # Check if polygon is convex
    is_convex = quad.is_convex()
    
    # Get centroid
    centroid = quad.centroid()
    
    # Calculate area
    area = quad.area()
    
    # Perimeter
    perimeter = quad.perimeter()
