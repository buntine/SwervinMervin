import pygame
import settings as s

class TunnelEntrance:
    """Represents a Tunnel Entrance polygon."""

    def __init__(self):
        self.quantifier = 3

    def render(self, window, coords, clip):
        s_width    = s.DIMENSIONS[0]
        s_height   = int(120 * coords["s"] * s.ROAD_WIDTH * self.quantifier)
        x          = 0
        y          = s.DIMENSIONS[1] - coords["y"] - s_height
        top_clip   = s.DIMENSIONS[1] - clip[1] - y

        if top_clip > 0:
            pygame.draw.rect(window, s.COLOURS["black"],
              (x, y, s_width, s_height))

#        if self.offset_y > 0:
#            y -= (self.offset_y * 100000 * coords["s"])
 
#        if s_width > 0 and s_height > 0 and top_clip > 0 and\
#           s_width < s.DIMENSIONS[0] * 2 and s_height < s.DIMENSIONS[1] * 2 and\
#           (left_clip >= 0 or abs(left_clip) < s_width):
#            img      = self.path()
#            img      = pygame.transform.scale(img, (s_width, s_height))
#            offset_x = 0 if left_clip >= 0 else abs(left_clip)
#
#            window.blit(img, (x, y), (offset_x, 0, s_width, top_clip))
