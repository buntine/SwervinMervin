import pygame, os
import settings as s
import util as u

class PlayerSelect():
    """Displays a player selection screen."""

    def __init__(self):
        self.selected   = 0
        self.finished   = False
        self.fonts      = {"title": pygame.font.Font(s.FONTS["retro_computer"], 38),
                           "name": pygame.font.Font(s.FONTS["retro_computer"], 22),
                           "details": pygame.font.Font(s.FONTS["retro_computer"], 14),
                           "stats": pygame.font.Font(s.FONTS["retro_computer"], 12)}
        self.background = pygame.image.load(os.path.join("lib", "player_select.png"))
        
    def progress(self, window):
        txt_title = self.fonts["title"].render("Player Select", 1, s.COLOURS["text"])
        player    = s.PLAYERS[self.selected]
 
        window.blit(self.background, (0, 0))
        window.blit(txt_title, ((s.DIMENSIONS[0] / 2) - (txt_title.get_size()[0] / 2), 10))

        lpad        = 40
        start_point = (s.DIMENSIONS[0] / 2) + (lpad / 2)
        step        = player["sprites"]["mugshot_small"]["width"]
        for i, p in enumerate(s.PLAYERS):
            mugshot = pygame.image.load(os.path.join("lib", p["sprites"]["mugshot_small"]["path"]))
            x       = start_point + (i * (step + lpad))
            y       = 120

            window.blit(mugshot, (x, y))

        large_mugshot = pygame.image.load(os.path.join("lib", player["sprites"]["mugshot_large"]["path"]))
        window.blit(large_mugshot, (0, s.DIMENSIONS[1] - player["sprites"]["mugshot_large"]["height"]))

        txt_name = self.fonts["name"].render(player["name"], 1, s.COLOURS["text"])
        txt_city = self.fonts["details"].render(player["city"], 1, s.COLOURS["text"])
        window.blit(txt_name, (start_point, 200))
        window.blit(txt_city, (start_point, 228))

        for e in pygame.event.get():
            u.try_quit(e)

            if e.type == pygame.KEYDOWN: 
                if e.key == pygame.K_LEFT and self.selected > 0:
                    self.selected -= 1
                elif e.key == pygame.K_RIGHT and self.selected < len(s.PLAYERS) - 1:
                    self.selected += 1
                elif e.key == pygame.K_RETURN:
                    self.finished = True
