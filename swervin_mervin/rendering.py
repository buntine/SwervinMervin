# Helper functions for rendering.

import pygame

def render_road(window, segment, dimensions):
    top    = segment["top"]["screen"]
    bottom = segment["bottom"]["screen"]

    # Road.
    points = [((bottom["x"] - bottom["w"]), (dimensions[1] - bottom["y"])),
              ((bottom["x"] + bottom["w"]), (dimensions[1] - bottom["y"])),
              ((top["x"] + top["w"]), (dimensions[1] - top["y"])),
              ((top["x"] - top["w"]), (dimensions[1] - top["y"]))]
    pygame.draw.polygon(window, segment["colour"]["road"], points)

    # Rumble strip.
    if (segment["index"] / 3) % 2 > 0:
        points = [((bottom["x"] - bottom["w"] + 20), (dimensions[1] - bottom["y"])),
                  ((bottom["x"] - bottom["w"]), (dimensions[1] - bottom["y"])),
                  ((top["x"] - top["w"]), (dimensions[1] - top["y"])),
                  ((top["x"] - top["w"] + 20), (dimensions[1] - top["y"]))]

        pygame.draw.polygon(window, segment["colour"]["rumble"], points)

        points = [((bottom["x"] + bottom["w"] - 20), (dimensions[1] - bottom["y"])),
                  ((bottom["x"] + bottom["w"]), (dimensions[1] - bottom["y"])),
                  ((top["x"] + top["w"]), (dimensions[1] - top["y"])),
                  ((top["x"] + top["w"] - 20), (dimensions[1] - top["y"]))]

        pygame.draw.polygon(window, segment["colour"]["rumble"], points)



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
