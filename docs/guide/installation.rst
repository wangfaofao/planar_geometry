Installation
=============

Requirements
============

- Python 3.10 or higher
- pip or another package manager

From PyPI
=========

::

    pip install planar-geometry

From Source
-----------

Clone the repository and install in development mode:

::

    git clone https://github.com/yourusername/planar_geometry.git
    cd planar_geometry
    pip install -e .

Installing Development Tools
-----------------------------

For development, testing, and documentation:

::

    pip install -r requirements-dev.txt
    pip install -r requirements-test.txt
    pip install -r requirements-docs.txt

Or install all at once:

::

    make install-all

Verifying Installation
----------------------

To verify that planar_geometry is installed correctly:

::

    python -c "import planar_geometry; print(planar_geometry.__version__)"

Or run a simple test:

::

    python -c "from planar_geometry.point import Point; p = Point(3, 4); print(p)"
