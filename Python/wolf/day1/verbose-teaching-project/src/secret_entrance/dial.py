"""Some classes to represent and manipulate the state needed to solve Advent of Code 2025 day 1."""

from collections.abc import Iterator
from dataclasses import dataclass, field, replace
from enum import Enum
from pathlib import Path
from typing import NewType, override

DialPosition = NewType("DialPosition", int)  # Would be **inside** `Dial` but Python doesn't allow it.


@dataclass
class Dial:
    """
    All the solution **machinery** for Advent of Code 2025 day 1.

    That is, the code here models the things actually **in** the problems, but it doesn't know the problems
    themselves, such as what events are being counted. This is all about the state and the transformations.

    `Dial` looks more complicated than it is. It **contains** a couple of other class definitions. I do this
    just to get the naming I wanted. There are other ways I could have gone about this, but the reasons to
    pick one over the other come down to taste. Here's what I define:

        `class Dial`  # a `dataclass`
            `class Rotation`  # a `dataclass`
                `class Direction` # an `Enum`
            `class Journey`  # a `dataclass`

    I would have put `DialPosition` in here as well (as `Position`) but Python doesn't allow it.

    `Dial` itself is pretty simple. It has a size (the total number of different `DialPosition`s it can "point" to)
    and to which of those positions it is currently pointing. The positions go from `0` to the total size - 1. You
    can change the current position by applying a `Dial.Rotation` using the instance method `Dial.rotate()`.

    For the basic solution, you only need:
        - `Rotation.from_str()` and `Rotation.multiple_from_file()` to parse input
        - `rotate_returning_stop()` for part 1 (where did we end up?)
        - `rotate_returning_journey()` for part 2 (what positions did we cross?)

    Additional methods like `predict_stop()`, `as_set()`, `Journey.as_set()`, and `Rotation.unit()` are
    provided for more advanced analysis or for solving larger variations of the problem.

    Because these are all `dataclass`es, they already work with `dataclasses.replace` and `copy.copy`. `deepcopy`
    doesn't matter: all members here are scalar, and `Rotation` and `Journey` are already frozen. `DialPosition`
    is really an `int`, so simple assignment is already a copy. Examples:

        from dataclasses import replace
        from copy import copy

        dial = Dial()
        dial2 = copy(dial)
        dial3 = replace(dial, _position=12)

        dial == dial2  # True
        dial is dial2  # False
        dial == dial3  # False
    """

    @dataclass(frozen=True)
    class Rotation:
        """`Dial.Rotation` is a single transformation of a `Dial`."""

        class Direction(Enum):
            """`Dial.Rotation.Direction` works with "L" and "R" as found in the input data, and `-1` and `1` make the math easy."""
            L = -1
            R = 1

        # `Dial.Rotation` members
        direction: Direction
        distance: int

        # Why not implement `__len__`? Because a rotation isn't like a collection. It doesn't **contain** things.
        # `len(x)` almost always means "the number of items in `x`". That's appropriate for a `Journey`, but not
        # for a `Rotation`.

        @override
        def __repr__(self) -> str:
            """Expresses a `Dial.Rotation` as, e.g., `"L41"` instead of the very long default for a `dataclass`."""
            return f"{self.direction.name}{self.distance}"

        def unit(self) -> "Dial.Rotation":
            """Return a new `DialRotation` in the same direction, but `distance==1`."""
            return replace(self, distance=1)

        @classmethod
        def from_str(cls, rotation_spec: str) -> "Dial.Rotation":
            """Build a single new `Dial.Rotation` from a string, e.g., `"L41"` (a factory method)."""
            rotation_spec = rotation_spec.strip()
            if (n := len(rotation_spec.split())) != 1:
                raise ValueError(f'`Rotation.from_str("{rotation_spec}")`: the string describing the rotation must contain exactly one, e.g., "L41". The supplied specification contains {n}.')
            # We can test for too short, but the problem description didn't make any promises about how long it could be. "R10000000" is allowed.
            if len(rotation_spec) < 2:
                raise ValueError(f'`Rotation.from_str("{rotation_spec}")`: the input string is ill-formed. It\'s too short.')

            direction_str, distance_str = rotation_spec[0].upper(), rotation_spec[1:]

            if direction_str not in cls.Direction.__members__.keys():
                raise ValueError(f'`Rotation.from_str("{rotation_spec}")`: the input string is ill-formed. It doesn\'t start with a valid direction letter.')
            if not distance_str.isdigit():
                raise ValueError(f'`Rotation.from_str("{rotation_spec}")`: the input string is ill-formed. After the direction, the remainder of the string must be entirely digits (also excludes "-").')

            return Dial.Rotation(Dial.Rotation.Direction[direction_str], int(distance_str))

        @classmethod
        def multiple_from_str(cls, rotation_specs: str) -> tuple["Dial.Rotation", ...]:
            r"""
            Build an ordered sequence (tuple) of `Dial.Rotation`s given a multi-line string.

            Expects one rotation per line, as the problem specifies. Blank lines are skipped.

            If you need to parse whitespace-separated rotations on a single line, preprocess first:

                import re
                specs = re.sub(r"\s+", r"\n", "L42 R10 L5")
                rotations = Dial.Rotation.multiple_from_str(specs)
            """
            return tuple(cls.from_str(line) for line in rotation_specs.splitlines() if line.strip())

        @classmethod
        def multiple_from_file(cls, path: Path) -> tuple["Dial.Rotation", ...]:
            """Build an ordered sequence (tuple) of `Dial.Rotation`s, from the contents of a file (a factory method built on `.multiple_from_str`)."""
            if not path.is_file():
                raise FileNotFoundError(f'`Dial.Rotation.multiple_from_file("{path=}")`): "{path}" is not a file.')
            with open(path) as f:
                return cls.multiple_from_str(f.read())


    @dataclass(frozen=True)
    class Journey:
        """
        `Dial.Journey` is the result of applying a `Dial.Rotation` to a `Dial`.

        Think of it something like (the built-in) `range`. It tells what `DialPosition`s the `Dial` crosses over
        during the `Dial.Rotation`. It's a bit backwards from a `range`, though. It **doesn't** include the start
        position (unless the rotation is so large that it "goes all the way around"). It **does** include the
        stop position.

        Why am I missing the obvious constructor: taking a dial and a rotation? If I did that, there would be
        two options. I could either actually apply the rotation, modifying the dial parameter as a side-effect,
        or else, I could make the caller do the math twice. It's not much math. The performance is not really
        a convincing argument, it's just that both choices are unpalatable.
        """
        start: DialPosition
        stop: DialPosition
        rotation: Dial.Rotation
        dial_size: int = field(default=100)

        # `Dial.Journey` construction is cheap. No work to contruct any of the fields. No `__init__`. No `__post_init__`.

        def __iter__(self) -> Iterator[DialPosition]:
            """
            Lazily generate the ordered sequence of every `DialPosition` covered by a `Dial.Rotation`.

            Creating the iterator is cheap. Taking one step is cheap. The iterator is automatically invoked
            in all the places you expect, e.g., `for` loops; but `list(journey)` and `set(journey)` will
            use it ... and fully resolve it ... to build the thing you want.
            """
            current = self.start
            unit_rotation = self.rotation.unit()
            for _ in range(self.rotation.distance):
                # Constructing a temporary `Dial` here is cheap, and necessary (because `predict_stop` won't modify it).
                current = Dial.predict_stop(Dial(current, self.dial_size), unit_rotation)
                yield current
            assert current == self.stop, "Something bizarre is wrong (in `Dial.Journey.__iter__`): the `Journey` didn't end where it was supposed to."

        def __contains__(self, p: DialPosition) -> bool:
            """
            Return `True` if `p` is a `DialPosition` covered by the provided `Dial.Rotation`.

            This implementation is pure vanity. For `j: Dial.Journey` and `p: DialPosition` you could just as
            easily say `p in set(j)`. The performance of this is better in the case where the `self.rotation.distance`
            is larger than `self.dial_size`, and a **little** better when the rotation **doesn't** go all the way
            around.
            """
            return self.rotation.distance >= self.dial_size or any(p == pos for pos in self)

        def __len__(self) -> int:
            """Return the "length" of the `Journey` (though it's not realized until you turn it into a list)."""
            return self.rotation.distance

        def as_set(self) -> set[DialPosition]:
            """Return a fully resolved set of `DialPosition`s covered by the underlying rotation."""
            return Dial(size=self.dial_size).as_set() if self.rotation.distance >= self.dial_size else set(self)

        @override
        def __repr__(self) -> str:
            """Provide a readable representation of the Journey."""
            return f"Journey(from={self.start}, to={self.stop}, rotation={self.rotation})"

        def crosses(self, position: DialPosition) -> bool:
            """
            Check if the journey crosses the given position (semantic alias for __contains__).

            Example:
                journey = dial.rotate_returning_journey(Dial.Rotation.from_str("R25"))
                if journey.crosses(DialPosition(0)):
                    print("Crossed zero!")
            """
            return position in self


    # `Dial` members
    _position: DialPosition
    size: int

    # `Dial` construction is cheap: initializing two fields. No calculations. No non-debug `__post_init__`.

    def __init__(self, position: DialPosition | None = None, size: int = 100):
        """Construct a `Dial`."""
        if position is None:
            position = DialPosition(min(50, size // 2))
        assert size > 0, f"Programming error (in `Dial({position=}, {size=})`): the new `Dial`s size must be greater than zero. You asked for {size}."
        assert 0 <= position < size, f"Programming error (in `Dial({position=}, {size=})`): the starting position must be **on** the dial, that is, `0 <= {position=} < {size=}`."
        self._position = position
        self.size = size

    @override
    def __repr__(self) -> str:
        return f"Dial(position={self._position}, size={self.size})"

    @property
    def position(self) -> DialPosition:
        """Read-only property: the `DialPosition` to which this `Dial` currently points."""
        return self._position

    @staticmethod
    def predict_stop(dial: Dial, rotation: Dial.Rotation) -> DialPosition:
        """Centralize the ring-math for moving a `Dial`. This is a pure function that does not modify the dial."""
        # Annoying: `%`, the mod operator, produces an `int`, so I have to cast.
        return DialPosition((dial.position + rotation.distance * rotation.direction.value) % dial.size)

    def rotate(self, rotation: Dial.Rotation) -> None:
        """Move to a new position according to the supplied `Dial.Rotation`."""
        self._position = self.predict_stop(self, rotation)

    def rotate_returning_stop(self, rotation: Dial.Rotation) -> DialPosition:
        """Rotate with this method when you care about the final position."""
        self.rotate(rotation)
        return self.position

    def rotate_returning_journey(self, rotation: Dial.Rotation) -> Dial.Journey:
        """Rotate with this method when you want to reason about every position crossed during the rotation."""
        start = self.position
        self.rotate(rotation)
        return Dial.Journey(start, self.position, rotation, self.size)

    def as_set(self) -> set[DialPosition]:
        """Return a `set` comprising every available `DialPosition` (in case you want to do `set` math)."""
        return set(DialPosition(p) for p in range(self.size))
