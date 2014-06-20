# Utility functions.

import math

def limit(v, low, high):
    """Returns v, limited to low/high threshold"""
    if v < low:
        return low
    elif v > high:
        return high
    else:
        return v

def ease_in(a, b, p):
    """Ease-in from a to b motion function"""
    return a + (b - a) * (p ** 2)

def ease_out(a, b, p):
    """Ease-out from a to b motion functon"""
    return a + (b - a) * (1 - ((1 - p) ** 2))

def ease_in_out(a, b, p):
    """Ease-in-and-then-out from a to b motion function"""
    return a + (b - a) * ((-math.cos(p * math.pi) / 2) + 0.5)
