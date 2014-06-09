# Helper functions for rendering.

import pygame

def segment_pointlist(segment):
    top    = segment["top"]["screen"]
    bottom = segment["bottom"]["screen"]

    return [((bottom["x"] - bottom["w"]), (480 - bottom["y"])),
            ((bottom["x"] + bottom["w"]), (480 - bottom["y"])),
            ((top["x"] + top["w"]), (480 - top["y"])),
            ((top["x"] - top["w"]), (480 - top["y"]))]

def render_grass(window, segment):
    top       = segment["top"]["screen"]
    bottom    = segment["bottom"]["screen"]
    height    = (top["y"] - bottom["y"])

    pygame.draw.rect(window, segment["colour"]["grass"], (0, (480 - top["y"]), 640, height))

def render_player():
    pass
