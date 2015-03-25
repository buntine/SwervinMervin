import pygame, os
import settings as s

class PlayerSelect():
    """Displays a player selection screen."""

    def __init__(self):
        self.selected = 0
        self.finished  = False
        self.font      = pygame.font.Font(s.FONTS["bladerunner"], 300)
        
    def progress(self, window):
        self.finished = True
