# Helper functions for generating / finding segments.

import settings as s
import util as u

    # Hold.
    for n in range(hold):
        segments.append(new_segment(segs + n, curve))
    segs += hold

    # Ease out of corner.
    for n in range(exit):
        segments.append(new_segment(segs + n, u.ease_in_out(curve, 0, n / exit)))

    return segments

def find_segment(z, segments):
    """Finds the correct segment for any given Z position"""
    i = int(round((z / s.SEGMENT_HEIGHT) % len(segments)))

    if i == len(segments):
        i = 0

    return segments[i]
