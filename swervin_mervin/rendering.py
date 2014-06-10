# Helper functions for rendering.

import pygame
import settings as s

def render_road(window, segment):
    """Renders the polygons for the road, markers, etc."""
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

    top_rumble_width    = top["w"] / (s.LANES * 2)
    bottom_rumble_width = bottom["w"] / (s.LANES * 2)

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
       
        # Road lane marker(s).
        top_line_width    = (top["w"] / (s.LANES * 8))
        bottom_line_width = (bottom["w"] / (s.LANES * 8))
        lane_top_w        = top["w"] / s.LANES
        lane_bottom_w     = bottom["w"] / s.LANES

        for lane in range(s.LANES - 1):
            lane_bottom_w *= 2
            lane_top_w    *= 2
            bottom_left    = (bottom["x"] - bottom["w"] + lane_bottom_w)
            bottom_right   = bottom_left + bottom_line_width
            top_left       = (top["x"] - top["w"] + lane_top_w)
            top_right      = top_left + top_line_width

            points = [(bottom_left,  y_bottom),
                      (bottom_right, y_bottom),
                      (top_right,    y_top),
                      (top_left,     y_top)]
            pygame.draw.polygon(window, colour["line"], points)

def render_grass(window, segment):
    """Renders grass strip for the given segment"""
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
