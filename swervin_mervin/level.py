import settings as s
import segment as seg
import competitor as c
import sprite as sp
import csv, os, pygame

class Level:
    """Represents a level in the game world."""

    def __init__(self, name):
        self.name        = name
        self.segments    = []
        self.competitors = []
        self.high_scores = []

    def build(self):
        """Reads the level file and builds a level by populating the segments array."""
        base_path        = os.path.join("swervin_mervin", "levels", self.name)
        level_path       = os.path.join(base_path, "segments.csv")
        sprites_path     = os.path.join(base_path, "sprites.csv")
        competitors_path = os.path.join(base_path, "competitors.csv")
        high_scores_path = os.path.join(base_path, "high_scores.csv")

        with open(level_path, "r") as csvfile:
            for row in csv.reader(csvfile):
                ints = map(lambda c: float(c), row)
                self.add_segment(*ints)

        with open(sprites_path, "r") as csvfile:
            for row in csv.reader(csvfile):
                segment = self.segments[int(row[0])]
                self.add_sprite(segment, float(row[1]), row[2])

        with open(competitors_path, "r") as csvfile:
            for row in csv.reader(csvfile):
                self.add_competitor(int(row[0]), float(row[1]), row[2], float(row[3]))

        with open(high_scores_path, "r") as csvfile:
            for row in csv.reader(csvfile):
                self.add_high_score(row[0], int(row[1]))

    def add_segment(self, curve, start_y=0, end_y=0):
        """Creates a new segment and pushes it to the segments array"""
        palette = "dark" if (len(self.segments) / s.RUMBLE_LENGTH) % 2 == 0 else "light"
        segment = seg.Segment(palette, len(self.segments), curve, start_y, end_y)

        self.segments.append(segment)

    def add_sprite(self, segment, offset, name):
        """Adds a sprite to the given segment."""
        sprite = sp.Sprite(offset, name)
        segment.sprites.append(sprite)

    def add_competitor(self, position, offset, name, speed):
        """Adds a competitor sprite to the given segment."""
        competitor = c.Competitor(position, offset, name, speed)
        self.competitors.append(competitor)

    def add_high_score(self, name, score):
        """Adds a high score to the level."""
        self.high_scores.append([name, score])

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
