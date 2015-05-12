import pygame, os
import util as u
import settings as s

class CountDown():
    """Plays a countdown before the level starts."""

    def __init__(self, level_number, level_name):
        self.level_number = level_number
        self.level_name   = level_name
        self.remaining    = 3
        self.remaining    = 3
        self.finished     = False
        self.text_font    = pygame.font.Font(s.FONTS["retro_computer"], 20)
        self.cd_font      = pygame.font.Font(s.FONTS["retro_computer"], 250)
        
    def progress(self, window):
        txt        = str(self.remaining) if self.remaining > 0 else "GO"
        cd_text    = self.cd_font.render(txt, 1, s.COLOURS["text"])
        level_text = self.text_font.render("Level %d: %s" % (self.level_number, self.level_name), 1, s.COLOURS["text"])
        freq       = 440 if self.remaining > 0 else 570
        beep       = pygame.mixer.Sound(os.path.join("lib", "%d.wav" % freq))

        window.fill(s.COLOURS["black"])
        window.blit(level_text, u.middle(level_text, y=25))
        window.blit(cd_text, u.middle(cd_text, y_offset=(level_text.get_height())))

        beep.set_volume(0.6)
        beep.play()

        self.remaining -= 1

        if self.remaining < 0:
            self.finished = True
