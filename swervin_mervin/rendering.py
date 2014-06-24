# Helper functions for rendering.

import pygame
import settings as s

def render_background(window, offset):
    bg = pygame.image.load("lib/city.png")
    x  = (500 - (s.DIMENSIONS[0] / 2)) + offset

    window.blit(bg, (0, 80), (x, 0, s.DIMENSIONS[0], 200))
