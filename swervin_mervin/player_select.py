import pygame, os
import settings as s
import util as u

class PlayerSelect():
    """Displays a player selection screen."""

    def __init__(self):
        self.selected         = 0
        self.finished         = False
        self.player_chosen    = False
        self.selection_colour = 0
        self.background       = pygame.image.load(os.path.join("lib", "player_select.png"))
        self.fonts            = {"title": pygame.font.Font(s.FONTS["fipps"], 38),
                                 "name": pygame.font.Font(s.FONTS["retro_computer"], 18),
                                 "details": pygame.font.Font(s.FONTS["retro_computer"], 12),
                                 "stats": pygame.font.Font(s.FONTS["retro_computer"], 8)}
        
    def progress(self, window):
        txt_title     = self.fonts["title"].render("Player Select", 1, s.COLOURS["text"])
        player        = s.PLAYERS[self.selected]
        lpad          = 40
        start_point   = (s.DIMENSIONS[0] / 2) + (lpad / 2)
        step          = player["sprites"]["mugshot_small"]["width"]
        large_mugshot = pygame.image.load(os.path.join("lib", player["sprites"]["mugshot_large"]["path"]))

        self.selection_colour = 1 if self.selection_colour == 0 else 0

        window.blit(self.background, (0, 0))
        window.blit(txt_title, ((s.DIMENSIONS[0] / 2) - (txt_title.get_size()[0] / 2), 10))

        for i, p in enumerate(s.PLAYERS):
            details = p["sprites"]["mugshot_small"]
            mugshot = pygame.image.load(os.path.join("lib", details["path"]))
            x       = start_point + (i * (step + lpad))
            y       = 120

            window.blit(mugshot, (x, y))

            if i == self.selected:
                bw = 10
                pygame.draw.rect(window, 
                  s.COLOURS["selection"][self.selection_colour],
                  [x - (bw / 2), y - (bw / 2), details["width"] + bw, details["width"] + bw], bw)

        # Player name and picture.
        window.blit(large_mugshot, (0, s.DIMENSIONS[1] - player["sprites"]["mugshot_large"]["height"]))
        window.blit(self.fonts["name"].render(player["name"], 1, s.COLOURS["text"]), (start_point - bw, 200))
        window.blit(self.fonts["details"].render(player["city"], 1, s.COLOURS["text"]), (start_point - bw, 228))

        # Player stats.
        desired_acceleration = int(self.normalise(player["acceleration_factor"], *s.HARD_ACCELERATION) * 155)
        desired_handling = int((1.0 - self.normalise(player["centrifugal_force"], *s.HARD_HANDLING)) * 155)
        desired_top_speed = int(self.normalise(player["top_speed"], *s.HARD_TOP_SPEED) * 155)

        window.blit(self.fonts["stats"].render("Acceleration", 1, s.COLOURS["text"]), (start_point - bw, 290))
        window.blit(self.fonts["stats"].render("Handling", 1, s.COLOURS["text"]), (start_point - bw, 314))
        window.blit(self.fonts["stats"].render("Speed", 1, s.COLOURS["text"]), (start_point - bw, 338))

        su = pygame.Surface((155, 18), pygame.SRCALPHA)
        su.fill(s.COLOURS["opaque_white"])

        window.blit(su, (start_point + 105, 285))
        window.blit(su, (start_point + 105, 309))
        window.blit(su, (start_point + 105, 333))

        pygame.draw.rect(window, 
          s.COLOURS["text"],
          [start_point + 105, 285, desired_acceleration, 18])

        pygame.draw.rect(window, 
          s.COLOURS["text"],
          [start_point + 105, 309, desired_handling, 18])

        pygame.draw.rect(window, 
          s.COLOURS["text"],
          [start_point + 105, 333, desired_top_speed, 18])

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
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue

        self.finished = True

    def normalise(self, v, low, high):
        return (v - low) / (high - low)
