import settings as s
import segment as seg
import util as u
import csv

class Level:
    """Represents a level in the game world."""

    def __init__(self, path):
        self.path = path
        self.segments = []

    def build(self):
        """Reads the level file and builds a level by populating the segments array."""
        with open(self.path, "r") as csvfile:
            for row in csv.reader(csvfile):
                ints = map(lambda c: int(c), row)
                self.add_segment(*ints)

    def add_segment(self, curve, start_y=0, end_y=0, sprites=[]):
        """Creates a new segment and pushes it to the segments array"""
        palette = "dark" if (len(self.segments) / s.RUMBLE_LENGTH) % 2 == 0 else "light"
        segment = seg.Segment(palette, len(self.segments), curve, start_y, end_y, sprites)

        self.segments.append(segment)

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
