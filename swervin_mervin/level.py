import csv, os, random
import settings as s
import segment as seg
import competitor as c
import background as b
import sprite as sp
import tunnel_entrance as te
import tunnel_inside as ti

class Level:
    """Represents a level in the game world."""

    def __init__(self, details):
        self.name        = details["name"]
        self.slug        = details["id"]
        self.song        = details["song"]
        self.laps        = details["laps"]
        self.backgrounds = map(lambda bg: b.Background(bg["id"], bg["speed"], bg["scale"], bg["convert"]), details["backgrounds"])
        self.palettes    = details["colours"]
        self.finished    = False
        self.segments    = []
        self.competitors = []

    def build(self):
        """Reads the level file and builds a level by populating the segments array."""
        build_path = lambda p: os.path.join("swervin_mervin", "levels", p, "{0}.csv".format(self.slug))

        with open(build_path("tracks"), "r") as csvfile:
            for row in csv.reader(csvfile):
                flts = map(lambda c: float(c), row)
                self.add_segment(*flts)

        with open(build_path("sprites"), "r") as csvfile:
            for row in csv.reader(csvfile):

                if row[1] == "speed_boost":
                    self.add_speed_boost(int(row[0]), float(row[2]))
                else:
                    segment = self.segments[int(row[0])]
                    self.add_sprite(segment, row[1], float(row[2]), float(row[3]))

        with open(build_path("competitors"), "r") as csvfile:
            for row in csv.reader(csvfile):
                self.add_competitor(int(row[0]), float(row[1]), row[2], float(row[3]))

        with open(build_path("tunnels"), "r") as csvfile:
            for row in csv.reader(csvfile):
                self.add_tunnel(int(row[0]), int(row[1]))

    def add_segment(self, curve, start_y=0, end_y=0):
        """Creates a new segment and pushes it to the segments array"""
        palette = "dark" if (len(self.segments) / s.RUMBLE_LENGTH) % 2 == 0 else "light"
        segment = seg.Segment(self.palettes[palette], len(self.segments), curve, start_y, end_y)

        self.segments.append(segment)

    def add_sprite(self, segment, name, x, y=0.0):
        """Adds a sprite to the given segment."""
        sprite = sp.Sprite(name, x, y)
        segment.sprites.append(sprite)

    def add_polygon(self, segment, klass, when="pre", args=[]):
        """Adds a miscallaneous non-sprite renderable object to the given segment."""
        obj = klass(*args)

        if when == "pre":
            segment.pre_polygons.append(obj)
        else:
            segment.post_polygons.append(obj)

    def insert_bonuses(self):
        """Adds a couple of bonuses into the track at random places."""
        segs = random.sample(self.segments, 2)

        for s in segs:
            offset = random.randint(-10, 10) / 10.0
            self.add_sprite(s, "bonus", offset)

    def add_speed_boost(self, position, offset):
        """Inserts the sprites for speed boosts at the correct locations."""

        for n in range(0, s.SPEED_BOOST_LENGTH):
            segment = self.offset_segment(position + n)

            self.add_sprite(segment, "speed_boost", offset)
            segment.speed_boost = True

    def add_competitor(self, position, offset, name, speed):
        """Adds a competitor sprite to the given segment."""
        competitor = c.Competitor(position, offset, name, speed)
        self.competitors.append(competitor)

    def add_tunnel(self, start, end):
        """Tells the appropriate segments they are in a tunnel."""
        for segment in self.segments[start:end]:
            segment.in_tunnel = True

            if segment.index % s.TUNNEL_LIGHT_FREQ == 0:
                self.add_sprite(segment, "tunnel_light", -1.0, 2.0)
                self.add_sprite(segment, "tunnel_light", 1.0, 2.0)

        self.segments[end-1].tunnel_end = True
        self.add_polygon(self.segments[start], ti.TunnelInside, "pre")
        self.add_polygon(self.segments[start], te.TunnelEntrance, "post", [self.palettes["wall"]])

        self.add_sprite(self.segments[start], "tunnel_entrance", -1.0)
        self.add_sprite(self.segments[start], "tunnel_entrance", 1.85)

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
