import pytest

import tello.tello_command as command


def test_generic_command():
    cmd = command.GenericCommand("command string")
    assert cmd.get_command() == "command string"


@pytest.mark.parametrize("distance, expected", [
    (-100, 20),
    (0, 20),
    (20, 20),
    (100, 100),
    (500, 500),
    (1000, 500)
])
def test_enforce_distance_range(distance, expected):
    assert command.enforce_distance_range('command', distance) == expected


@pytest.mark.parametrize("degree, expected", [
    (-100, 1),
    (0, 1),
    (1, 1),
    (100, 100),
    (3600, 3600),
    (10000, 3600)
])
def test_enforce_degree_range(degree, expected):
    assert command.enforce_degree_range('command', degree) == expected


@pytest.mark.parametrize("speed, expected", [
    (-100, 10),
    (0, 10),
    (10, 10),
    (50, 50),
    (100, 100),
    (1000, 100)
])
def test_enforce_speed_range(speed, expected):
    assert command.enforce_speed_range('command', speed) == expected


@pytest.mark.parametrize("direction, expected", [
    ("l", "l"),
    ("r", "r"),
    ("f", "f"),
    ("b", "b"),
    ("unsupported", "l")
])
def test_enforce_flip_direction(direction, expected):
    assert command.enforce_flip_direction(direction) == expected
