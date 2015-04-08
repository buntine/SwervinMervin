import pygame, os
import settings as s
import util as u

class PlayerSelect():
    """Displays a player selection screen."""

    def __init__(self):
        self.selected   = 0
        self.finished   = False
        self.player_chosen = False
        self.background = pygame.image.load(os.path.join("lib", "player_select.png"))
        self.fonts      = {"title": pygame.font.Font(s.FONTS["fipps"], 38),
                           "name": pygame.font.Font(s.FONTS["retro_computer"], 18),
                           "details": pygame.font.Font(s.FONTS["retro_computer"], 12),
                           "stats": pygame.font.Font(s.FONTS["retro_computer"], 10)}
        
    def progress(self, window):
        txt_title     = self.fonts["title"].render("Player Select", 1, s.COLOURS["text"])
        player        = s.PLAYERS[self.selected]
        lpad          = 40
        start_point   = (s.DIMENSIONS[0] / 2) + (lpad / 2)
        step          = player["sprites"]["mugshot_small"]["width"]
        large_mugshot = pygame.image.load(os.path.join("lib", player["sprites"]["mugshot_large"]["path"]))

        window.blit(self.background, (0, 0))
        window.blit(txt_title, ((s.DIMENSIONS[0] / 2) - (txt_title.get_size()[0] / 2), 10))

        for i, p in enumerate(s.PLAYERS):
            mugshot = pygame.image.load(os.path.join("lib", p["sprites"]["mugshot_small"]["path"]))
            x       = start_point + (i * (step + lpad))
            y       = 120

            window.blit(mugshot, (x, y))

        window.blit(large_mugshot, (0, s.DIMENSIONS[1] - player["sprites"]["mugshot_large"]["height"]))
        window.blit(self.fonts["name"].render(player["name"], 1, s.COLOURS["text"]), (start_point, 200))
        window.blit(self.fonts["details"].render(player["city"], 1, s.COLOURS["text"]), (start_point, 228))

        if self.player_chosen:
            self.finalise_selection(player)

        for e in pygame.event.get():
            u.try_quit(e)

            if e.type == pygame.KEYDOWN and not self.player_chosen:
                if e.key == pygame.K_LEFT and self.selected > 0:
                    self.selected -= 1
                elif e.key == pygame.K_RIGHT and self.selected < len(s.PLAYERS) - 1:
                    self.selected += 1
                elif e.key == pygame.K_RETURN:
                    self.player_chosen = True

    def finalise_selection(self, player):
        pygame.mixer.music.load(os.path.join("lib", player["select_sfx"]))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue

        self.finished = True
