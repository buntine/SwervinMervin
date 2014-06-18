# Utility functions.

import math
import settings as s
from pygame.locals import *

def limit(v, low, high):
    """Returns v, limited to low/high threshold"""
    if v < low:
        return low
    elif v > high:
        return high
    else:
        return v

def steer(x, direction):
    """Returns a new X position for the player"""
    return limit(x + direction, -s.BOUNDS, s.BOUNDS)

def accelerate(speed, acceleration):
    """Returns a new speed given the acceleration/deceleration value"""
    return limit(speed + (s.ACCELERATION * acceleration), 0, s.TOP_SPEED)

def acceleration(keys):
    """Accepts key-polling array and returns appropriate acceleration factor"""
    a = -s.FRAME_RATE

    if keys[K_UP]:
        a = s.FRAME_RATE
    elif keys[K_DOWN]:
        a = -(s.FRAME_RATE * s.DECELERATION)

    return a

def direction(keys, dir_speed):
    """Accepts key-polling array and returns appropriate direction factor"""
    d = 0

    if keys[K_LEFT]:
        d = -dir_speed
    elif keys[K_RIGHT]:
        d = dir_speed

    return d

def position(position, speed, track_length):
    """Returns a new Z position for the camera, looping the track if we reach the end"""
    new_pos = position + (s.FRAME_RATE * speed)

    while new_pos >= track_length:
        new_pos -= track_length

    while new_pos < 0:
        new_pos += track_length

    return new_pos

def player_y(segment, percent):
    """Returns a new Y coordinate for the player given the current base segment"""
    top_y    = segment["top"]["world"]["y"]
    bottom_y = segment["bottom"]["world"]["y"]

    return top_y + (top_y - bottom_y) * percent

def ease_in(a, b, p):
    """Ease-in from a to b motion function"""
    return a + (b - a) * (p ** 2)

def ease_out(a, b, p):
    """Ease-out from a to b motion functon"""
    return a + (b - a) * (1 - ((1 - p) ** 2))

def ease_in_out(a, b, p):
    """Ease-in-and-then-out from a to b motion function"""
    return a + (b - a) * ((-math.cos(p * math.pi) / 2) + 0.5)
