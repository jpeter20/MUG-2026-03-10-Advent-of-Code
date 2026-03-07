"""
Functions useful in debugging and testing, but not necessary for solving the Advent of Code problems.

These utilities are available in IPython sessions (see `.ipython/profile_default/startup/`) but
are not exported in `secret_entrance.__all__`. They're helpful for exploring the problem space
and writing tests, but aren't part of the core solution machinery.
"""

from collections.abc import Iterable
from enum import Enum
from typing import TYPE_CHECKING

from secret_entrance.dial import Dial, DialPosition
from secret_entrance.solve_day1 import Part1Result, Part2Result


def stop_at_the_same_position(dial: Dial, rotation1: Dial.Rotation, rotation2: Dial.Rotation) -> bool:
    """
    Return `True` if two rotations would end at the same position.

    Example:
        dial = Dial(size=100)
        stop_at_the_same_position(dial, Dial.Rotation.from_str("L50"), Dial.Rotation.from_str("R50"))  # True

    """
    return rotation1 == rotation2 or Dial.predict_stop(dial, rotation1) == Dial.predict_stop(dial, rotation2)


# Why not write `make_the_same_journey(dial, rotation1, rotation2)`? Because that could only be true iff `rotation1 == rotation2`.


def debug_part1(result: Part1Result, rotations: Iterable[Dial.Rotation]) -> None:
    """
    Print part 1 execution in problem description format.

    Example:
        from secret_entrance.solve_day1 import part1, Part1Result
        rotations = Dial.Rotation.multiple_from_file(Path("test-input.txt"))
        result = part1(rotations)
        debug_part1(result, rotations)

    """
    print(f"The dial starts by pointing at {result.starting_position}.")
    for rotation, stop in zip(rotations, result.stops):
        print(f"The dial is rotated {rotation} to point at {stop}.")
    print(f"Stopped at 0 a total of {result.password} times. Ended on {result.ending_position}.")


def debug_part2(result: Part2Result, rotations: Iterable[Dial.Rotation]) -> None:
    """
    Print part 2 execution in problem description format.

    Example:
        from secret_entrance.solve_day1 import part2, Part2Result
        rotations = Dial.Rotation.multiple_from_file(Path("test-input.txt"))
        result = part2(rotations)
        debug_part2(result, rotations)

    """
    print(f"The dial starts by pointing at {result.starting_position}.")
    for rotation, journey in zip(rotations, result.journeys):
        final_position = journey[-1]
        stopped_at_zero = final_position == DialPosition(0)
        crossed_zero = journey.count(DialPosition(0)) - stopped_at_zero

        print(f"The dial is rotated {rotation} to point at {final_position}", end="")
        match crossed_zero:
            case 0:
                pass
            case 1:
                print("; during this rotation, it points at 0 once", end="")
            case _:
                print(f"; during this rotation, it points at 0 a total of {crossed_zero} times", end="")
        print(".")

    print(f"Stopped at or crossed position 0 a total of {result.password} times.")
