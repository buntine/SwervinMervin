# Helper functions for generating level files.

import math
import csv

def ease_in(a, b, p):
    return a + (b - a) * (p ** 2)

def ease_out(a, b, p):
    return a + (b - a) * (1 - ((1 - p) ** 2))

def ease_in_out(a, b, p):
    return a + (b - a) * ((-math.cos(p * math.pi) / 2) + 0.5)

def add_corner(enter, hold, exit, curve, start_y=0, height=0):
    segments = []
    peak     = height * 260
    total    = float(enter + hold + exit)
    last_y   = start_y
    next_y   = start_y
 
    # Ease into corner.
    for n in range(enter):
        last_y = next_y
        next_y = ease_in_out(start_y, peak, n / total)
 
        segments.append([ease_in(0, curve, n / enter), last_y, next_y])

    # Hold.
    for n in range(hold):
        last_y = next_y
        next_y = ease_in_out(start_y, peak, (n + enter) / total)
 
        segments.append([curve, last_y, next_y])

    # Ease out of corner.
    for n in range(exit):
        last_y = next_y
        next_y = ease_in_out(start_y, peak, (n + enter + hold) / total)
 
        segments.append([ease_in_out(curve, 0, n / exit), last_y, next_y])

    return segments

def add_hill(enter, hold, exit, height, start_y):
    segments = []
    peak     = height * 260
    total    = float(enter + hold + exit)
    y        = start_y
    last_y   = 0

    for n in range(enter):
        last_y = y
        y = ease_in_out(start_y, peak, n / total)
        segments.append([0, last_y, y])

    for n in range(hold):
        last_y = y
        y = ease_in_out(start_y, peak, (n + enter) / total)
        segments.append([0, last_y, y])

    for n in range(exit):
        last_y = y
        y = ease_in_out(start_y, peak, (n + enter + hold) / total)
        segments.append([0, last_y, y])

    return segments

def add_straight(length, y):
    segments = []

    for n in range(length):
        segments.append([0, y, y])

    return segments

def last_y(segments):
    return segments[-1][-1]

def write(path, segments):
    with open(path, "w") as csvfile:
        w = csv.writer(csvfile)

        for row in segments:
            w.writerow(row)
