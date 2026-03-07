"""Tests for Dial.Rotation class and its nested Direction enum."""

from pathlib import Path

import pytest

from secret_entrance import Dial, DialPosition


class TestDirection:
    """Tests for Dial.Rotation.Direction enum."""

    def test_direction_values(self) -> None:
        """Direction enum maps L to -1 and R to 1 for arithmetic."""
        assert Dial.Rotation.Direction.L.value == -1
        assert Dial.Rotation.Direction.R.value == 1

    def test_direction_names(self) -> None:
        """Direction enum has L and R as member names."""
        assert Dial.Rotation.Direction.L.name == "L"
        assert Dial.Rotation.Direction.R.name == "R"

    def test_direction_from_string(self) -> None:
        """Direction can be accessed by string key."""
        assert Dial.Rotation.Direction["L"] == Dial.Rotation.Direction.L
        assert Dial.Rotation.Direction["R"] == Dial.Rotation.Direction.R

    # Is there an easy way, to see if a specific name is one of the choices? I would have expected
    # `"L" in Dial.Rotation.Direction` to work.


class TestRotationBasics:
    """Tests for basic Rotation construction and representation."""

    def test_rotation_construction(self) -> None:
        """Rotation can be constructed with direction and distance."""
        rotation = Dial.Rotation(Dial.Rotation.Direction.L, 42)
        assert rotation.direction == Dial.Rotation.Direction.L
        assert rotation.distance == 42

    def test_rotation_repr(self) -> None:
        """Rotation repr is compact: direction letter + distance."""
        assert repr(Dial.Rotation(Dial.Rotation.Direction.L, 42)) == "L42"
        assert repr(Dial.Rotation(Dial.Rotation.Direction.R, 99)) == "R99"

    def test_rotation_unit(self) -> None:
        """Rotation.unit() returns a rotation in the same direction with distance=1."""
        rotation = Dial.Rotation(Dial.Rotation.Direction.L, 42)
        unit = rotation.unit()
        assert unit.direction == Dial.Rotation.Direction.L
        assert unit.distance == 1


class TestRotationParsing:
    """Tests for parsing rotations from strings."""

    def test_from_str_basic(self) -> None:
        """from_str() parses basic rotation strings."""
        rotation = Dial.Rotation.from_str("L42")
        assert rotation.direction == Dial.Rotation.Direction.L
        assert rotation.distance == 42

        rotation = Dial.Rotation.from_str("R99")
        assert rotation.direction == Dial.Rotation.Direction.R
        assert rotation.distance == 99

    def test_from_str_case_insensitive(self) -> None:
        """from_str() handles lowercase direction letters."""
        rotation = Dial.Rotation.from_str("l42")
        assert rotation.direction == Dial.Rotation.Direction.L
        assert rotation.distance == 42

    def test_from_str_with_whitespace(self) -> None:
        """from_str() strips leading/trailing whitespace."""
        rotation = Dial.Rotation.from_str("  L42  ")
        assert rotation.direction == Dial.Rotation.Direction.L
        assert rotation.distance == 42

    def test_from_str_large_distance(self) -> None:
        """from_str() handles large distances (per problem: R1000 is valid)."""
        rotation = Dial.Rotation.from_str("R1000")
        assert rotation.direction == Dial.Rotation.Direction.R
        assert rotation.distance == 1000

    def test_from_str_invalid_direction(self) -> None:
        """from_str() raises ValueError for invalid direction letter."""
        with pytest.raises(ValueError, match="doesn't start with a valid direction"):
            _ = Dial.Rotation.from_str("X42")

    def test_from_str_no_direction(self) -> None:
        """from_str() raises ValueError when direction letter is missing."""
        with pytest.raises(ValueError, match="doesn't start with a valid direction"):
            _ = Dial.Rotation.from_str("42")

    def test_from_str_no_distance(self) -> None:
        """from_str() raises ValueError when distance is missing."""
        with pytest.raises(ValueError, match="too short"):
            _ = Dial.Rotation.from_str("L")

    def test_from_str_negative_distance(self) -> None:
        """from_str() raises ValueError for negative distance."""
        with pytest.raises(ValueError, match="must be entirely digits"):
            _ = Dial.Rotation.from_str("L-5")

    def test_from_str_float_distance(self) -> None:
        """from_str() raises ValueError for non-integer distance."""
        with pytest.raises(ValueError, match="must be entirely digits"):
            _ = Dial.Rotation.from_str("L3.5")

    def test_from_str_empty_string(self) -> None:
        """from_str() raises ValueError for empty string."""
        with pytest.raises(ValueError, match="must contain exactly one"):
            _ = Dial.Rotation.from_str("")

    def test_from_str_multiple_rotations(self) -> None:
        """from_str() raises ValueError when string contains multiple rotations."""
        with pytest.raises(ValueError, match="must contain exactly one"):
            _ = Dial.Rotation.from_str("L42 R10")


