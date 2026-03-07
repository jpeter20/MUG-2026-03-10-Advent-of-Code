import pytest

from secret_entrance import Dial, DialPosition


def test_dial_construction() -> None:
    with pytest.raises(AssertionError):
        _ = Dial(size=-1)
    with pytest.raises(AssertionError):
        _ = Dial(position=DialPosition(50), size=10)


def test_dial_repr() -> None:
    expected = "Dial(position=50, size=100)"
    dial = Dial()
    assert repr(dial) == expected


def test_dial_position_property() -> None:
    dial = Dial(position=DialPosition(25), size=100)
    assert dial.position == DialPosition(25)


@pytest.mark.parametrize(
    "start_position, rotation_str, expected_position",
    [
        (DialPosition(10), "R5", DialPosition(15)),
        (DialPosition(95), "R10", DialPosition(5)),
        (DialPosition(5), "L10", DialPosition(95)),
    ]
)
def test_dial_rotate(start_position: DialPosition, rotation_str: str, expected_position: DialPosition) -> None:
    dial = Dial(position=start_position, size=100)
    rotation = Dial.Rotation.from_str(rotation_str)
    dial.rotate(rotation)
    assert dial.position == expected_position


@pytest.mark.parametrize(
    "start_position, rotation_str, expected_position",
    [
        (DialPosition(20), "R15", DialPosition(35)),
        (DialPosition(90), "R20", DialPosition(10)),
    ]
)
def test_dial_predict_stop(start_position: DialPosition, rotation_str: str, expected_position: DialPosition) -> None:
    dial = Dial(position=start_position, size=100)
    rotation = Dial.Rotation.from_str(rotation_str)

    predicted = Dial.predict_stop(dial, rotation)

    assert predicted == expected_position
    assert dial.position == start_position


def test_dial_as_set() -> None:
    dial = Dial(size=10)
    positions_set = dial.as_set()

    assert len(positions_set) == 10
    assert all(DialPosition(i) in positions_set for i in range(10))
    assert DialPosition(10) not in positions_set
    assert DialPosition(-1) not in positions_set


def test_dial_as_set_default_size() -> None:
    dial = Dial()
    positions_set = dial.as_set()

    assert len(positions_set) == 100


@pytest.mark.parametrize(
    "start_position, rotation_str, expected_stop",
    [
        (DialPosition(10), "R25", DialPosition(35)),
        (DialPosition(90), "R20", DialPosition(10)),
        (DialPosition(50), "L30", DialPosition(20)),
    ]
)
def test_dial_rotate_returning_stop(
    start_position: DialPosition, rotation_str: str, expected_stop: DialPosition
) -> None:
    dial = Dial(position=start_position)
    rotation = Dial.Rotation.from_str(rotation_str)

    result = dial.rotate_returning_stop(rotation)

    assert result == expected_stop
    assert dial.position == expected_stop


@pytest.mark.parametrize(
    "start_position, rotation_str, expected_stop, expected_length",
    [
        (DialPosition(10), "R25", DialPosition(35), 25),
        (DialPosition(90), "R20", DialPosition(10), 20),
        (DialPosition(50), "L30", DialPosition(20), 30),
    ]
)
def test_dial_rotate_returning_journey(
    start_position: DialPosition, rotation_str: str, expected_stop: DialPosition, expected_length: int
) -> None:
    dial = Dial(position=start_position)
    rotation = Dial.Rotation.from_str(rotation_str)

    journey = dial.rotate_returning_journey(rotation)

    assert journey.start == start_position
    assert journey.stop == expected_stop
    assert dial.position == expected_stop
    assert len(journey) == expected_length
    assert list(journey)[-1] == expected_stop if expected_length > 0 else True


class TestDialEdgeCases:
    """Tests for edge cases with small dials and zero-distance rotations."""

    @pytest.mark.parametrize(
        "size, start_position, rotation_str, expected_position",
        [
            (1, DialPosition(0), "R5", DialPosition(0)),
            (1, DialPosition(0), "L3", DialPosition(0)),
            (2, DialPosition(0), "R1", DialPosition(1)),
            (2, DialPosition(1), "R1", DialPosition(0)),
            (100, DialPosition(25), "R0", DialPosition(25)),
            (100, DialPosition(50), "L0", DialPosition(50)),
        ]
    )
    def test_edge_case_rotations(
        self, size: int, start_position: DialPosition, rotation_str: str, expected_position: DialPosition
    ) -> None:
        dial = Dial(position=start_position, size=size)
        rotation = Dial.Rotation.from_str(rotation_str) if "R0" not in rotation_str and "L0" not in rotation_str else Dial.Rotation(Dial.Rotation.Direction.R if "R" in rotation_str else Dial.Rotation.Direction.L, 0)
        dial.rotate(rotation)
        assert dial.position == expected_position

    @pytest.mark.parametrize(
        "start_position, distance, expected_journey",
        [
            (DialPosition(10), 0, []),
            (DialPosition(10), 1, [DialPosition(11)]),
            (DialPosition(99), 1, [DialPosition(0)]),
        ]
    )
    def test_journey_edge_cases(
        self, start_position: DialPosition, distance: int, expected_journey: list[DialPosition]
    ) -> None:
        dial = Dial(position=start_position)
        rotation = Dial.Rotation(Dial.Rotation.Direction.R, distance)
        journey = dial.rotate_returning_journey(rotation)

        assert len(journey) == distance
        assert list(journey) == expected_journey
