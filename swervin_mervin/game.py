import pygame, sys, os, math, random
from pygame.locals import *
import player as p
import background as b
import level as l
import title_screen as ts
import countdown as cd
import player_select as ps
import settings as s
import high_scores as hs

class Game:
    """Represents the game flow."""

    def __init__(self, window, clock):
        self.window          = window
        self.clock           = clock
        self.paused          = False
        self.waiting         = False
        self.selected_player = 0
        self.player          = None
        self.level           = None
        self.backgrounds     = None
        self.high_scores     = hs.HighScores()

    def play(self):
        if s.TITLE_SCREEN:
            self.__title_screen()

        if s.PLAYER_SELECT:
            self.__player_select()

        if s.COUNTDOWN:
            self.__countdown()

        self.player      = p.Player(self.high_scores.minimum_score(), self.selected_player)
        self.level       = l.Level("melbourne")
        self.backgrounds = [b.Background("sky", 0, 2, True),
                            b.Background("city", 0, 1)]

        self.level.build()

        pygame.mixer.music.load(os.path.join("lib", "lazerhawk-overdrive.ogg"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(s.MUSIC_VOLUME)

        while self.player.alive():
            if self.paused:
                self.__pause_cycle()
            else:
                self.__game_cycle()

            pygame.display.update()
            self.clock.tick(s.FPS)

        ## Post-game high scores and wait for new player.
        if self.high_scores.is_high_score(self.player.points):
            self.high_scores.add_high_score(math.trunc(self.player.points))

        pygame.mixer.music.fadeout(1500)
        self.waiting = True

    def wait(self):
        """Shows high scores until a new player is ready."""

        heading_font = pygame.font.Font(s.FONTS["bladerunner"], 44)
        content_font = pygame.font.Font(s.FONTS["arcade"], 15)
        background   = pygame.image.load(os.path.join("lib", "title.png"))
        heading_text = heading_font.render("High Scores", 1, s.COLOURS["text"])
        y            = 100

        self.window.fill(s.COLOURS["black"])
        self.window.blit(background, (0, 0))
        self.window.blit(heading_text, (30, 30))

        for score in self.high_scores.high_scores:
            date_text  = content_font.render(score[0].strftime("%d %b %Y"), 1, s.COLOURS["text"])
            score_text = content_font.render(str(score[1]), 1, s.COLOURS["text"])

            self.window.blit(date_text, (30, y))
            self.window.blit(score_text, (230, y))
            y += 35

        pygame.display.update()

        while self.waiting:
            for e in pygame.event.get():
                self.__try_quit(e)

                if e.type == KEYDOWN and e.key in [K_UP, K_SPACE]:
                    self.waiting = False
     
            self.clock.tick(s.FPS)

    def __game_cycle(self):
        p = self.player
        l = self.level

        p.travel(l.track_length(), self.window)

        base_segment   = l.find_segment(p.position)
        player_segment = l.find_segment(p.position + s.PLAYER_Z)

        p.accelerate()
        p.steer(player_segment)
        p.climb(base_segment)
        p.detect_collisions(player_segment)
        p.handle_crash()

        # Sprinkle some random bonuses into the next lap if we are lucky.
        if p.new_lap:
            if random.randint(1, s.CHANCE_OF_BONUSES) == 1:
                l.insert_bonuses()

        # Move the other players.
        for c in l.competitors:
            old_seg = l.find_segment(c.position)
            c.travel(l.track_length())
            new_seg = l.find_segment(c.position)

            c.play_engine(p.position)

            if old_seg.index != new_seg.index:
                if c in old_seg.competitors:
                    old_seg.competitors.remove(c)
                new_seg.competitors.append(c)

        y_coverage  = 0
        curve       = 0
        curve_delta = -(base_segment.curve * p.segment_percent())

        # Position backgrounds according to current curve.
        for bg in self.backgrounds:
            if base_segment.curve != 0:
                bg.step(base_segment.curve, p.speed_percent())
            bg.render(self.window)

        # Loop through segments we should draw for this frame.
        for i in range(s.DRAW_DISTANCE):
            segment            = l.offset_segment(base_segment.index + i)
            projected_position = p.position
            camera_x           = p.x * s.ROAD_WIDTH

            # Past end of track and looped back.
            if segment.index < base_segment.index:
                projected_position -= l.track_length()

            segment.project(camera_x,
              curve,
              curve_delta,
              projected_position,
              p.y)

            curve       += curve_delta
            curve_delta += segment.curve

            # Remember highest Y coordinate so we can clip sprites later.
            segment.clip = y_coverage

            if segment.should_ignore(y_coverage):
                continue

            segment.render_grass(self.window)
            segment.render_road(self.window)

            if (segment.top["screen"]["y"] > y_coverage):
                y_coverage = segment.top["screen"]["y"]

        # Draw sprites in from back to front (painters algorithm).
        if segment.index != base_segment.index:
            for i in reversed(range(1, s.SPRITE_DRAW_DISTANCE)):
                segment = l.offset_segment(base_segment.index + i)
                segment.render_world_objects(self.window)

            p.render(self.window, base_segment)
            p.render_hud(self.window)

            if p.blood_alpha > 0:
                p.render_blood(self.window)

        for e in pygame.event.get():
            self.__try_quit(e)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                pygame.mixer.music.pause()
                self.paused = True

        # Steering, acceleration.
        keys = pygame.key.get_pressed()
        p.set_acceleration(keys)
        p.set_direction(keys)

    def __pause_cycle(self):
        pause_font = pygame.font.Font(s.FONTS["bladerunner"], 64)
        pause_text = pause_font.render("Paused", 1, s.COLOURS["text"])
        x          = (s.DIMENSIONS[0] - pause_text.get_width()) / 2
        y          = (s.DIMENSIONS[1] - pause_text.get_height()) / 2

        self.window.fill(s.COLOURS["black"])
        self.window.blit(pause_text, (x, y))

        for e in pygame.event.get():
            self.__try_quit(event)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                pygame.mixer.music.unpause()
                self.paused = False

    def __title_screen(self):
        title_screen = ts.TitleScreen()
        pygame.mixer.music.load(os.path.join("lib", "mn84-theme.ogg"))
        pygame.mixer.music.play(-1)

        while not title_screen.finished:
            title_screen.progress(self.window)

            for e in pygame.event.get():
                self.__try_quit(e)

                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and title_screen.ready:
                    pygame.mixer.music.fadeout(1500)
                    title_screen.finished = True

            pygame.display.update()
            self.clock.tick(s.TITLE_FPS)

    def __countdown(self):
        countdown = cd.CountDown()

        while not countdown.finished:
            countdown.progress(self.window)

            pygame.display.update()
            self.clock.tick(s.COUNTDOWN_FPS)

    def __player_select(self):
        player_select = ps.PlayerSelect()

        while not player_select.finished:
            player_select.progress(self.window)

            pygame.display.update()
            self.clock.tick(s.FPS)

        self.selected_player = player_select.selected

    def __try_quit(self, e):
        if e.type == QUIT or\
          (e.type == pygame.KEYDOWN and\
           e.key == pygame.K_ESCAPE and\
           s.FULLSCREEN):
            pygame.quit()
            sys.exit()
