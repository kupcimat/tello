import pytest

import tello.tello_command as command


@pytest.mark.parametrize("cmd, expected_command_string", [
    (command.GenericCommand('custom command'), 'custom command'),
    (command.Command(), 'command'),
    (command.Takeoff(), 'takeoff'),
    (command.Land(), 'land'),
    (command.StreamOn(), 'streamon'),
    (command.StreamOff(), 'streamoff'),
    (command.Emergency(), 'emergency'),
    (command.Up(100), 'up 100'),
    (command.Down(100), 'down 100'),
    (command.Left(100), 'left 100'),
    (command.Right(100), 'right 100'),
    (command.Forward(100), 'forward 100'),
    (command.Back(100), 'back 100'),
    (command.Clockwise(100), 'cw 100'),
    (command.CounterClockwise(100), 'ccw 100'),
    (command.Flip('b'), 'flip b'),
    (command.Go(20, 30, 40, 50), 'go 20 30 40 50'),
    (command.SetSpeed(100), 'speed 100'),
    (command.SetWifi('name', 'password'), 'wifi name password'),
    (command.GetSpeed(), 'speed?'),
    (command.GetBattery(), 'battery?'),
    (command.GetTime(), 'time?'),
    (command.GetHeight(), 'height?'),
    (command.GetTemperature(), 'temp?'),
    (command.GetAttitude(), 'attitude?'),
    (command.GetBarometer(), 'baro?'),
    (command.GetAcceleration(), 'acceleration?'),
    (command.GetDistance(), 'tof?'),
    (command.GetWifi(), 'wifi?')
])
def test_commands(cmd, expected_command_string):
    assert cmd.get_command() == expected_command_string


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
