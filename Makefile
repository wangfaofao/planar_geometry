.PHONY: help install install-dev install-test install-docs install-all \
        test test-unit test-coverage lint format type docs clean build \
        pre-commit pre-commit-install pre-commit-run dev serve-docs \
        publish publish-test check all

# Default target
help:
	@echo "planar_geometry development tasks"
	@echo ""
	@echo "Setup:"
	@echo "  make install              Install package in production mode"
	@echo "  make install-dev          Install development tools"
	@echo "  make install-test         Install testing tools"
	@echo "  make install-docs         Install documentation tools"
	@echo "  make install-all          Install everything (dev + test + docs)"
	@echo ""
	@echo "Development:"
	@echo "  make dev                  Set up development environment"
	@echo "  make pre-commit-install   Set up pre-commit hooks"
	@echo "  make pre-commit-run       Run pre-commit on all files"
	@echo ""
	@echo "Testing:"
	@echo "  make test                 Run all tests (pytest + unittest)"
	@echo "  make test-unit            Run only unit tests"
	@echo "  make test-coverage        Run tests with coverage report"
	@echo ""
	@echo "Quality:"
	@echo "  make lint                 Run all linters (black, ruff, isort)"
	@echo "  make format               Auto-format code"
	@echo "  make type                 Run type checkers (mypy, pyright)"
	@echo "  make check                Run all checks (lint, type, test)"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs                 Build Sphinx documentation"
	@echo "  make serve-docs           Serve docs locally (requires http.server)"
	@echo ""
	@echo "Build & Publish:"
	@echo "  make build                Build distribution packages"
	@echo "  make publish-test         Publish to test PyPI"
	@echo "  make publish              Publish to PyPI"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean                Clean build artifacts and caches"
	@echo "  make all                  Run all checks, tests, and build"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt

install-test:
	pip install -r requirements-test.txt

install-docs:
	pip install -r requirements-docs.txt

install-all: install install-dev install-test install-docs
	@echo "✓ All dependencies installed"

dev: install-all pre-commit-install
	@echo "✓ Development environment ready"
	@echo "Next steps:"
	@echo "  1. Run 'make pre-commit-run' to format all files"
	@echo "  2. Use 'make test' to run tests"
	@echo "  3. Use 'make check' to run all quality checks"

# Pre-commit hooks
pre-commit-install:
	pre-commit install
	@echo "✓ Pre-commit hooks installed"

pre-commit-run:
	pre-commit run --all-files
	@echo "✓ Pre-commit checks completed"

# Testing targets
test: test-unit
	@echo "✓ All tests passed"

test-unit:
	pytest tests/ -v --tb=short
	python -m unittest discover tests/ -v

test-coverage:
	pytest tests/ -v --cov=src/planar_geometry --cov-report=term-missing --cov-report=html --cov-report=xml
	@echo "✓ Coverage report generated in htmlcov/index.html"

# Quality targets
lint:
	black --check src/ tests/
	ruff check src/ tests/
	isort --check-only src/ tests/
	@echo "✓ All linting checks passed"

format:
	black src/ tests/
	isort src/ tests/
	ruff check --fix src/ tests/
	@echo "✓ Code formatted"

type:
	mypy src/planar_geometry --strict
	pyright src/planar_geometry
	@echo "✓ Type checking passed"

check: lint type test
	@echo "✓ All checks passed"

# Documentation targets
docs:
	sphinx-build -W -b html -d docs/_build/doctrees docs docs/_build/html
	@echo "✓ Documentation built in docs/_build/html"

serve-docs: docs
	cd docs/_build/html && python -m http.server 8000
	@echo "Serving docs at http://localhost:8000"

# Build & Publish targets
build: clean
	python -m build
	@echo "✓ Build complete. Artifacts in dist/"
	ls -lh dist/

publish-test: build
	python -m twine upload --repository testpypi dist/*
	@echo "✓ Published to Test PyPI"

publish: build
	python -m twine upload dist/*
	@echo "✓ Published to PyPI"

# Maintenance targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf docs/_build/
	@echo "✓ Cleaned build artifacts and caches"

all: clean check build docs
	@echo "✓ Complete build successful"
