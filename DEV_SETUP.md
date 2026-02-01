# Development & CI/CD Setup Guide

This document describes the complete development, testing, and deployment infrastructure for the planar_geometry project.

## Quick Start

### Setup Development Environment

```bash
# Install all development dependencies
make install-all

# Or do it step by step
pip install -e .                    # Install package
pip install -r requirements-dev.txt # Dev tools (black, ruff, mypy, etc.)
pip install -r requirements-test.txt # Test tools (pytest)
pip install -r requirements-docs.txt # Docs tools (sphinx)

# Initialize pre-commit hooks
pre-commit install
```

### Run Common Tasks

```bash
# Run all tests
make test

# Format code
make format

# Run linters and type checkers
make lint
make type

# Build documentation
make docs

# Run all checks before committing
make check

# See all available tasks
make help
```

## Project Structure

```
planar_geometry/
├── .github/
│   ├── workflows/              # GitHub Actions CI/CD
│   │   ├── tests.yml          # Test on all Python versions
│   │   ├── quality.yml        # Code quality checks
│   │   └── build.yml          # Build distribution packages
│   ├── CODEOWNERS             # Code review assignments
│   ├── pull_request_template.md
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── docs/                       # Sphinx documentation
│   ├── conf.py
│   ├── index.rst
│   ├── guide/                 # User guides
│   ├── api/                   # API reference
│   └── dev/                   # Developer documentation
├── scripts/
│   └── bump_version.py        # Version management
├── src/planar_geometry/       # Source code
├── tests/                     # Unit tests
├── Dockerfile                 # Docker multi-stage build
├── docker-compose.yml         # Docker Compose services
├── .dockerignore              # Docker ignore file
├── .gitignore                 # Git ignore file
├── .pre-commit-config.yaml    # Pre-commit hooks
├── Makefile                   # Development tasks
├── tox.ini                    # Multi-version testing config
├── pyproject.toml             # Modern Python packaging
├── CHANGELOG.md               # Version history
└── AGENTS.md                  # Development guidelines
```

## CI/CD Workflows

### GitHub Actions

The project uses GitHub Actions for automated testing and building.

#### Tests Workflow (.github/workflows/tests.yml)

- **Trigger**: Push to main/develop, Pull requests
- **Matrix**: Python 3.10, 3.11, 3.12, 3.13
- **Tasks**:
  - Install dependencies
  - Run ruff linting
  - Type check with mypy and pyright
  - Format check with black
  - Run pytest with coverage
  - Run unittest
  - Upload coverage to codecov

#### Quality Workflow (.github/workflows/quality.yml)

- **Trigger**: Push to main/develop, Pull requests
- **Python**: 3.11 only
- **Tasks**:
  - Format check (black)
  - Linting (ruff)
  - Import ordering (isort)
  - Type checking (mypy, pyright)

#### Build Workflow (.github/workflows/build.yml)

- **Trigger**: Push to main, tags (v*)
- **Tasks**:
  - Build distribution (wheel + sdist)
  - Upload artifacts (30-day retention)

## Testing

### Local Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test file
pytest tests/test_point.py -v

# Run specific test class
pytest tests/test_point.py::TestPoint -v

# Run specific test method
pytest tests/test_point.py::TestPoint::test_distance -v
```

### Multi-Version Testing with tox

```bash
# Test on all supported Python versions
tox

# Test on specific version
tox -e py311

# Run linting
tox -e lint

# Run type checking
tox -e type

# Generate coverage report
tox -e coverage

# Build documentation
tox -e docs

# Development environment
tox -e dev
```

### Docker Testing

```bash
# Test on Python 3.10
docker-compose run test-py310

# Test on Python 3.11
docker-compose run test-py311

# Test on Python 3.12
docker-compose run test-py312

# Test on Python 3.13
docker-compose run test-py313

# Development container
docker-compose run dev

# Build Docker image
docker build -t planar_geometry:latest .

# Run Docker image
docker run -it planar_geometry:latest
```

## Code Quality

### Formatting with Black

```bash
# Check formatting
black --check src/ tests/

# Auto-format code
black src/ tests/

# Or use make
make format
```

### Linting with ruff

```bash
# Check code style
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### Type Checking

```bash
# Check with mypy
mypy src/planar_geometry --strict

# Check with pyright
pyright src/planar_geometry

# Or use make
make type
```

### Import Sorting

```bash
# Check import order
isort --check-only src/ tests/

# Auto-sort imports
isort src/ tests/
```

### Pre-commit Hooks

Pre-commit hooks automatically run checks before each commit:

```bash
# Install hooks (one time)
pre-commit install

# Run hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

Available hooks:
- Trailing whitespace trimming
- File ending fixes
- YAML/JSON/TOML validation
- Merge conflict detection
- Large file detection
- Code formatting (black, ruff)
- Import sorting (isort)
- Type checking (mypy, pyright)
- Unit tests (pytest)

## Documentation

### Building Documentation

```bash
# Build with sphinx
sphinx-build -W -b html docs docs/_build/html

# Build and serve locally
make serve-docs

# Then open http://localhost:8000 in browser

