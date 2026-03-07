"""Shared test fixtures and utilities for the secret_entrance test suite."""

import os
from dataclasses import replace
from pathlib import Path

import pytest

from secret_entrance import Dial, DialPosition


@pytest.fixture
def test_input_file() -> Path:
    """
    Path to the test input file shared across all tests.

    Requires TEST_INPUT environment variable (set by direnv/.envrc).
    """
    if not (test_input_path := os.environ.get("TEST_INPUT")):
        pytest.skip("TEST_INPUT environment variable not set (direnv not active?)")
    return Path(test_input_path)


@pytest.fixture
def test_rotations(test_input_file: Path) -> tuple[Dial.Rotation, ...]:
    """Load rotations from the test input file."""
    return Dial.Rotation.multiple_from_file(test_input_file)


@pytest.fixture
def default_dial() -> Dial:
    """Return a dial with default settings (position=50, size=100)."""
    return Dial()


@pytest.fixture
def default_dial_at_zero() -> Dial:
    """Return a default-sized dial starting at position 0 (useful for testing wrap-around)."""
    return replace(Dial(), position=DialPosition(0))
