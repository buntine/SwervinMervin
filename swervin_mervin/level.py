import settings as s
import segment as seg
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
            self.add_segment(0, last_y, y)

        for n in range(25):
            last_y = y
            y = u.ease_in_out(0, (20 * 260), (n + 25) / 75.0)
            self.add_segment(0, last_y, y)

        for n in range(25):
            last_y = y
            y = u.ease_in_out(0, (20 * 260), (n + 50) / 75.0)
            self.add_segment(0, last_y, y)

        end_y = y
        for n in range(25):
            self.add_segment(0, y, y)

        for n in range(25):
            last_y = y
            y = u.ease_in_out(end_y, 0, n / 75.0)
            self.add_segment(0, last_y, y)

        for n in range(25):
            last_y = y
            y = u.ease_in_out(end_y, 0, (n + 25) / 75.0)
            self.add_segment(0, last_y, y)

        for n in range(25):
            last_y = y
            y = u.ease_in_out(end_y, 0, (n + 50) / 75.0)
            self.add_segment(0, last_y, y)

        self.add_corner(50, 25, 100, 4)
        self.add_corner(50, 25, 100, -6)

        for n in range(100):
            sprites = []

            if (n % 10 == 0):
                sprites.append({"sprite": s.SPRITES["column"], "offset": -1.1})
                sprites.append({"sprite": s.SPRITES["column"], "offset": 1.4})

            self.add_segment(0, 0, 0, sprites)

    def add_segment(self, curve, start_y=0, end_y=0, sprites=[]):
        """Creates a new segment and pushes it to the segments array"""
        palette = "dark" if (len(self.segments) / s.RUMBLE_LENGTH) % 2 == 0 else "light"
        segment = seg.Segment(palette, len(self.segments), curve, start_y, end_y, sprites)

        self.segments.append(segment)

    def add_corner(self, enter, hold, exit, curve):
        """Writes a curve (with easing) into the segments array"""
        # Ease into corner.
        for n in range(enter):
            self.add_segment(u.ease_in(0, curve, n / enter))

        # Hold.
        for n in range(hold):
            self.add_segment(curve)

        # Ease out of corner.
        for n in range(exit):
            self.add_segment(u.ease_in_out(curve, 0, n / exit))

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
