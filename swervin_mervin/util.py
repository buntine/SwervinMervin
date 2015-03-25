import pygame, sys
from pygame.locals import *
from pygame.font import Font
import settings as s

def try_quit(e):
    if e.type == QUIT or\
      (e.type == pygame.KEYDOWN and\
       e.key == pygame.K_ESCAPE and\
       s.FULLSCREEN):
        pygame.quit()
        sys.exit()

def limit(v, low, high):
    """Returns v, limited to low/high threshold"""
    if v < low:
        return low
    elif v > high:
        return high
    else:
        return v

def render_text(text, window, font, color, position):
    """Renders a font and blits it to the given window"""
    text = font.render(text, 1, color)

    window.blit(text, position)
