import settings as s
import pygame

class WorldObject:
    """Represents a single renderable object in a level. Should always be subclassed."""

    def render(self, window, coords, clip):
        """Renders an object to the window with appropriate scaling, etc."""
        s_width   = int(self.sprite["width"] * coords["s"] * s.ROAD_WIDTH * self.quantifier)
        s_height  = int(self.sprite["height"] * coords["s"] * s.ROAD_WIDTH * self.quantifier)
        x         = (coords["x"] - s_width) + (coords["w"] * self.offset)
        y         = s.DIMENSIONS[1] - coords["y"] - s_height
        clip_line = (s.DIMENSIONS[1] - clip) - y

        if s_width > 0 and s_height > 0 and clip_line > 0 and\
           s_width < s.DIMENSIONS[0] * 2 and s_height < s.DIMENSIONS[1] * 2:
            img = self.path()
            img = pygame.transform.scale(img, (s_width, s_height))

            window.blit(img, (x, y), (0, 0, s_width, clip_line))
