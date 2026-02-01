#!/usr/bin/env python3
"""
Version management script for planar_geometry.

Usage:
    python scripts/bump_version.py major
    python scripts/bump_version.py minor
    python scripts/bump_version.py patch
    python scripts/bump_version.py --current
    python scripts/bump_version.py --set 0.3.0
"""

import argparse
import re
import subprocess
from pathlib import Path
from typing import Tuple


def get_current_version() -> str:
    """Get current version from pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    content = pyproject_path.read_text()

    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Version not found in pyproject.toml")

    return match.group(1)


def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse version string into (major, minor, patch)."""
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")

    try:
        return tuple(int(p) for p in parts)  # type: ignore
    except ValueError:
        raise ValueError(f"Version parts must be integers: {version}")


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version tuple as string."""
    return f"{major}.{minor}.{patch}"


def bump_version(current: str, bump_type: str) -> str:
    """Bump version according to semantic versioning."""
    major, minor, patch = parse_version(current)

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

    return format_version(major, minor, patch)


def update_pyproject_toml(new_version: str) -> None:
    """Update version in pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    content = pyproject_path.read_text()

    # Update version field
    new_content = re.sub(r'(version\s*=\s*)["\']([^"\']+)["\']', rf'\1"{new_version}"', content)

    pyproject_path.write_text(new_content)
    print(f"✓ Updated pyproject.toml to version {new_version}")


def update_docs_conf(new_version: str) -> None:
    """Update version in docs/conf.py."""
    conf_path = Path(__file__).parent.parent / "docs" / "conf.py"
    content = conf_path.read_text()

    major, minor, _ = parse_version(new_version)
    short_version = f"{major}.{minor}"

    # Update release and version
    new_content = re.sub(r"release\s*=\s*['\"][^'\"]+['\"]", f'release = "{new_version}"', content)
    new_content = re.sub(
        r"version\s*=\s*['\"][^'\"]+['\"]", f'version = "{short_version}"', new_content
    )

    conf_path.write_text(new_content)
    print(f"✓ Updated docs/conf.py to version {new_version}")


def create_git_tag(version: str) -> None:
    """Create and push git tag."""
    tag = f"v{version}"

    try:
        subprocess.run(
            ["git", "tag", "-a", tag, "-m", f"Version {version}"], check=True, capture_output=True
        )
        print(f"✓ Created git tag {tag}")

        # Try to push (may fail if no remote)
        try:
            subprocess.run(["git", "push", "origin", tag], check=True, capture_output=True)
            print(f"✓ Pushed git tag {tag} to remote")
        except subprocess.CalledProcessError:
            print(f"⚠ Could not push tag {tag} to remote (no remote configured)")

    except subprocess.CalledProcessError as e:
        print(f"⚠ Git tag creation failed: {e.stderr.decode()}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Bump planar_geometry version")
    parser.add_argument(
        "bump",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Version bump type (major/minor/patch)",
    )
    parser.add_argument("--current", action="store_true", help="Show current version")
    parser.add_argument("--set", type=str, help="Set version to specific value")
    parser.add_argument("--no-tag", action="store_true", help="Don't create git tag")

    args = parser.parse_args()

    # Get current version
    current_version = get_current_version()

    if args.current:
        print(f"Current version: {current_version}")
        return

    # Determine new version
    if args.set:
        new_version = args.set
        # Validate
        try:
            parse_version(new_version)
        except ValueError as e:
            print(f"✗ {e}")
            return
    elif args.bump:
        new_version = bump_version(current_version, args.bump)
    else:
        parser.print_help()
        return

    # Skip if same version
    if new_version == current_version:
        print(f"Version already {new_version}")
        return

    print(f"Bumping version: {current_version} → {new_version}")

    # Update files
    update_pyproject_toml(new_version)
    update_docs_conf(new_version)

    # Create git commit
    try:
        subprocess.run(
            ["git", "add", "pyproject.toml", "docs/conf.py"], check=True, capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", f"chore: bump version to {new_version}"],
            check=True,
            capture_output=True,
        )
        print(f"✓ Created git commit")
    except subprocess.CalledProcessError as e:
        print(f"⚠ Git commit failed: {e.stderr.decode()}")

    # Create git tag
    if not args.no_tag:
        create_git_tag(new_version)

    print(f"\n✓ Version successfully bumped to {new_version}")


if __name__ == "__main__":
    main()
