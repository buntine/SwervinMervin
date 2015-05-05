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

    return text

def middle(surface, x_offset=0, y_offset=0, x=-1, y=-1):
    """Returns a tuple of X,Y coordinates that represents the center position for the given surface. 
       x_offset and y_offset will offset the appropriate axis by N pixels.
       Passing in a value for x or y will override the calculated value."""
    mx = x if x > -1 else ((s.DIMENSIONS[0] - surface.get_width()) / 2) + x_offset
    my = y if y > -1 else ((s.DIMENSIONS[1] - surface.get_height()) / 2) + y_offset

    return (mx, my)