# Or use tox
tox -e docs
```

### Documentation Structure

- `docs/guide/installation.rst` - Installation instructions
- `docs/guide/quick_start.rst` - Quick start guide
- `docs/guide/basic_usage.rst` - Basic usage examples
- `docs/guide/advanced.rst` - Advanced features
- `docs/api/points.rst` - Points API reference
- `docs/api/vectors.rst` - Vectors API reference
- `docs/api/lines.rst` - Lines API reference
- `docs/api/circles.rst` - Circles API reference
- `docs/api/polygons.rst` - Polygons API reference
- `docs/dev/contributing.rst` - Contributing guidelines
- `docs/dev/architecture.rst` - Architecture documentation

### Sphinx Configuration

Located in `docs/conf.py`:
- Theme: sphinx_rtd_theme (Read the Docs)
- Extensions: autodoc, napoleon, sphinx_autodoc_typehints
- Auto-generates API docs from docstrings

## Version Management

### Bump Version

Use the version management script to bump versions:

```bash
# Show current version
python scripts/bump_version.py --current

# Bump patch version (0.2.0 → 0.2.1)
python scripts/bump_version.py patch

# Bump minor version (0.2.0 → 0.3.0)
python scripts/bump_version.py minor

# Bump major version (0.2.0 → 1.0.0)
python scripts/bump_version.py major

# Set specific version
python scripts/bump_version.py --set 1.0.0

# Don't create git tag
python scripts/bump_version.py patch --no-tag
```

The script:
- Updates version in `pyproject.toml`
- Updates version in `docs/conf.py`
- Creates git commit
- Creates annotated git tag
- Pushes tag to remote (if configured)

## Docker

### Multi-Stage Build

The Dockerfile uses multi-stage build:
1. **Builder stage**: Compiles the package
2. **Runtime stage**: Installs only the built package

Benefits:
- Minimal image size (Python 3.11-slim base)
- No build tools in final image
- Secure by default (non-root user)
- Health check included

### Usage

```bash
# Build image
docker build -t planar_geometry:latest .

# Run Python
docker run -it planar_geometry:latest

# Run interactive shell
docker run -it planar_geometry:latest bash

# Mount local code
docker run -it -v $(pwd):/app/project planar_geometry:latest

# Run tests in container
docker run -v $(pwd):/app/project planar_geometry:latest \
  python -m pytest /app/project/tests
```

### Docker Compose

Services defined in `docker-compose.yml`:
- `dev` - Development environment
- `test-py310` - Tests on Python 3.10
- `test-py311` - Tests on Python 3.11
- `test-py312` - Tests on Python 3.12
- `test-py313` - Tests on Python 3.13
- `docs` - Documentation builder

```bash
# Start development container
docker-compose run dev bash

# Run tests on all versions
docker-compose run test-py310
docker-compose run test-py311
docker-compose run test-py312
docker-compose run test-py313

# Build documentation
docker-compose run docs
```

## Makefile Commands

### Setup

- `make install` - Install package
- `make install-dev` - Install development tools
- `make install-test` - Install test tools
- `make install-docs` - Install documentation tools
- `make install-all` - Install everything
- `make dev` - Complete development setup

### Testing

- `make test` - Run all tests
- `make test-unit` - Run unit tests
- `make test-coverage` - Run with coverage report

### Quality

- `make lint` - Run linters
- `make format` - Auto-format code
- `make type` - Run type checkers
- `make check` - Run all checks (lint, type, test)

### Documentation

- `make docs` - Build documentation
- `make serve-docs` - Build and serve locally

### Build & Publish

- `make build` - Build distribution packages
- `make publish-test` - Publish to Test PyPI
- `make publish` - Publish to PyPI

### Maintenance

- `make clean` - Clean build artifacts
- `make all` - Full build and test

## tox Environments

- `py310` - Tests on Python 3.10
- `py311` - Tests on Python 3.11
- `py312` - Tests on Python 3.12
- `py313` - Tests on Python 3.13
- `lint` - Code style checks
- `format` - Auto-format code
- `type` - Type checking
- `coverage` - Coverage report
- `docs` - Build documentation
- `dev` - Development environment

## Contributing

### Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Set up development environment: `make dev`
4. Make changes and commit
5. Run checks: `make check`
6. Push and create a pull request

### Pre-Commit Checklist

- [ ] Tests pass: `make test`
- [ ] Code is formatted: `make format`
- [ ] Linting passes: `make lint`
- [ ] Type checking passes: `make type`
- [ ] Documentation builds: `make docs`

### Pull Request Process

1. Update CHANGELOG.md
2. Include test for new functionality
3. Update documentation if needed
4. Ensure all checks pass in CI/CD
5. Get code review approval
6. Squash commits if needed
7. Merge to main

## Troubleshooting

### Import Errors

If you get import errors, ensure the package is installed in development mode:

```bash
pip install -e .
```

### Pre-commit Hook Failures

To run pre-commit manually without committing:

```bash
pre-commit run --all-files
```

To skip pre-commit for a specific commit:

```bash
git commit --no-verify
```

### Docker Build Issues

Rebuild without cache:

```bash
docker build --no-cache -t planar_geometry:latest .
```

### tox Version Issues

Update tox:

```bash
pip install --upgrade tox
```

## Performance Tips

- Use `make` for common tasks (faster than typing full commands)
- Use Docker for consistent testing across versions
- Use pre-commit hooks to catch issues before CI/CD
- Run `make test-coverage` to identify untested code paths

## Resources

- [AGENTS.md](../AGENTS.md) - Development guidelines
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [pyproject.toml](../pyproject.toml) - Project configuration
- [Makefile](../Makefile) - Development tasks
- [tox.ini](../tox.ini) - Testing configuration
- [.pre-commit-config.yaml](../.pre-commit-config.yaml) - Pre-commit hooks
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Docker Documentation](https://docs.docker.com/)

---

**Last Updated**: 2026-02-01  
**Maintained by**: Contributors
