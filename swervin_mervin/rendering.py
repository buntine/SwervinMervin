# Helper functions for rendering.

import pygame

def render_road(window, segment, dimensions, rumble_length):
    top    = segment["top"]["screen"]
    bottom = segment["bottom"]["screen"]

    # Road.
    points = [((bottom["x"] - bottom["w"]), (dimensions[1] - bottom["y"])),
              ((bottom["x"] + bottom["w"]), (dimensions[1] - bottom["y"])),
              ((top["x"] + top["w"]), (dimensions[1] - top["y"])),
              ((top["x"] - top["w"]), (dimensions[1] - top["y"]))]
    pygame.draw.polygon(window, segment["colour"]["road"], points)

    # Rumble strip.
    left_rumble_width  = top["w"] / 6
    right_rumble_width = bottom["w"] / 6

    points = [((bottom["x"] - bottom["w"] - left_rumble_width), (dimensions[1] - bottom["y"])),
              ((bottom["x"] - bottom["w"]), (dimensions[1] - bottom["y"])),
              ((top["x"] - top["w"]), (dimensions[1] - top["y"])),
              ((top["x"] - top["w"] - left_rumble_width), (dimensions[1] - top["y"]))]

    pygame.draw.polygon(window, segment["colour"]["rumble"], points)

    points = [((bottom["x"] + bottom["w"] + right_rumble_width), (dimensions[1] - bottom["y"])),
              ((bottom["x"] + bottom["w"]), (dimensions[1] - bottom["y"])),
              ((top["x"] + top["w"]), (dimensions[1] - top["y"])),
              ((top["x"] + top["w"] + right_rumble_width), (dimensions[1] - top["y"]))]

    pygame.draw.polygon(window, segment["colour"]["rumble"], points)

    if (segment["index"] / rumble_length) % 2 == 0:
        bottom_line_width = (bottom["w"] / 32)
        top_line_width    = (top["w"] / 32)
        
        points = [(bottom["x"], (dimensions[1] - bottom["y"])),
                  ((bottom["x"] + bottom_line_width * 2), (dimensions[1] - bottom["y"])),
                  ((top["x"] + top_line_width * 2), (dimensions[1] - top["y"])),
                  (top["x"], (dimensions[1] - top["y"]))]
                  
        pygame.draw.polygon(window, segment["colour"]["line"], points)


def render_grass(window, segment, dimensions):
    top       = segment["top"]["screen"]
    bottom    = segment["bottom"]["screen"]
    height    = (top["y"] - bottom["y"])
    y         = (dimensions[1] - top["y"])

    if height <= 1:
        pygame.draw.line(window, segment["colour"]["grass"], (0, y), (dimensions[0], y), 1)
    else:
        pygame.draw.rect(window, segment["colour"]["grass"], (0, y, dimensions[0], height))

def render_player(window, segment, dimensions):
    pass
