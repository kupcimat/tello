class TelloCommand:
    def get_command(self):
        pass


class GenericCommand(TelloCommand):
    def __init__(self, command_string):
        self.command_string = command_string

    def get_command(self):
        return self.command_string


class Command(TelloCommand):
    def get_command(self):
        return 'command'


class Takeoff(TelloCommand):
    def get_command(self):
        return 'takeoff'


class Land(TelloCommand):
    def get_command(self):
        return 'land'


class StreamOn(TelloCommand):
    def get_command(self):
        return 'streamon'


class StreamOff(TelloCommand):
    def get_command(self):
        return 'streamoff'


class Emergency(TelloCommand):
    def get_command(self):
        return 'emergency'


class Up(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range('up', distance)

    def get_command(self):
        return f'up {self.distance}'


class Down(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range('down', distance)

    def get_command(self):
        return f'down {self.distance}'


class Left(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range('left', distance)

    def get_command(self):
        return f'left {self.distance}'


class Right(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range('right', distance)

    def get_command(self):
        return f'right {self.distance}'


class Forward(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range('forward', distance)

    def get_command(self):
        return f'forward {self.distance}'


class Back(TelloCommand):
    def __init__(self, distance):
        self.distance = enforce_distance_range('back', distance)

    def get_command(self):
        return f'back {self.distance}'


def enforce_distance_range(command, distance):
    return enforce_range(command, distance, 'distance', 20, 500)


def enforce_range(command, value, value_description, min_value, max_value):
    if value < min_value:
        print(f'command {command}: invalid {value_description} {value}, allowed range is [{min_value}-{max_value}]')
        return min_value
    elif value > max_value:
        print(f'command {command}: invalid {value_description} {value}, allowed range is [{min_value}-{max_value}]')
        return max_value
    else:
        return value
