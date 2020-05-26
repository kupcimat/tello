from typing import Tuple


def find_mid_point(x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int]:
    return int((x1 + x2) / 2), int((y1 + y2) / 2)
