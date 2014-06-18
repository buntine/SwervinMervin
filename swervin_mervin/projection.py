# Helper functions for projection.

import settings as s

def project_line(segment, line, camera_x, camera_z, player_y):
    """Translates 3d coordinates to fit into a 2d surface.
       Modifies segment[line] in place."""
    p      = segment[line]
    width  = s.DIMENSIONS[0] / 2
    height = s.DIMENSIONS[1] / 2

    p["camera"]["x"] = p["world"].get("x", 0) - camera_x
    p["camera"]["y"] = p["world"].get("y", 0) - (s.CAMERA_HEIGHT + player_y)
    p["camera"]["z"] = p["world"].get("z", 0) - camera_z
    p["screen"]["s"] = s.CAMERA_DEPTH / p["camera"]["z"]
    p["screen"]["x"] = round(width + (p["screen"]["s"] * p["camera"]["x"] * width))
    p["screen"]["y"] = round(height + (p["screen"]["s"] * p["camera"]["y"] * height))
    p["screen"]["w"] = round(p["screen"]["s"] * s.ROAD_WIDTH * width)
