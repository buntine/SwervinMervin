import pygame, os
import settings as s

class Background:
    """Represents a single scrollable background in a level."""

    def __init__(self, name, y, parallax_speed, convert=False):
        self.image          = pygame.image.load(os.path.join("lib", "{0}.png".format(name)))
        self.parallax_speed = parallax_speed
        self.y              = y
        self.width          = self.image.get_width()
        self.height         = self.image.get_height()
        self.curviture      = (self.width - s.DIMENSIONS[0]) / 2

        if convert:
            self.image = self.image.convert()

    def step(self, curve, speed_percent):
        """Moves the background one step to simulate turning."""
        c = self.curviture

        # Background is now completely off screen, so reset it.
        if c <= -self.width:
            self.curviture = c + self.width
        elif c >= self.width:
            self.curviture = (c - self.width) + (self.width - s.DIMENSIONS[0])

        self.curviture += (curve / self.parallax_speed) * speed_percent
    
    def render(self, window):
        """Draws the image to the window."""
        c = self.curviture
        w = s.DIMENSIONS[0]

        window.blit(self.image,
          (0, self.y),
          (c, 0, w, self.height))

        # FIll empty space on the left of the screen.
        if c < 0:
            window.blit(self.image,
              (0, self.y),
              (self.width + c, 0, -c, self.height))

        # FIll empty space on the right of the screen.
        elif c > (self.width - w):
            window.blit(self.image,
              (self.width - c, self.y),
              (0, 0, (c - (self.width - w)), self.height))
