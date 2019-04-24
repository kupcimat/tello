import math


class BoundingBox:
    def __init__(self, x_limit, y_limit, z_limit):
        self.x_limit = x_limit
        self.y_limit = y_limit
        self.z_limit = z_limit
        self.current_position = (0, 0)  # [-x_limit, x_limit], [-y_limit, y_limit]
        self.current_angle = 0  # [0, 359]
        self.current_height = 0  # [0, z_limit]

    def climb(self, change):
        self.current_height = self._compute_new_height(change)

    def rotate(self, angle):
        self.current_angle = (self.current_angle + angle) % 360

    def move_forward(self, distance):
        if distance < 0:
            raise RuntimeError("Distance must be >= 0")

        change = self._compute_position_change(distance)
        self.current_position = self._compute_new_position(change)

    def _compute_new_height(self, change):
        new_height = self.current_height + change
        if new_height < 0:
            raise RuntimeError("Height must be >= 0")
        if new_height > self.z_limit:
            raise RuntimeError("Exceeded z-axis limit", self.z_limit)

        return new_height

    def _compute_new_position(self, change):
        new_x = self.current_position[0] + change[0]
        new_y = self.current_position[1] + change[1]

        if abs(new_x) > self.x_limit:
            raise RuntimeError("Exceeded x-axis limit", self.x_limit)
        if abs(new_y) > self.y_limit:
            raise RuntimeError("Exceeded y-axis limit", self.y_limit)

        return new_x, new_y

    def _compute_position_change(self, distance):
        quadrant = self.current_angle // 90  # [0, 3]
        quadrant_angle = self.current_angle % 90  # [0, 89]
        quadrant_radians = math.radians(quadrant_angle)

        if quadrant == 0:
            return distance * math.sin(quadrant_radians), distance * math.cos(quadrant_radians)
        elif quadrant == 1:
            return distance * math.cos(quadrant_radians), -1 * (distance * math.sin(quadrant_radians))
        elif quadrant == 2:
            return -1 * (distance * math.sin(quadrant_radians)), -1 * (distance * math.cos(quadrant_radians))
        elif quadrant == 3:
            return -1 * (distance * math.cos(quadrant_radians)), distance * math.sin(quadrant_radians)
        else:
            raise RuntimeError("Unexpected quadrant", quadrant)
