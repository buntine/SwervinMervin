from pygame.font import Font

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
