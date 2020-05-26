import pytest

import kupcimat.command as command


@pytest.mark.parametrize("command_string, expected_command_string", [
    (command.command(), "command"),
    (command.takeoff(), "takeoff"),
    (command.land(), "land"),
    (command.stream_on(), "streamon"),
    (command.stream_off(), "streamoff"),
    (command.emergency(), "emergency"),
    (command.up(100), "up 100"),
    (command.down(100), "down 100"),
    (command.left(100), "left 100"),
    (command.right(100), "right 100"),
    (command.forward(100), "forward 100"),
    (command.backward(100), "back 100"),
    (command.clockwise(100), "cw 100"),
    (command.counter_clockwise(100), "ccw 100"),
    (command.flip("b"), "flip b"),
    (command.go(20, 30, 40, 50), "go 20 30 40 50"),
    (command.curve(20, 30, 40, 50, 60, 70, 50), "curve 20 30 40 50 60 70 50"),
    (command.set_speed(100), "speed 100"),
    (command.set_wifi("name", "password"), "wifi name password"),
    (command.get_speed(), "speed?"),
    (command.get_battery(), "battery?"),
    (command.get_time(), "time?"),
    (command.get_height(), "height?"),
    (command.get_temperature(), "temp?"),
    (command.get_attitude(), "attitude?"),
    (command.get_barometer(), "baro?"),
    (command.get_acceleration(), "acceleration?"),
    (command.get_distance(), "tof?"),
    (command.get_wifi(), "wifi?")
])
def test_commands(command_string, expected_command_string):
    assert command_string == expected_command_string


@pytest.mark.parametrize("distance, expected", [
    (-100, 20),
    (0, 20),
    (20, 20),
    (100, 100),
    (500, 500),
    (1000, 500)
])
def test_enforce_distance(distance, expected):
    assert command.enforce_distance("command", distance) == expected


@pytest.mark.parametrize("degrees, expected", [
    (-100, 1),
    (0, 1),
    (1, 1),
    (100, 100),
    (3600, 3600),
    (10000, 3600)
])
def test_enforce_degrees(degrees, expected):
    assert command.enforce_degrees("command", degrees) == expected


@pytest.mark.parametrize("speed, expected", [
    (-100, 10),
    (0, 10),
    (10, 10),
    (50, 50),
    (100, 100),
    (1000, 100)
])
def test_enforce_speed(speed, expected):
    assert command.enforce_speed("command", speed) == expected


@pytest.mark.parametrize("speed, expected", [
    (-100, 10),
    (0, 10),
    (10, 10),
    (50, 50),
    (60, 60),
    (100, 60)
])
def test_enforce_lower_speed(speed, expected):
    assert command.enforce_lower_speed("command", speed) == expected


@pytest.mark.parametrize("direction, expected", [
    ("l", "l"),
    ("r", "r"),
    ("f", "f"),
    ("b", "b"),
    ("unsupported", "l")
])
def test_enforce_flip_direction(direction, expected):
    assert command.enforce_flip_direction(direction) == expected
