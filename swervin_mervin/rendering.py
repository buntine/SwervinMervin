# Helper functions for rendering.

import pygame
import settings as s

def render_road(window, segment):
    top      = segment["top"]["screen"]
    bottom   = segment["bottom"]["screen"]
    y_top    = (s.DIMENSIONS[1] - top["y"])
    y_bottom = (s.DIMENSIONS[1] - bottom["y"])
    colour   = segment["colour"]

    # Road.
    points = [((bottom["x"] - bottom["w"]), y_bottom),
              ((bottom["x"] + bottom["w"]), y_bottom),
              ((top["x"] + top["w"]),       y_top),
              ((top["x"] - top["w"]),       y_top)]
    pygame.draw.polygon(window, colour["road"], points)

    top_rumble_width    = top["w"] / 6
    bottom_rumble_width = bottom["w"] / 6

    # Left rumble strip.
    points = [((bottom["x"] - bottom["w"] - top_rumble_width), y_bottom),
              ((bottom["x"] - bottom["w"]),                    y_bottom),
              ((top["x"] - top["w"]),                          y_top),
              ((top["x"] - top["w"] - top_rumble_width),       y_top)]
    pygame.draw.polygon(window, colour["rumble"], points)

    # Right rumble strip.
    points = [((bottom["x"] + bottom["w"] + bottom_rumble_width), y_bottom),
              ((bottom["x"] + bottom["w"]),                       y_bottom),
              ((top["x"] + top["w"]),                             y_top),
              ((top["x"] + top["w"] + bottom_rumble_width),       y_top)]
    pygame.draw.polygon(window, colour["rumble"], points)

    if (segment["index"] / s.RUMBLE_LENGTH) % 2 == 0:
        top_line_width    = (top["w"] / 32)
        bottom_line_width = (bottom["w"] / 32)
        
        # Road lane marker.
        points = [(bottom["x"],                           y_bottom),
                  ((bottom["x"] + bottom_line_width * 2), y_bottom),
                  ((top["x"] + top_line_width * 2),       y_top),
                  (top["x"],                              y_top)]
        pygame.draw.polygon(window, colour["line"], points)

def render_grass(window, segment):
    top       = segment["top"]["screen"]
    bottom    = segment["bottom"]["screen"]
    height    = top["y"] - bottom["y"]
    y         = s.DIMENSIONS[1] - top["y"]

    if height <= 1:
        pygame.draw.line(window, segment["colour"]["grass"], (0, y), (s.DIMENSIONS[0], y), 1)
    else:
        pygame.draw.rect(window, segment["colour"]["grass"], (0, y, s.DIMENSIONS[0], height))

def render_player(window, segment):
    pass
