import settings as s

class Level:
    """Represents a level in the game world."""

    def __init__(self, path):
        self.path = path
        self.segments = []

    def build(self):
        """Reads the level file and builds a level by populating the segments array."""
        pass

    def track_length(self):
        return len(self.segments) * s.SEGMENT_HEIGHT

    def find_segment(self, position):
        """Returns the appropriate segment given a Z position."""
        n = len(self.segments)
        i = round((position / s.SEGMENT_HEIGHT) % n)

        if i == n
            i = 0

        return self.segments[i]

    def offset_segment(self, i):
        """Returns a segment by i, wrapping back to the beginning if we go past the end of the level."""
        return self.segments[i % len(self.segments)]

    def project_segment(self, i, camera_x, curve, curve_delta, position, player_y):
        """Modifies a segment in place, projecting the bottom and top lines to 2D coordinates."""
        self.__project_line(i, "top", camera_x - curve - curve_delta, position, player.y)
        self.__project_line(i, "bottom", camera_x - curve, position, player.y)

    def __project_line(self, i, line, camera_x, camera_z, player_y):
        """Projects a 3D world position into 2D coordinates for a given segment line."""
        p      = self.segments[i][line]
        width  = s.DIMENSIONS[0] / 2
        height = s.DIMENSIONS[1] / 2

        p["camera"]["x"] = p["world"].get("x", 0) - camera_x
        p["camera"]["y"] = p["world"].get("y", 0) - (s.CAMERA_HEIGHT + player_y)
        p["camera"]["z"] = p["world"].get("z", 0) - camera_z
        p["screen"]["s"] = s.CAMERA_DEPTH / p["camera"]["z"]
        p["screen"]["x"] = round(width + (p["screen"]["s"] * p["camera"]["x"] * width))
        p["screen"]["y"] = round(height + (p["screen"]["s"] * p["camera"]["y"] * height))
        p["screen"]["w"] = round(p["screen"]["s"] * s.ROAD_WIDTH * width)
