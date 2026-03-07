from itertools import pairwise

import pytest

from secret_entrance import Dial, DialPosition


@pytest.mark.parametrize(
    "dial, rotation_str, an_expected_position",
    [
        (Dial(), "L22", DialPosition(40)),
    ]
)
def test_journey_contains(dial: Dial, rotation_str: str, an_expected_position: DialPosition) -> None:
    starting_position = dial.position
    rotation = Dial.Rotation.from_str(rotation_str)
    journey = dial.rotate_returning_journey(rotation)

    assert starting_position not in journey
    assert dial.position in journey
    assert DialPosition(-5) not in journey
    assert DialPosition(dial.size + 20) not in journey
    assert DialPosition(an_expected_position) in journey

    all_available_stops = set(range(dial.size))
    all_stops_on_journey = set(journey)
    all_unvisited_stops = all_available_stops - all_stops_on_journey

    assert len(all_available_stops) == dial.size
    assert len(all_stops_on_journey) == rotation.distance
    assert len(all_stops_on_journey) + len(all_unvisited_stops) == dial.size


@pytest.mark.parametrize(
    "dial, rotation",
    [
        (Dial(), Dial.Rotation.from_str("L22")),
    ]
)
def test_journey_iterator(dial: Dial, rotation: Dial.Rotation) -> None:
    starting_position = dial.position
    journey = dial.rotate_returning_journey(rotation)
    all_stops = list(journey)

    assert len(all_stops) == rotation.distance
    assert all_stops[-1] == dial.position

    unit_rotation = rotation.unit()
    assert all(
        Dial.predict_stop(Dial(start, dial.size), unit_rotation) == stop
        for start, stop in pairwise([starting_position] + all_stops)
    )


@pytest.mark.parametrize(
    "dial, rotation",
    [
        (Dial(), Dial.Rotation.from_str("L22")),
        (Dial(), Dial.Rotation.from_str("R50")),
        (Dial(position=DialPosition(5), size=10), Dial.Rotation.from_str("L5")),
    ]
)
def test_journey_len(dial: Dial, rotation: Dial.Rotation) -> None:
    starting_position = dial.position
    journey = dial.rotate_returning_journey(rotation)

    assert len(journey) == rotation.distance


def test_journey_len_matches_list_length() -> None:
    dial = Dial()
    rotation = Dial.Rotation.from_str("R25")
    journey = dial.rotate_returning_journey(rotation)

    assert len(journey) == len(list(journey))


@pytest.mark.parametrize(
    "dial, rotation",
    [
        (Dial(), Dial.Rotation.from_str("L22")),
        (Dial(), Dial.Rotation.from_str("R50")),
    ]
)
def test_journey_as_set_normal(dial: Dial, rotation: Dial.Rotation) -> None:
    starting_position = dial.position
    journey = dial.rotate_returning_journey(rotation)
    journey_set = journey.as_set()
    journey_list = list(journey)

    assert len(journey_set) <= rotation.distance
    assert all(pos in journey_set for pos in journey_list)


def test_journey_as_set_full_rotation() -> None:
    dial = Dial(size=100)
    rotation = Dial.Rotation.from_str("R100")
    journey = dial.rotate_returning_journey(rotation)
    journey_set = journey.as_set()

    assert len(journey_set) == dial.size
    assert journey_set == dial.as_set()


def test_journey_as_set_multiple_full_rotations() -> None:
    dial = Dial(size=100)
    rotation = Dial.Rotation.from_str("L250")
    journey = dial.rotate_returning_journey(rotation)
    journey_set = journey.as_set()

    assert len(journey_set) == dial.size
    assert journey_set == dial.as_set()


def test_journey_as_set_small_rotation() -> None:
    dial = Dial(position=DialPosition(10), size=100)
    rotation = Dial.Rotation.from_str("R5")
    journey = dial.rotate_returning_journey(rotation)
    journey_set = journey.as_set()

    expected_positions = {DialPosition(11), DialPosition(12), DialPosition(13), DialPosition(14), DialPosition(15)}
    assert journey_set == expected_positions


def test_journey_repr() -> None:
    dial = Dial(position=DialPosition(10))
    rotation = Dial.Rotation.from_str("R25")
    journey = dial.rotate_returning_journey(rotation)

    repr_str = repr(journey)
    assert "Journey" in repr_str
    assert "from=10" in repr_str
    assert "to=35" in repr_str
    assert "R25" in repr_str


@pytest.mark.parametrize(
    "start_position, rotation_str, test_position, should_cross",
    [
        (DialPosition(10), "R20", DialPosition(15), True),
        (DialPosition(10), "R20", DialPosition(30), True),
        (DialPosition(10), "R20", DialPosition(5), False),
        (DialPosition(10), "R20", DialPosition(10), False),
        (DialPosition(95), "R10", DialPosition(0), True),
    ]
)
def test_journey_crosses(
    start_position: DialPosition, rotation_str: str, test_position: DialPosition, should_cross: bool
) -> None:
    dial = Dial(position=start_position)
    rotation = Dial.Rotation.from_str(rotation_str)
    journey = dial.rotate_returning_journey(rotation)

    assert journey.crosses(test_position) == should_cross
    assert (test_position in journey) == should_cross
