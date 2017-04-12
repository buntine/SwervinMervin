import pygame
import settings as s

class WorldObject:
    """Represents a single renderable object in a level. Should always be subclassed."""

    def __init__(self, quant=3):
        self.rendered_area = 0
        self.quantifier    = quant

    def non_renderable(self):
        """Returns True if this object doesn't actually have a sprite that appears on
           screen (usually means it's only there for collision detection)."""
        return self.sprite["path"] == None

    def screen_dim(self, dimension, screen_pos):
        return int(self.sprite[dimension] * screen_pos * s.ROAD_WIDTH * self.quantifier)

    def render(self, window, segment):
        """Renders an object to the window with appropriate scaling, clipping, etc."""
        coords     = segment.bottom["screen"]
        s_width    = self.screen_dim("width", coords["s"])
        s_height   = self.screen_dim("height", coords["s"])
        x          = (coords["x"] - s_width) + (coords["w"] * self.offset)
        y          = s.DIMENSIONS[1] - coords["y"] - s_height
        top_clip   = s.DIMENSIONS[1] - segment.clip[1] - y
        left_clip  = 0 if not segment.in_tunnel else max(x, 0) - segment.clip[0]
        right_clip = 0 if not segment.in_tunnel else segment.clip[2]

        if right_clip > 0 and right_clip < (x + s_width):
            s_width -= int((x + s_width) - right_clip)

        if self.offset_y > 0:
            y -= (self.offset_y * 100000 * coords["s"])
 
        self.rendered_area = [x, x + s_width]

        if s_width > 0 and s_height > 0 and top_clip > 0 and\
           s_width < s.DIMENSIONS[0] * 2 and s_height < s.DIMENSIONS[1] * 2 and\
           (left_clip >= 0 or abs(left_clip) < s_width):

            if not self.non_renderable():
                offset_x = 0 if left_clip >= 0 else abs(left_clip)
                img      = self.path()
                img      = pygame.transform.scale(img, (s_width, s_height))
                window.blit(img, (x, y), (offset_x, 0, s_width, top_clip))
