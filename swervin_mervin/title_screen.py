import pygame, os
import settings as s
import util as u

class TitleScreen():
    """Plays a title screen and waits for user to insert coin."""

    def __init__(self):
        self.finished   = False
        self.ready      = False
        self.background = pygame.image.load(os.path.join("lib", "title.png"))
        self.logo_a     = pygame.image.load(os.path.join("lib", "title_swervin.png"))
        self.logo_b     = pygame.image.load(os.path.join("lib", "title_mervin.png"))
        self.bg_offset  = 0
        self.font       = pygame.font.Font(s.FONTS["retro_computer"], 22)
        self.state      = 0
        self.frame      = 0
        self.logo_a_off = -420
        self.logo_b_off = s.DIMENSIONS[0]
        
    def progress(self, window):
        self.frame += 1

        window.fill(s.COLOURS["black"])

        self.state_0_step(window)
        self.state_1_step(window)
        self.state_2_step(window)

        for e in pygame.event.get():
            u.try_quit(e)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN and self.ready:
                pygame.mixer.music.fadeout(1500)
                self.finished = True

    def state_0_step(self, window):
        w, h = s.DIMENSIONS
        colours = [(100, 100, 10), (120, 130, 10), (150, 160, 10), (170, 180, 10), (190, 200, 10)]
        colour  = colours[(self.frame / 5) % 5]

        window.blit(self.background, (0, 0), (0, self.bg_offset, w, h))

        pygame.draw.circle(window, colour, (88, (h + 176) - self.bg_offset), 3)
        pygame.draw.circle(window, colour, (106, (h + 176) - self.bg_offset), 3)
        pygame.draw.circle(window, colour, (287, (h + 397) - self.bg_offset), 3)
        pygame.draw.circle(window, colour, (357, (h + 397) - self.bg_offset), 3)
        pygame.draw.circle(window, colour, (492, (h + 236) - self.bg_offset), 3)
        pygame.draw.circle(window, colour, (501, (h + 233) - self.bg_offset), 3)
        pygame.draw.circle(window, colour, (506, (h + 234) - self.bg_offset), 3)
        pygame.draw.circle(window, colour, (603, (h + 192) - self.bg_offset), 3)
        pygame.draw.polygon(window, colour,
          ((189, (h + 273) - self.bg_offset),
           (189, (h + 243) - self.bg_offset),
           (193, (h + 273) - self.bg_offset),
           (193, (h + 243) - self.bg_offset)))

        if self.state == 0:
            if self.bg_offset + h >= self.background.get_height():
                self.state = 1
            else:
                self.bg_offset += 2

    def state_1_step(self, window):
        if not self.state == 0:
            center_a = ((s.DIMENSIONS[0] - self.logo_a.get_width()) / 2)
            center_b = ((s.DIMENSIONS[0] - self.logo_b.get_width()) / 2)

            window.blit(self.logo_b, (self.logo_b_off, 158))
            window.blit(self.logo_a, (self.logo_a_off, 34))

            if self.state == 1: 
                if self.logo_a_off < center_a:
                    self.logo_a_off += 10
                elif self.logo_b_off > center_b:
                    self.logo_b_off -= 10
                else:
                    self.state = 2
    
    def state_2_step(self, window):
        if self.state == 2:
            w, h = s.DIMENSIONS

            if (self.frame / 20) % 2 == 1:
                self.ready = True

                ic = self.font.render("Press Start", 1, s.COLOURS["red"])
                x  = (w - ic.get_size()[0]) / 2
                y  = (h - ic.get_size()[1]) - 120

                window.blit(ic, (x, y))
