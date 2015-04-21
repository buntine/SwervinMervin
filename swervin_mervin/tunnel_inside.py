import pygame
import settings as s

class TunnelEntrance:
    """Represents a Tunnel inside (walls, roof) polygon as we approach it."""

    def __init__(self):
        self.quantifier = 3

    def render(self, window, coords, clip):
        s_width  = s.DIMENSIONS[0]
        s_height = int(s.TUNNEL_HEIGHT * coords["s"] * s.ROAD_WIDTH * self.quantifier)
        x        = 0
        y        = s.DIMENSIONS[1] - coords["y"] - s_height
        top_clip = s.DIMENSIONS[1] - clip[1] - y

        if top_clip > 0:
            points = (x, y, s_width, s_height - top_clip)

            pygame.draw.rect(window, s.COLOURS["tunnel"], points)