class TestRotationMultipleParsing:
    """Tests for parsing multiple rotations from strings and files."""

    def test_multiple_from_str(self) -> None:
        """multiple_from_str() parses newline-separated rotations."""
        rotations = Dial.Rotation.multiple_from_str("L68\nR48\nL99")
        assert len(rotations) == 3
        assert rotations[0] == Dial.Rotation(Dial.Rotation.Direction.L, 68)
        assert rotations[1] == Dial.Rotation(Dial.Rotation.Direction.R, 48)
        assert rotations[2] == Dial.Rotation(Dial.Rotation.Direction.L, 99)

    def test_multiple_from_str_empty_string(self) -> None:
        """multiple_from_str() returns empty tuple for empty string."""
        rotations = Dial.Rotation.multiple_from_str("")
        assert len(rotations) == 0

    def test_multiple_from_file_not_found(self) -> None:
        """multiple_from_file() raises FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            _ = Dial.Rotation.multiple_from_file(Path("/nonexistent/file.txt"))


class TestRotationExamplesFromProblem:
    """Tests using exact examples from the problem description."""

    def test_example_at_11_rotate_r8(self) -> None:
        """Problem example: dial at 11, rotate R8 → points at 19."""
        dial = Dial(position=DialPosition(11))
        rotation = Dial.Rotation.from_str("R8")
        final_position = dial.rotate_returning_stop(rotation)
        assert final_position == DialPosition(19)

    def test_example_at_19_rotate_l19(self) -> None:
        """Problem example: dial at 19, rotate L19 → points at 0."""
        dial = Dial(position=DialPosition(19))
        rotation = Dial.Rotation.from_str("L19")
        final_position = dial.rotate_returning_stop(rotation)
        assert final_position == DialPosition(0)

    def test_example_wrap_left_from_0(self) -> None:
        """Problem example: dial at 0, rotate L1 → points at 99."""
        dial = Dial(position=DialPosition(0))
        rotation = Dial.Rotation.from_str("L1")
        final_position = dial.rotate_returning_stop(rotation)
        assert final_position == DialPosition(99)

    def test_example_wrap_right_from_99(self) -> None:
        """Problem example: dial at 99, rotate R1 → points at 0."""
        dial = Dial(position=DialPosition(99))
        rotation = Dial.Rotation.from_str("R1")
        final_position = dial.rotate_returning_stop(rotation)
        assert final_position == DialPosition(0)

    def test_example_at_5_rotate_l10(self) -> None:
        """Problem example: dial at 5, rotate L10 → points at 95."""
        dial = Dial(position=DialPosition(5))
        rotation = Dial.Rotation.from_str("L10")
        final_position = dial.rotate_returning_stop(rotation)
        assert final_position == DialPosition(95)

    def test_example_at_95_rotate_r5(self) -> None:
        """Problem example: dial at 95, rotate R5 → points at 0."""
        dial = Dial(position=DialPosition(95))
        rotation = Dial.Rotation.from_str("R5")
        final_position = dial.rotate_returning_stop(rotation)
        assert final_position == DialPosition(0)

    def test_example_large_rotation_r1000(self) -> None:
        """Problem example: dial at 50, rotate R1000 → crosses 0 ten times, ends at 50."""
        dial = Dial(position=DialPosition(50))
        rotation = Dial.Rotation.from_str("R1000")
        journey = dial.rotate_returning_journey(rotation)

        # Should end back at 50
        assert dial.position == DialPosition(50)

        # Should cross 0 exactly 10 times
        positions = list(journey)
        assert positions.count(DialPosition(0)) == 10
