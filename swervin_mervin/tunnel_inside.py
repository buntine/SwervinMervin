import pygame
import settings as s

class TunnelInside:
    """Represents a Tunnel inside (walls, roof) polygon as we approach it."""

    def __init__(self):
        self.quantifier = 3

    def render(self, window, coords, clip, full_clip):
        s_width  = s.DIMENSIONS[0]
        s_height = int(s.TUNNEL_HEIGHT * coords["s"] * s.ROAD_WIDTH * self.quantifier)
        x        = 0
        y        = s.DIMENSIONS[1] - coords["y"] - s_height
        top_clip = s.DIMENSIONS[1] - full_clip[1]

        s_height -= ((y + s_height) - top_clip)

        points = (x, y, s_width, s_height)
        pygame.draw.rect(window, s.COLOURS["tunnel"], points)
