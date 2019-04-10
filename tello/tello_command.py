class TelloCommand:
    def get_command(self):
        raise NotImplementedError()


class GenericCommand(TelloCommand):
    def __init__(self, command_string):
        self.command_string = command_string

    def get_command(self):
        return self.command_string


class Command(TelloCommand):
    def get_command(self):
        return "command"


class Takeoff(TelloCommand):
    def get_command(self):
        return "takeoff"


class Land(TelloCommand):
    def get_command(self):
        return "land"


class StreamOn(TelloCommand):
    def get_command(self):
        return "streamon"


class StreamOff(TelloCommand):
    def get_command(self):
        return "streamoff"


class Emergency(TelloCommand):
    def get_command(self):
        return "emergency"


class Up(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range("up", distance)

    def get_command(self):
        return f"up {self.distance}"


class Down(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range("down", distance)

    def get_command(self):
        return f"down {self.distance}"


class Left(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range("left", distance)

    def get_command(self):
        return f"left {self.distance}"


class Right(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range("right", distance)

    def get_command(self):
        return f"right {self.distance}"


class Forward(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range("forward", distance)

    def get_command(self):
        return f"forward {self.distance}"


class Back(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range("back", distance)

    def get_command(self):
        return f"back {self.distance}"


class Clockwise(TelloCommand):
    def __init__(self, degree):
        self.degree = enforce_degree_range("cw", degree)

    def get_command(self):
        return f"cw {self.degree}"


class CounterClockwise(TelloCommand):
    def __init__(self, degree):
        self.degree = enforce_degree_range("ccw", degree)

    def get_command(self):
        return f"ccw {self.degree}"


class Flip(TelloCommand):
    def __init__(self, direction):
        self.direction = enforce_flip_direction(direction)

    def get_command(self):
        return f"flip {self.direction}"


class Go(TelloCommand):
    def __init__(self, x, y, z, speed):
        self.x = enforce_distance_range("go", x)
        self.y = enforce_distance_range("go", y)
        self.z = enforce_distance_range("go", z)
        self.speed = enforce_speed_range("go", speed)

    def get_command(self):
        return f"go {self.x} {self.y} {self.z} {self.speed}"


class Curve(TelloCommand):
    def __init__(self, x1, y1, z1, x2, y2, z2, speed):
        # TODO Add check for arc radius
        self.x1 = enforce_distance_range("curve", x1)
        self.y1 = enforce_distance_range("curve", y1)
        self.z1 = enforce_distance_range("curve", z1)
        self.x2 = enforce_distance_range("curve", x2)
        self.y2 = enforce_distance_range("curve", y2)
        self.z2 = enforce_distance_range("curve", z2)
        self.speed = enforce_lower_speed_range("curve", speed)

    def get_command(self):
        return f"curve {self.x1} {self.y1} {self.z1} {self.x2} {self.y2} {self.z2} {self.speed}"


class SetSpeed(TelloCommand):
    def __init__(self, speed):
        self.speed = enforce_speed_range("speed", speed)

    def get_command(self):
        return f"speed {self.speed}"


class SetWifi(TelloCommand):
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password

    def get_command(self):
        return f"wifi {self.ssid} {self.password}"


class GetSpeed(TelloCommand):
    def get_command(self):
        return f"speed?"


class GetBattery(TelloCommand):
    def get_command(self):
        return f"battery?"


class GetTime(TelloCommand):
    def get_command(self):
        return f"time?"


class GetHeight(TelloCommand):
    def get_command(self):
        return f"height?"


class GetTemperature(TelloCommand):
    def get_command(self):
        return f"temp?"


class GetAttitude(TelloCommand):
    def get_command(self):
        return f"attitude?"


class GetBarometer(TelloCommand):
    def get_command(self):
        return f"baro?"


class GetAcceleration(TelloCommand):
    def get_command(self):
        return f"acceleration?"


class GetDistance(TelloCommand):
    def get_command(self):
        return f"tof?"


class GetWifi(TelloCommand):
    def get_command(self):
        return f"wifi?"


def enforce_distance_range(command, distance):
    return enforce_range(command, distance, "distance", 20, 500)


def enforce_degree_range(command, degree):
    return enforce_range(command, degree, "degree", 1, 3600)


def enforce_speed_range(command, speed):
    return enforce_range(command, speed, "speed", 10, 100)


def enforce_lower_speed_range(command, speed):
    return enforce_range(command, speed, "speed", 10, 60)


def enforce_range(command, value, value_description, min_value, max_value):
    if value < min_value:
        print(f"command {command}: invalid {value_description} {value}, allowed range is [{min_value}-{max_value}]")
        return min_value
    elif value > max_value:
        print(f"command {command}: invalid {value_description} {value}, allowed range is [{min_value}-{max_value}]")
        return max_value
    else:
        return value


def enforce_flip_direction(direction):
    allowed_values = ["l", "r", "f", "b"]
    if direction not in allowed_values:
        print(f"command flip: invalid direction {direction}, allowed values are {allowed_values}")
        return "l"
    else:
        return direction
