"""Tests for part 2 solution."""

from secret_entrance import Dial, DialPosition, part2


def test_part2_example(test_rotations: tuple[Dial.Rotation, ...]):
    """Test part 2 with the example from the problem description."""
    result = part2(test_rotations)

    # From problem: "the new password would be 6"
    assert result.password == 6

    # Verify the dial ended at position 32 (same as part 1)
    assert result.ending_position == DialPosition(32)

    # Verify dial properties
    assert result.starting_position == DialPosition(50)
    assert result.dial_size == 100

    # Count total zeros across all journeys
    total_zeros = sum(j.count(DialPosition(0)) for j in result.journeys)
    assert total_zeros == 6
