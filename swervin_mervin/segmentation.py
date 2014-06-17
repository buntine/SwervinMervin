# Helper functions for generating / finding segments.

import settings as s
import projection as p

def build_level():
    """Builds an array of segments, pre-populating each with a Z position
       and alternating colour palette"""
    segments = []

    y = 0
    last_y = 0
    for n in range(25):
        last_y = y
        y = p.ease_in_out(0, (60 * 260), n / 75.0)
        segments.append(new_segment(n, 0, last_y, y))

    for n in range(25):
        last_y = y
        y = p.ease_in_out(0, (60 * 260), (n + 25) / 75.0)
        segments.append(new_segment(n + 25, 0, last_y, y))

    for n in range(25):
        last_y = y
        y = p.ease_in_out(0, (60 * 260), (n + 50) / 75.0)
        segments.append(new_segment(n + 50, 0, last_y, y))

    end_y = y

    for n in range(25):
        segments.append(new_segment(n + 75, 0, y, y))

    for n in range(25):
        last_y = y
        y = p.ease_in_out(end_y, 0, n / 75.0)
        segments.append(new_segment(n + 100, 0, last_y, y))

    for n in range(25):
        last_y = y
        y = p.ease_in_out(end_y, 0, (n + 25) / 75.0)
        segments.append(new_segment(n + 125, 0, last_y, y))

    for n in range(25):
        last_y = y
        y = p.ease_in_out(end_y, 0, (n + 50) / 75.0)
        segments.append(new_segment(n + 150, 0, last_y, y))


    segments += add_corner(len(segments), 50, 25, 100, 4)

    segments += add_corner(len(segments), 50, 25, 100, -6)

    for n in range(len(segments), len(segments) + 100):
        segments.append(new_segment(n, 0))

    return segments

def new_segment(index, curve, start_y=0, end_y=0):
    """Returns a new segment for the segments array"""
    palette = "dark" if (index / s.RUMBLE_LENGTH) % 2 == 0 else "light"
    segment = {
      "index":  index,
      "curve": curve,
      "top":    {"world": {"y": end_y, "z": ((index + 1) * s.SEGMENT_HEIGHT)},
                 "camera": {},
                 "screen": {}},
      "bottom": {"world": {"y": start_y, "z": (index * s.SEGMENT_HEIGHT)},
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
        segments.append(new_segment(segs + n, p.ease_in_out(curve, 0, n / exit)))

    return segments

def find_segment(z, segments):
    """Finds the correct segment for any given Z position"""
    i = int(round((z / s.SEGMENT_HEIGHT) % len(segments)))

    if i == len(segments):
        i = 0

    return segments[i]


