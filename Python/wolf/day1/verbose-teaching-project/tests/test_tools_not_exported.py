"""Tests for tools_not_exported module."""

import io
from contextlib import redirect_stdout

import pytest

from secret_entrance import Dial, DialPosition, part1, part2
from secret_entrance.tools_not_exported import (
    debug_part1,
    debug_part2,
    stop_at_the_same_position,
)


class TestStopAtTheSamePosition:
    """Tests for stop_at_the_same_position function."""

    @pytest.mark.parametrize(
        "dial, rotation1_str, rotation2_str, should_match",
        [
            (Dial(), "R25", "R25", True),
            (Dial(size=100), "L50", "R50", True),
            (Dial(), "L25", "R25", False),
            (Dial(size=100), "R10", "L90", True),
        ]
    )
    def test_stop_at_same_position_cases(
        self, dial: Dial, rotation1_str: str, rotation2_str: str, should_match: bool
    ) -> None:
        rotation1 = Dial.Rotation.from_str(rotation1_str)
        rotation2 = Dial.Rotation.from_str(rotation2_str)

        assert stop_at_the_same_position(dial, rotation1, rotation2) == should_match

    def test_full_rotation_same_as_no_rotation(self) -> None:
        dial = Dial(position=DialPosition(25), size=100)
        rotation_full = Dial.Rotation.from_str("R100")
        rotation_none = Dial.Rotation(Dial.Rotation.Direction.R, 0)

        assert stop_at_the_same_position(dial, rotation_full, rotation_none)


class TestDebugPart1:
    """Tests for debug_part1 function."""

    def test_debug_part1_output_format(
        self, test_rotations: tuple[Dial.Rotation, ...]
    ) -> None:
        expected_strings = ["starts by pointing at", "rotated", "Stopped at 0", "Ended on"]
        result = part1(test_rotations)

        output = io.StringIO()
        with redirect_stdout(output):
            debug_part1(result, test_rotations)

        output_str = output.getvalue()

        for expected in expected_strings:
            assert expected in output_str

    def test_debug_part1_shows_details(self, test_rotations: tuple[Dial.Rotation, ...]) -> None:
        result = part1(test_rotations)

        output = io.StringIO()
        with redirect_stdout(output):
            debug_part1(result, test_rotations)

        output_str = output.getvalue()
        assert str(result.starting_position) in output_str
        assert str(result.password) in output_str


class TestDebugPart2:
    """Tests for debug_part2 function."""

    def test_debug_part2_output_format(
        self, test_rotations: tuple[Dial.Rotation, ...]
    ) -> None:
        expected_strings = ["starts by pointing at", "rotated", "total of"]
        result = part2(test_rotations)

        output = io.StringIO()
        with redirect_stdout(output):
            debug_part2(result, test_rotations)

        output_str = output.getvalue()

        for expected in expected_strings:
            assert expected in output_str

    def test_debug_part2_shows_details(self, test_rotations: tuple[Dial.Rotation, ...]) -> None:
        result = part2(test_rotations)

        output = io.StringIO()
        with redirect_stdout(output):
            debug_part2(result, test_rotations)

        output_str = output.getvalue()
        assert str(result.starting_position) in output_str
        assert str(result.password) in output_str

    def test_debug_part2_mentions_crossing_zero(self) -> None:
        rotations = (
            Dial.Rotation.from_str("L68"),
            Dial.Rotation.from_str("R48"),
            Dial.Rotation.from_str("L99"),
        )
        result = part2(rotations)

        output = io.StringIO()
        with redirect_stdout(output):
            debug_part2(result, rotations)

        output_str = output.getvalue()

        assert "points at 0" in output_str or str(result.password) in output_str
