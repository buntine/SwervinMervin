import pygame
import settings as s

class TunnelInside:
    """Represents a Tunnel inside (walls, roof) polygon as we approach it."""

    def __init__(self):
        self.quantifier = 3

    def render(self, window, coords, clip, coverage):
        # Roof.
        s_width  = s.DIMENSIONS[0]
        s_height = int(s.TUNNEL_HEIGHT * coords["s"] * s.ROAD_WIDTH * self.quantifier)
        x        = 0
        y        = s.DIMENSIONS[1] - coords["y"] - s_height
        top_clip = s.DIMENSIONS[1] - coverage[1].top["screen"]["y"]

        s_height -= ((y + s_height) - top_clip)

        points = (x, y, s_width, s_height)
        pygame.draw.rect(window, s.COLOURS["tunnel"], points)

        # Left wall.
        l_bottom = coverage[0].bottom["screen"]

        if l_bottom["w"] < s.DIMENSIONS[0] and l_bottom["w"] > 0:
            ly_bottom = (s.DIMENSIONS[1] - l_bottom["y"])
            l_x       = l_bottom["x"] - l_bottom["w"]

            points = [(0, ly_bottom),
                      (l_x, ly_bottom),
                      (l_x, y),
                      (0, y)]
            pygame.draw.polygon(window, s.COLOURS["tunnel"], points)

        # Right wall.
        r_bottom = coverage[2].bottom["screen"]

        if r_bottom["w"] < s.DIMENSIONS[0] and r_bottom["w"] > 0:
            ry_bottom = (s.DIMENSIONS[1] - r_bottom["y"])
            r_x       = r_bottom["x"] + r_bottom["w"]

            points = [(r_x, ry_bottom),
                      (s.DIMENSIONS[0], ry_bottom),
                      (s.DIMENSIONS[0], y),
                      (r_x, y)]
            pygame.draw.polygon(window, s.COLOURS["tunnel"], points)
