"""Tests for part 1 solution."""

from secret_entrance import Dial, DialPosition, part1


def test_part1_example(test_rotations: tuple[Dial.Rotation, ...]):
    """Test part 1 with the example from the problem description."""
    result = part1(test_rotations)

    # From problem: "the password in this example is 3"
    assert result.password == 3

    # Verify the dial ended at position 32 (from problem description)
    assert result.ending_position == DialPosition(32)

    # Verify dial properties
    assert result.starting_position == DialPosition(50)
    assert result.dial_size == 100

    # Verify the three stops at 0
    assert result.stops.count(DialPosition(0)) == 3
