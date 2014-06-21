import settings as s
import util as u

class Level:
    """Represents a level in the game world."""

    def __init__(self, path):
        self.path = path
        self.segments = []

    def build(self):
        """Reads the level file and builds a level by populating the segments array."""
        y = 0
        last_y = 0
        for n in range(25):
            last_y = y
            y = u.ease_in_out(0, (20 * 260), n / 75.0)
            self.segments.append(self.new_segment(n, 0, last_y, y))

        for n in range(25):
            last_y = y
            y = u.ease_in_out(0, (20 * 260), (n + 25) / 75.0)
            self.segments.append(self.new_segment(n + 25, 0, last_y, y))

        for n in range(25):
            last_y = y
            y = u.ease_in_out(0, (20 * 260), (n + 50) / 75.0)
            self.segments.append(self.new_segment(n + 50, 0, last_y, y))

        end_y = y

        for n in range(25):
            self.segments.append(self.new_segment(n + 75, 0, y, y))

        for n in range(25):
            last_y = y
            y = u.ease_in_out(end_y, 0, n / 75.0)
            self.segments.append(self.new_segment(n + 100, 0, last_y, y))

        for n in range(25):
            last_y = y
            y = u.ease_in_out(end_y, 0, (n + 25) / 75.0)
            self.segments.append(self.new_segment(n + 125, 0, last_y, y))

        for n in range(25):
            last_y = y
            y = u.ease_in_out(end_y, 0, (n + 50) / 75.0)
            self.segments.append(self.new_segment(n + 150, 0, last_y, y))

        self.add_corner(len(self.segments), 50, 25, 100, 4)
        self.add_corner(len(self.segments), 50, 25, 100, -6)

        for n in range(len(self.segments), len(self.segments) + 100):
            sprites = []

            if (n % 10 == 0):
                sprites.append({"sprite": s.SPRITES["column"], "offset": -1.1})
                sprites.append({"sprite": s.SPRITES["column"], "offset": 1.4})

            self.segments.append(self.new_segment(n, 0, 0, 0, sprites))

    def new_segment(self, index, curve, start_y=0, end_y=0, sprites=[]):
        """Returns a new segment for the segments array"""
        palette = "dark" if (index / s.RUMBLE_LENGTH) % 2 == 0 else "light"
        segment = {
          "index":  index,
          "curve": curve,
          "sprites":  sprites,
          "top":    {"world": {"y": end_y, "z": ((index + 1) * s.SEGMENT_HEIGHT)},
                     "camera": {},
                     "screen": {}},
          "bottom": {"world": {"y": start_y, "z": (index * s.SEGMENT_HEIGHT)},
                     "camera": {},
                     "screen": {}},
          "colour": s.COLOURS[palette]}

        return segment

    def add_corner(self, i, enter, hold, exit, curve):
        """Writes a curve (with easing) into the segments array"""
        segs = i

        # Ease into corner.
        for n in range(enter):
            self.segments.append(self.new_segment(segs + n, u.ease_in(0, curve, n / enter)))
        segs += enter

        # Hold.
        for n in range(hold):
            self.segments.append(self.new_segment(segs + n, curve))
        segs += hold

        # Ease out of corner.
        for n in range(exit):
            self.segments.append(self.new_segment(segs + n, u.ease_in_out(curve, 0, n / exit)))

    def track_length(self):
        return len(self.segments) * s.SEGMENT_HEIGHT

    def find_segment(self, position):
        """Returns the appropriate segment given a Z position."""
        n = len(self.segments)
        i = int(round((position / s.SEGMENT_HEIGHT) % n))

        if i == n:
            i = 0

        return self.segments[i]

    def offset_segment(self, i):
        """Returns a segment by i, wrapping back to the beginning if we go past the end of the level."""
        return self.segments[i % len(self.segments)]

    def project_segment(self, i, camera_x, curve, curve_delta, position, player_y):
        """Modifies a segment in place, projecting the bottom and top lines to 2D coordinates."""
        self.__project_line(i, "top", camera_x - curve - curve_delta, position, player_y)
        self.__project_line(i, "bottom", camera_x - curve, position, player_y)

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
