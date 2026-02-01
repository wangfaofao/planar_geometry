Contributing
=============

We welcome contributions to planar_geometry! This guide will help you get started.

Development Setup
-----------------

1. Fork the repository on GitHub
2. Clone your fork locally:

::

    git clone https://github.com/yourusername/planar_geometry.git
    cd planar_geometry

3. Set up development environment:

::

    make dev

This will:
- Install the package in development mode
- Install all development tools
- Set up pre-commit hooks

Running Tests
-------------

Run all tests:

::

    make test

Run with coverage:

::

    make test-coverage

Run specific test file:

::

    pytest tests/test_point.py -v

Code Quality
------------

Format your code:

::

    make format

Run linters:

::

    make lint

Type checking:

::

    make type

Or run all checks:

::

    make check

Pre-commit Hooks
----------------

Pre-commit hooks automatically run checks before each commit:

::

    make pre-commit-install
    make pre-commit-run  # Run on all files

Submitting Changes
------------------

1. Create a new branch for your changes:

::

    git checkout -b feature/your-feature-name

2. Make your changes and commit them:

::

    git commit -m "Add your commit message"

3. Push to your fork:

::

    git push origin feature/your-feature-name

4. Create a Pull Request on GitHub

Coding Standards
----------------

- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for all public functions
- Maintain 100% test coverage for new code
- Use black for formatting
- Use ruff for linting

Documentation
-------------

Build documentation locally:

::

    make docs

View documentation:

::

    make serve-docs

Open http://localhost:8000 in your browser.

Release Process
---------------

1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Create a git tag:

::

    git tag -a v0.3.0 -m "Version 0.3.0"

4. Push tag to GitHub:

::

    git push origin v0.3.0

5. Publish to PyPI:

::

    make publish
