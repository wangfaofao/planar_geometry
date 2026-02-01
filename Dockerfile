# Multi-stage build for planar_geometry

# Build stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md /build/
COPY src/ /build/src/
COPY tests/ /build/tests/

# Build the package
RUN pip install --upgrade pip setuptools wheel && \
    python -m build

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user
RUN useradd -m -u 1000 planar

# Copy built package from builder
COPY --from=builder /build/dist/ /tmp/dist/

# Install the package
RUN pip install --upgrade pip && \
    pip install /tmp/dist/planar_geometry-*.whl && \
    rm -rf /tmp/dist/

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import planar_geometry; print('OK')" || exit 1

# Switch to non-root user
USER planar

# Metadata
LABEL maintainer="Contributors <dev@planar_geometry.local>"
LABEL description="Pure Python 2D geometry library"
LABEL version="0.2.0"

# Default command
CMD ["python"]
