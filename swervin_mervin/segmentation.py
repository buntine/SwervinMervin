# Helper functions for generating / finding segments.

import settings as s
import projection as p

def build_level():
    """Builds an array of segments, pre-populating each with a Z position
       and alternating colour palette"""
    segments = []

    for n in range(100):
        segments.append(new_segment(n, 0))

    segments += add_corner(len(segments), 50, 50, 50, 2)

    for n in range(len(segments), len(segments) + 100):
        segments.append(new_segment(n, 0))

    return segments

def new_segment(index, curve):
    """Returns a new segment for the segments array"""
    palette = "dark" if (index / s.RUMBLE_LENGTH) % 2 == 0 else "light"
    segment = {
      "index":  index,
      "curve": curve,
      "top":    {"world": {"z": ((index + 1) * s.SEGMENT_HEIGHT)},
                 "camera": {},
                 "screen": {}},
      "bottom": {"world": {"z": (index * s.SEGMENT_HEIGHT)},
                 "camera": {},
                 "screen": {}},
      "colour": s.COLOURS[palette]}

    return segment

def add_corner(i, enter, hold, exit, curve):
    """Writes a curve (with easing) into the segments array"""
    segments = []
    segs     = i

    # Ease into corner.
    for n in range(enter):
        segments.append(new_segment(segs + n, p.ease_in(0, curve, n / enter)))
    segs += enter

    # Hold.
    for n in range(hold):
        segments.append(new_segment(segs + n, curve))
    segs += hold

    # Ease out of corner.
    for n in range(exit):
        segments.append(new_segment(segs + n, p.ease_out(curve, 0, n / exit)))

    return segments

def find_segment(z, segments):
    """Finds the correct segment for any given Z position"""
    i = int(round((z / s.SEGMENT_HEIGHT) % len(segments)))

    if i == len(segments):
        i = 0

    return segments[i]


