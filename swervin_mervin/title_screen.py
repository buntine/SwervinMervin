import pygame, os
import settings as s

class TitleScreen():
    """Plays a title screen and waits for user to insert coin."""

    def __init__(self):
        self.finished   = False
        self.ready      = False
        self.background = pygame.image.load(os.path.join("lib", "title.png"))
        self.offset     = 0
        self.font       = pygame.font.Font(s.FONTS["computer"], 40)
        self.state      = 0
        self.frame      = 0
        
    def progress(self, window):
        self.frame += 1

        window.fill(s.COLOURS["black"])

        getattr(self, "state_{0}_step".format(self.state))(window)

    def state_0_step(self, window):
        w, h = s.DIMENSIONS
        colours = [(100, 100, 10), (130, 140, 10), (170, 180, 10)]

        window.blit(self.background, (0, 0), (0, self.offset, w, h))
        self.offset += 2

        pygame.draw.circle(window, colours[(self.frame / 3) % 3], (88, (h + 176) - self.offset), 3)
        pygame.draw.circle(window, colours[(self.frame / 3) % 3], (106, (h + 176) - self.offset), 3)
        pygame.draw.polygon(window, colours[(self.frame / 3) % 3], ((189, (h + 275) - self.offset), (189, (h + 245) - self.offset), (193, (h + 275) - self.offset), (193, (h + 245) - self.offset)))

        if self.offset + h >= self.background.get_height():
            self.state = 1

    def state_1_step(self, window):
        w, h = s.DIMENSIONS

        window.blit(self.background, (0, 0), (0, self.offset, w, h))
 
        self.state = 2

    def state_2_step(self, window):
        w, h = s.DIMENSIONS
        window.blit(self.background, (0, 0), (0, self.offset, w, h))

        if (self.frame / 17) % 2 == 1:
            self.ready = True

            ic = self.font.render("Insert Coin", 1, s.COLOURS["red"])
            x  = (w - ic.get_size()[0]) / 2
            y  = (h - ic.get_size()[1]) - 120

            window.blit(ic, (x, y))
