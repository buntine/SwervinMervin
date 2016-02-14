import pygame
import settings as s

class TunnelEntrance:
    """Represents a Tunnel Entrance polygon as we approach it."""

    def __init__(self, colour):
        self.quantifier = 3
        self.colour     = colour

    def render(self, window, segment):
        coords     = segment.bottom["screen"]
        s_width    = s.DIMENSIONS[0]
        s_height   = int(s.TUNNEL_HEIGHT * coords["s"] * s.ROAD_WIDTH * self.quantifier)
        x          = 0
        y          = s.DIMENSIONS[1] - coords["y"] - s_height
        top_clip   = s.DIMENSIONS[1] - segment.clip[1] - y

        #  Player can see the tunnel approaching.
        if top_clip > 0:
            e_height = int(s_height * 0.7)
            surf     = pygame.Surface([s_width, s_height], pygame.SRCALPHA, 32)
            surf     = surf.convert_alpha()
            points   = [(s_width, s_height),
                        (coords["x"] + coords["w"], s_height),
                        (coords["x"] + coords["w"], s_height - e_height),
                        (coords["x"] - coords["w"], s_height - e_height),
                        (coords["x"] - coords["w"], s_height),
                        (0, s_height),
                        (0, 0),
                        (s_width, 0)] 

            pygame.draw.polygon(surf, self.colour, points)
            window.blit(surf, (x, y), (0, 0, s_width, top_clip))
