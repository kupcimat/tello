import logging


def command() -> str:
    return "command"


def takeoff() -> str:
    return "takeoff"


def land() -> str:
    return "land"


def stream_on() -> str:
    return "streamon"


def stream_off() -> str:
    return "streamoff"


def emergency() -> str:
    return "emergency"


def up(distance: int) -> str:
    safe_distance = enforce_distance("up", distance)
    return f"up {safe_distance}"


def down(distance: int) -> str:
    safe_distance = enforce_distance("down", distance)
    return f"down {safe_distance}"


def left(distance: int) -> str:
    safe_distance = enforce_distance("left", distance)
    return f"left {safe_distance}"


def right(distance: int) -> str:
    safe_distance = enforce_distance("right", distance)
    return f"right {safe_distance}"


def forward(distance: int) -> str:
    safe_distance = enforce_distance("forward", distance)
    return f"forward {safe_distance}"


def backward(distance: int) -> str:
    safe_distance = enforce_distance("back", distance)
    return f"back {safe_distance}"


def clockwise(degrees: int) -> str:
    safe_degrees = enforce_degrees("cw", degrees)
    return f"cw {safe_degrees}"


def counter_clockwise(degrees: int) -> str:
    safe_degrees = enforce_degrees("ccw", degrees)
    return f"ccw {safe_degrees}"


def flip(direction: str) -> str:
    safe_direction = enforce_flip_direction(direction)
    return f"flip {safe_direction}"


def go(x: int, y: int, z: int, speed: int) -> str:
    safe_x = enforce_distance("go-x", x)
    safe_y = enforce_distance("go-y", y)
    safe_z = enforce_distance("go-z", z)
    safe_speed = enforce_speed("go-speed", speed)
    return f"go {safe_x} {safe_y} {safe_z} {safe_speed}"


def curve(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, speed: int) -> str:
    # TODO Add check for arc radius
    safe_x1 = enforce_distance("curve-x1", x1)
    safe_y1 = enforce_distance("curve-y1", y1)
    safe_z1 = enforce_distance("curve-z1", z1)
    safe_x2 = enforce_distance("curve-x2", x2)
    safe_y2 = enforce_distance("curve-y2", y2)
    safe_z2 = enforce_distance("curve-z2", z2)
    safe_speed = enforce_lower_speed("curve-speed", speed)
    return f"curve {safe_x1} {safe_y1} {safe_z1} {safe_x2} {safe_y2} {safe_z2} {safe_speed}"


def set_speed(speed: int) -> str:
    safe_speed = enforce_speed("speed", speed)
    return f"speed {safe_speed}"


def set_wifi(ssid: str, password: str) -> str:
    return f"wifi {ssid} {password}"


def get_speed() -> str:
    return "speed?"


def get_battery() -> str:
    return "battery?"


def get_time() -> str:
    return "time?"


def get_height() -> str:
    return "height?"


def get_temperature() -> str:
    return "temp?"


def get_attitude() -> str:
    return "attitude?"


def get_barometer() -> str:
    return "baro?"


def get_acceleration() -> str:
    return "acceleration?"


def get_distance() -> str:
    return "tof?"


def get_wifi() -> str:
    return "wifi?"


def enforce_distance(command_name, distance):
    return enforce_range(command_name, distance, "distance", 20, 500)


def enforce_degrees(command_name, degrees):
    return enforce_range(command_name, degrees, "degrees", 1, 3600)


def enforce_speed(command_name, speed):
    return enforce_range(command_name, speed, "speed", 10, 100)


def enforce_lower_speed(command_name, speed):
    return enforce_range(command_name, speed, "speed", 10, 60)


def enforce_range(command_name, value, value_description, min_value, max_value):
    if value < min_value:
        logging.warning(f"command=%s error=invalid-%s value=%s expected=[%s-%s]",
                        command_name, value_description, value, min_value, max_value)
        return min_value
    elif value > max_value:
        logging.warning(f"command=%s error=invalid-%s value=%s expected=[%s-%s]",
                        command_name, value_description, value, min_value, max_value)
        return max_value
    else:
        return value


def enforce_flip_direction(direction):
    expected_values = ["l", "r", "f", "b"]
    if direction not in expected_values:
        logging.warning(f"command=flip error=invalid-direction value=%s expected=%s",
                        direction, expected_values)
        return "l"
    else:
        return direction
