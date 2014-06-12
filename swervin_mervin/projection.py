# Helper functions for projection.

import settings as s
import math

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

    # Prevent player from going too fast.
    if new_speed > s.TOP_SPEED:
        new_speed = s.TOP_SPEED
    elif new_speed < 0:
        new_speed = 0

    return new_speed

def position(position, speed, track_length):
    """Returns a new Z position for the camera, looping the track if we reach the end"""
    new_pos = position + (s.FRAME_RATE * speed)

    while new_pos >= track_length:
        new_pos -= track_length

    while new_pos < 0:
        new_pos += track_length

    return new_pos

def ease_in(a, b, p):
    """Traditional ease-in from a to b motion function"""
    return a + (b - a) * (p ** 2)

def ease_out(a, b, p):
    """Traditional ease-in-and-then-out from a to b motion function"""
    return a + (b - a) * (-math.cos(p * math.pi) / 2) + 0.5
