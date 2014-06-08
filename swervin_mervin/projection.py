# Helper functions for projection.

import math

def build_segments(segment_height, rumble_length, colours):
    segments = []

    for n in range(400):
        segments.append({
          "index":  n,
          "top":    {"world": {"z": ((n + 1) * segment_height)}, "camera": {}, "screen": {}},
          "bottom": {"world": {"z": (n * segment_height)}, "camera": {}, "screen": {}},
          "colour": colours["dark"] if (n / rumble_length) % 2 == 0 else colours["light"]})

    return segments

def find_segment(z, segments, segment_length):
    return segments[math.trunc((z / segment_length) % len(segments))]

def project_line(segment, line, camera_x, camera_y, camera_z, camera_depth, dimensions, road_width):
    p = segment[line]

    p["camera"]["x"] = p["world"].get("x", 0) - camera_x
    p["camera"]["y"] = p["world"].get("y", 0) - camera_y
    p["camera"]["z"] = p["world"].get("z", 0) - camera_z
    p["screen"]["s"] = camera_depth / p["camera"]["z"]
    p["screen"]["x"] = math.trunc((dimensions[0] / 2) + (p["screen"]["s"] * p["camera"]["x"] * (dimensions[0] / 2)))
    p["screen"]["y"] = math.trunc((dimensions[1] / 2) + (p["screen"]["s"] * p["camera"]["y"] * (dimensions[1] / 2)))
    p["screen"]["w"] = math.trunc(p["screen"]["s"] * road_width * (dimensions[0] / 2))

    return p
