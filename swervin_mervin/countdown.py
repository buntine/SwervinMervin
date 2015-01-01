import pygame, os
import settings as s

class CountDown():
    """Plays a countdown before the level starts."""

    def __init__(self):
        self.remaining = 3
        self.finished  = False
        self.font      = pygame.font.Font(s.FONTS["bladerunner"], 300)
        
    def progress(self, window):
        txt = str(self.remaining) if self.remaining > 0 else "GO"
        countdown_text = self.font.render(txt, 1, s.COLOURS["text"])
        x = (s.DIMENSIONS[0] - countdown_text.get_width()) / 2
        y = (s.DIMENSIONS[1] - countdown_text.get_height()) / 2

        window.fill(s.COLOURS["black"])
        window.blit(countdown_text, (x, y))

        freq = 440 if self.remaining > 0 else 570
        beep = pygame.mixer.Sound(os.path.join("lib", "%d.wav" % freq))

        beep.set_volume(0.2)
        beep.play()

        self.remaining -= 1

        if self.remaining < 0:
            self.finished = True
