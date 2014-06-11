# Helper functions for projection.

import settings as s

def build_segments():
    """Builds an array of segments, pre-populating each with a Z position
       and alternating colour palette"""
    segments = []

    for n in range(500):
        palette = "dark" if (n / s.RUMBLE_LENGTH) % 2 == 0 else "light"

        segments.append({
          "index":  n,
          "top":    {"world": {"z": ((n + 1) * s.SEGMENT_HEIGHT)},
                     "camera": {},
                     "screen": {}},
          "bottom": {"world": {"z": (n * s.SEGMENT_HEIGHT)},
                     "camera": {},
                     "screen": {}},
          "colour": s.COLOURS[palette]})

    return segments

def find_segment(z, segments):
    """Finds the correct segment for any given Z position"""
    i = int(round((z / s.SEGMENT_HEIGHT) % len(segments)))

    if i == len(segments):
        i = 0

    return segments[i]

def project_line(segment, line, camera_x, camera_z):
    """Translates 3d coordinates to fit into a 2d surface.
       Modifies segment[line] in place."""
    p      = segment[line]
    width  = s.DIMENSIONS[0] / 2
    height = s.DIMENSIONS[1] / 2

    p["camera"]["x"] = p["world"].get("x", 0) - camera_x
    p["camera"]["y"] = p["world"].get("y", 0) - s.CAMERA_HEIGHT
    p["camera"]["z"] = p["world"].get("z", 0) - camera_z
    p["screen"]["s"] = s.CAMERA_DEPTH / p["camera"]["z"]
    p["screen"]["x"] = round(width + (p["screen"]["s"] * p["camera"]["x"] * width))
    p["screen"]["y"] = round(height + (p["screen"]["s"] * p["camera"]["y"] * height))
    p["screen"]["w"] = round(p["screen"]["s"] * s.ROAD_WIDTH * width)

def steer(x, direction):
    """Returns a new X position for the player"""
    new_x = x + direction

    # Prevent player from going too far off track.
    if new_x < -s.BOUNDS:
        new_x = -s.BOUNDS
    elif new_x > s.BOUNDS:
        new_x = s.BOUNDS

    return new_x

def accelerate(speed, acceleration):
    """Returns a new speed given the acceleration/deceleration value"""
    new_speed = speed + (s.ACCELERATION * acceleration)

    if new_speed > s.TOP_SPEED:
        new_speed = s.TOP_SPEED
    if new_speed < 0:
        new_speed = 0

    return new_speed

def position(position, speed, track_length):
    """Returns a new Z position for the camera"""
    new_pos = position + (s.FRAME_RATE * speed)

    while new_pos >= track_length:
        new_pos -= track_length
    while new_pos < 0:
        new_pos += track_length

    return new_pos
