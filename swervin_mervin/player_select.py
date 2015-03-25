import pygame, os
import settings as s
import util as u

class PlayerSelect():
    """Displays a player selection screen."""

    def __init__(self):
        self.selected = 0
        self.finished  = False
        self.font      = pygame.font.Font(s.FONTS["bladerunner"], 300)
        
    def progress(self, window):
        txt = str(self.selected)
        text = self.font.render(txt, 1, s.COLOURS["text"])

        for e in pygame.event.get():
            u.try_quit(e)

            if e.type == pygame.KEYDOWN: 
                if e.key == pygame.K_LEFT and self.selected > 0:
                    self.selected -= 1
                elif e.key == pygame.K_RIGHT and self.selected < len(s.PLAYERS) - 1:
                    self.selected += 1
                elif e.key == pygame.K_SPACE:
                    self.finished = True
 
        window.fill(s.COLOURS["black"])
        window.blit(text, (100, 100))
