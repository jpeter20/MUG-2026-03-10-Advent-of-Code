#!/usr/bin/env -S uv run --quiet
# ///
# requires-python = ">=3.14"
# ///

import sys
from pathlib import Path
from typing import TypeAlias


RotationList: TypeAlias = list[tuple[str, int]]


DIRECTION = { "L": -1, "R": 1 }


def part1(rotations: RotationList) -> int:
    """Return the number of times a rotation stops at `0`."""
    dial_size = 100
    current_position = 50
    number_of_stops_at_zero = 0

    for direction, distance in rotations:
        # For each rotation, see where it stops.
        current_position = (current_position + DIRECTION[direction] * distance) % dial_size
        if current_position == 0:
            number_of_stops_at_zero += 1

    return number_of_stops_at_zero


def part2(rotations: RotationList) -> int:
    """Return the number of times a rotation stops at **or crosses over** `0`."""
    dial_size = 100
    current_position = 50
    number_of_stops_at_or_crosses_over_zero = 0

    for direction, distance in rotations:
        # For each rotation...
        step = DIRECTION[direction]
        for _ in range(distance):
            # ...for each step within that rotation, see if that step lands on `0`.
            current_position = (current_position + step) % dial_size
            if current_position == 0:
                number_of_stops_at_or_crosses_over_zero += 1

    return number_of_stops_at_or_crosses_over_zero


def main() -> None:
    input_path = Path(sys.argv[1])

    rotations: RotationList = []

    with open(input_path) as f:
        for line in f.readlines():
            line = line.strip()
            rotations.append((line[0], int(line[1:])))

    print(f"Part 1: from the rotations provided in {input_path}, those rotations, applied in order, stop at 0 a total of {part1(rotations)} times.")
    print(f"Part 2: from the rotations provided in {input_path}, those rotations, applied in order, stop at or cross over 0 a total of {part2(rotations)} times.")


if __name__ == "__main__":
    main()
