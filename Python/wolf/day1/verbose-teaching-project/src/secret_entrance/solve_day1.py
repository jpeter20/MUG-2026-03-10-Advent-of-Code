"""
Advent of Code 2025 Day 1 solution.

This module applies the `Dial` machinery to solve both parts of the day's puzzle.
Run from the command line with an input file:

    day1 ../input.txt              # Run both parts
    day1 ../input.txt --part1      # Run only part 1
    day1 ../input.txt --part2      # Run only part 2
"""
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from secret_entrance.dial import Dial, DialPosition

app = typer.Typer()


@dataclass(frozen=True)
class Part1Result:
    """Result of part 1: password and the stops list for debugging."""
    password: int
    stops: list[DialPosition]
    starting_position: DialPosition
    ending_position: DialPosition
    dial_size: int


@dataclass(frozen=True)
class Part2Result:
    """Result of part 2: password and the journeys list for debugging."""
    password: int
    journeys: list[list[DialPosition]]
    starting_position: DialPosition
    ending_position: DialPosition
    dial_size: int


def part1(rotations: Iterable[Dial.Rotation]) -> Part1Result:
    """
    Solve part 1: count how many times the dial stops at position 0.

    Example usage:
        rotations = Dial.Rotation.multiple_from_file(Path("input.txt"))
        result = part1(rotations)
        print(f"Password: {result.password}")
    """
    dial = Dial()
    starting_position = dial.position
    stops = [dial.rotate_returning_stop(r) for r in rotations]
    password = stops.count(DialPosition(0))

    return Part1Result(
        password=password,
        stops=stops,
        starting_position=starting_position,
        ending_position=dial.position,
        dial_size=dial.size,
    )


def part2(rotations: Iterable[Dial.Rotation]) -> Part2Result:
    """
    Solve part 2: count how many times the dial crosses or stops at position 0.

    Unlike part 1, this counts every position crossed during rotation, not just where it stops.

    Example usage:
        rotations = Dial.Rotation.multiple_from_file(Path("input.txt"))
        result = part2(rotations)
        print(f"Password: {result.password}")
    """
    dial = Dial()
    starting_position = dial.position
    journeys = [list(dial.rotate_returning_journey(r)) for r in rotations]
    password = sum(j.count(DialPosition(0)) for j in journeys)

    return Part2Result(
        password=password,
        journeys=journeys,
        starting_position=starting_position,
        ending_position=dial.position,
        dial_size=dial.size,
    )


@app.command()
def main(
    input_file: Annotated[Path, typer.Argument(help="Path to the input file containing rotation instructions")],
    part1_only: Annotated[bool, typer.Option("--part1", help="Run only part 1")] = False,
    part2_only: Annotated[bool, typer.Option("--part2", help="Run only part 2")] = False,
) -> None:
    """
    Solve Advent of Code 2025 Day 1: Secret Entrance.

    By default, runs both parts. Use --part1 or --part2 to run only one part.
    """
    if not input_file.is_file():
        raise typer.BadParameter(f"Input file not found: {input_file}")

    rotations = Dial.Rotation.multiple_from_file(input_file)

    # Print header
    print("Advent of Code 2025, Day 1")
    print(f"Input: {input_file} ({len(rotations)} rotations)")
    print()

    # Determine what to run
    run_part1 = not part2_only  # Run part1 unless --part2 is specified alone
    run_part2 = not part1_only  # Run part2 unless --part1 is specified alone

    if run_part1:
        result = part1(rotations)
        print(f"Part 1: The dial stopped at position 0 a total of {result.password} times.")

    if run_part2:
        result = part2(rotations)
        print(f"Part 2: The dial crossed over or stopped at position 0 a total of {result.password} times.")


if __name__ == "__main__":
    app()
