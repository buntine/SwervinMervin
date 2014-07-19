import pygame, os, sys
from pygame.locals import *
import settings as s

class TitleScreen():
    """Plays a title screen and waits for user to insert coin."""

    # This class is horrible.
    # Maybe one day I'll fix it.
    # And then again... Maybe I won't.

    def __init__(self, window):
        self.background = pygame.image.load(os.path.join("lib", "title.png"))
        self.logo_a     = pygame.image.load(os.path.join("lib", "title_swervin.png"))
        self.logo_b     = pygame.image.load(os.path.join("lib", "title_mervin.png"))
        self.font       = pygame.font.Font(s.FONTS["arcade"], 22)
        self.fps_clock  = pygame.time.Clock()
        self.window     = window

    def setup(self):
        """Resets the title screen"""
        self.finished   = False
        self.ready      = False
        self.bg_offset  = 0
        self.state      = 0
        self.frame      = 0
        self.logo_a_off = -420
        self.logo_b_off = s.DIMENSIONS[0] - 100

        pygame.mixer.music.load(os.path.join("lib", "mn84-theme.mp3"))
        pygame.mixer.music.play(-1)

    def progress(self):
        """Animates the next frame"""
        self.frame += 1

        self.window.fill(s.COLOURS["black"])

        self.__state_0_step()
        self.__state_1_step()
        self.__state_2_step()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.ready:
                    pygame.mixer.music.fadeout(1500)
                    self.finished = True
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        self.fps_clock.tick(s.TITLE_FPS)

    def __state_0_step(self):
        w, h = s.DIMENSIONS
        colours = [(100, 100, 10), (120, 130, 10), (150, 160, 10), (170, 180, 10), (190, 200, 10)]
        colour  = colours[(self.frame / 5) % 5]

        self.window.blit(self.background, (0, 0), (0, self.bg_offset, w, h))

        pygame.draw.circle(self.window, colour, (88, (h + 176) - self.bg_offset), 3)
        pygame.draw.circle(self.window, colour, (106, (h + 176) - self.bg_offset), 3)
        pygame.draw.circle(self.window, colour, (287, (h + 397) - self.bg_offset), 3)
        pygame.draw.circle(self.window, colour, (357, (h + 397) - self.bg_offset), 3)
        pygame.draw.circle(self.window, colour, (492, (h + 236) - self.bg_offset), 3)
        pygame.draw.circle(self.window, colour, (501, (h + 233) - self.bg_offset), 3)
        pygame.draw.circle(self.window, colour, (506, (h + 234) - self.bg_offset), 3)
        pygame.draw.circle(self.window, colour, (603, (h + 192) - self.bg_offset), 3)
        pygame.draw.polygon(self.window, colour,
          ((189, (h + 273) - self.bg_offset),
           (189, (h + 243) - self.bg_offset),
           (193, (h + 273) - self.bg_offset),
           (193, (h + 243) - self.bg_offset)))

        if self.state == 0:
            if self.bg_offset + h >= self.background.get_height():
                self.state = 1
            else:
                self.bg_offset += 2

    def __state_1_step(self):
        if not self.state == 0:
            center_a = ((s.DIMENSIONS[0] - self.logo_a.get_width()) / 2) - 34
            center_b = ((s.DIMENSIONS[0] - self.logo_b.get_width()) / 2) - 34

            self.window.blit(self.logo_b, (self.logo_b_off, 130))
            self.window.blit(self.logo_a, (self.logo_a_off, 34))

            if self.state == 1: 
                if self.logo_a_off < center_a:
                    self.logo_a_off += 10
                elif self.logo_b_off > center_b:
                    self.logo_b_off -= 10
                else:
                    self.state = 2
    
    def __state_2_step(self):
        if self.state == 2:
            w, h = s.DIMENSIONS

            if (self.frame / 20) % 2 == 1:
                self.ready = True

                ic = self.font.render("Insert Coin", 1, s.COLOURS["red"])
                x  = (w - ic.get_size()[0]) / 2
                y  = (h - ic.get_size()[1]) - 120

                self.window.blit(ic, (x, y))
