import pytest

from tello.bounding_box import BoundingBox
from test.tello import asin

raises_runtime_error = pytest.mark.xfail(raises=RuntimeError, strict=True)


@pytest.mark.parametrize("climbs, expected_heights", [
    ([0], [0]),
    ([30], [30]),
    ([100], [100]),
    ([30, -30, 30, 30, 30], [30, 0, 30, 60, 90]),
    pytest.param([-30], [None], marks=raises_runtime_error),
    pytest.param([130], [None], marks=raises_runtime_error),
    pytest.param([30, -30, 30, 30, 100], [30, 0, 30, 60, None], marks=raises_runtime_error)
])
def test_climb(climbs, expected_heights):
    box = BoundingBox(100, 100, 100)

    for climb, height in zip(climbs, expected_heights):
        box.climb(climb)
        assert box.current_height == pytest.approx(height)


@pytest.mark.parametrize("rotations, expected_angles", [
    ([-390], [330]),
    ([-360], [0]),
    ([-30], [330]),
    ([0], [0]),
    ([30], [30]),
    ([360], [0]),
    ([390], [30]),
    ([-30, 30, 30, 30, -30], [330, 0, 30, 60, 30]),
    ([-390, 390, 390, 390, -390], [330, 0, 30, 60, 30])
])
def test_rotate(rotations, expected_angles):
    box = BoundingBox(100, 100, 100)

    for rotation, angle in zip(rotations, expected_angles):
        box.rotate(rotation)
        assert box.current_angle == pytest.approx(angle)


# move = (angle, distance)
# position = (x, y)
@pytest.mark.parametrize("moves, expected_positions", [
    # do not move
    ([(0, 0)],
     [(0, 0)]),
    # move straight
    ([(0, 10)],
     [(0, 10)]),
    # move straight twice
    ([(0, 10), (0, 10)],
     [(0, 10), (0, 20)]),
    # rotate and do not move
    ([(45, 0)],
     [(0, 0)]),
    # rotate twice and do not move
    ([(30, 0), (30, 0)],
     [(0, 0), (0, 0)]),
    # move in right angles
    ([(0, 10), (90, 20), (90, 30), (90, 40)],
     [(0, 10), (20, 10), (20, -20), (-20, -20)]),
    # move complex in square
    ([(asin(3 / 5), 5), (90, 5), (90, 5), (90, 5)],
     [(3, 4), (7, 1), (4, -3), (0, 0)]),
    # move complex in diamond
    ([(asin(3 / 5), 5),
      (asin(4 / 5) * 2, 5),
      (asin(3 / 5) * 2, 5),
      (asin(4 / 5) * 2, 5)],
     [(3, 4), (6, 0), (3, -4), (0, 0)])
])
def test_move_forward(moves, expected_positions):
    box = BoundingBox(100, 100, 100)

    for move, position in zip(moves, expected_positions):
        angle, distance = move
        box.rotate(angle)
        box.move_forward(distance)
        assert box.current_position == pytest.approx(position)

# TODO test exceed box
