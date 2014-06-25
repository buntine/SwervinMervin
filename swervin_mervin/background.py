import pygame
import settings as s

class Background:
    """Represents a single scrollable background in a level."""

    def __init__(self, name, y, parallax_speed):
        self.image          = pygame.image.load("lib/{0}.png".format(name))
        self.parallax_speed = parallax_speed
        self.y              = y

        self.width          = self.image.get_width()
        self.height         = self.image.get_height()
        self.curviture      = (self.width - s.DIMENSIONS[0]) / 2

    def step(self, curve, speed_percent):
        """Moves the background one step to simulate turning."""
        self.curviture += (curve / self.parallax_speed) * speed_percent
    
    def render(self, window):
        """Draws the image to the window."""
        window.blit(self.image,
          (0, self.y),
          (self.curviture, 0, s.DIMENSIONS[0], self.height))
