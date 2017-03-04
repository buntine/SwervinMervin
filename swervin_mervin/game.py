import pygame, sys, os, math, random
from pygame.locals import *
import player as p
import level as l
import title_screen as ts
import countdown as cd
import player_select as ps
import settings as s
import high_scores as hs
import credits as c
import util as u

class Game:
    """Provides the game flow."""

    def __init__(self, window, clock):
        self.window          = window
        self.clock           = clock
        self.paused          = False
        self.waiting         = False
        self.selected_player = 0
        self.player          = None
        self.level           = None
        self.high_scores     = hs.HighScores()

    def play(self):
        if s.TITLE_SCREEN:
            self.__title_screen()

        if s.PLAYER_SELECT:
            self.__player_select()

        self.player = p.Player(self.high_scores.minimum_score(), self.selected_player)

        for i, lvl in enumerate(s.LEVELS):
            self.level = l.Level(lvl)

            self.player.reset(self.level.laps)
            self.level.build()

            if s.COUNTDOWN:
                self.__countdown(i + 1)

            pygame.mixer.music.load(os.path.join("lib", self.level.song))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(s.MUSIC_VOLUME)

            while not self.player.finished():
                if self.paused:
                    self.__pause_cycle()
                else:
                    self.__game_cycle()

                pygame.display.update()
                self.clock.tick(s.FPS)

            pygame.mixer.music.fadeout(1500)

            if not self.player.alive():
                break

        if self.player.alive():
            self.__credits_screen()

        ## Post-game high scores and wait for new player.
        if self.high_scores.is_high_score(self.player.points):
            self.high_scores.add_high_score(math.trunc(self.player.points))

        self.waiting = True

    def wait(self):
        """Shows high scores until a new player is ready."""

        heading_font = pygame.font.Font(s.FONTS["fipps"], 44)
        content_font = pygame.font.Font(s.FONTS["retro_computer"], 15)
        background   = pygame.image.load(os.path.join("lib", "title.png"))
        heading_text = heading_font.render("High Scores", 1, s.COLOURS["text"])
        y            = 120

        self.window.fill(s.COLOURS["black"])
        self.window.blit(background, (0, 0))
        self.window.blit(heading_text, (30, 3))

        for score in self.high_scores.high_scores:
            date_text  = content_font.render(score[0].strftime("%d %b %Y"), 1, s.COLOURS["text"])
            score_text = content_font.render(str(score[1]), 1, s.COLOURS["text"])

            self.window.blit(date_text, (30, y))
            self.window.blit(score_text, (230, y))
            y += 35

        pygame.display.update()

        while self.waiting:
            for e in pygame.event.get():
                u.try_quit(e)

                if e.type == KEYDOWN and e.key in [K_UP, K_RETURN]:
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

        coverage    = [base_segment, base_segment, base_segment]
        tunnel_exit = base_segment
        pre_renders = []
        curve       = 0
        curve_delta = -(base_segment.curve * p.segment_percent())

        # Position backgrounds according to current curve.
        for bg in l.backgrounds:
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

            # Remember biggest LEFT, TOP, RIGHT coordinates so we can clip sprites later.
            segment.clip = [
              coverage[0].bottom["screen"]["x"] - coverage[0].bottom["screen"]["w"],
              coverage[1].top["screen"]["y"],
              coverage[2].bottom["screen"]["x"] + coverage[2].bottom["screen"]["w"]]

            if len(segment.pre_polygons) > 0:
                pre_renders.append(segment)

            if segment.tunnel_end:
                tunnel_exit = segment

            if segment.should_ignore(coverage[1]):
                continue

            segment.render_grass(self.window)
            segment.render_road(self.window)

            if (segment.top["screen"]["y"] > coverage[1].top["screen"]["y"]):
                coverage[1] = segment

            # Remember where we should draw the left and right tunnel walls.
            if segment.in_tunnel:
                s_top  = segment.top["screen"]
                tl_top = coverage[0].top["screen"]
                tr_top = coverage[2].top["screen"]
                
                if (s_top["x"] - s_top["w"]) > (tl_top["x"] - tl_top["w"]):
                    coverage[0] = segment

                if (s_top["x"] + s_top["w"]) < (tr_top["x"] + tr_top["w"]):
                    coverage[2] = segment

        # Draw tunnel roof and walls.
        if base_segment.in_tunnel:
            self.player.in_tunnel = True

            tunnel_exit.render_tunnel_roof(self.window, coverage[1].top["screen"]["y"])
            coverage[0].render_left_tunnel(self.window)
            coverage[2].render_right_tunnel(self.window)
        else:
            self.player.in_tunnel = False

        # Let backgrounds know how much height they need to cover on the next paint.
        for bg in l.backgrounds:
            bg.visible_height = s.DIMENSIONS[1] - coverage[1].top["screen"]["y"]

        # Draw sprites in from back to front (painters algorithm).
        for segment in reversed(pre_renders):
            segment.render_polygons(self.window, coverage)

        for i in reversed(range(1, s.DRAW_DISTANCE)):
            segment = l.offset_segment(base_segment.index + i)
            segment.render_world_objects(self.window)

        p.render(self.window, base_segment)
        p.render_hud(self.window)

        if p.blood_alpha > 0:
            p.render_blood(self.window)

        for e in pygame.event.get():
            u.try_quit(e)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                pygame.mixer.music.pause()
                self.paused = True

        # Steering, acceleration.
        keys = pygame.key.get_pressed()
        p.set_acceleration(keys)
        p.set_direction(keys)

    def __pause_cycle(self):
        pause_font = pygame.font.Font(s.FONTS["retro_computer"], 64)
        pause_text = pause_font.render("Paused", 1, s.COLOURS["text"])
        x          = (s.DIMENSIONS[0] - pause_text.get_width()) / 2
        y          = (s.DIMENSIONS[1] - pause_text.get_height()) / 2

        self.window.fill(s.COLOURS["black"])
        self.window.blit(pause_text, (x, y))

        for e in pygame.event.get():
            u.try_quit(e)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                pygame.mixer.music.unpause()
                self.paused = False

    def __progress(self, screen, fps):
        while not screen.finished:
            screen.progress(self.window)

            pygame.display.update()
            self.clock.tick(fps)

    def __title_screen(self):
        title_screen = ts.TitleScreen()
        pygame.mixer.music.load(os.path.join("lib", "mn84-theme.ogg"))
        pygame.mixer.music.play(-1)
        self.__progress(title_screen, s.TITLE_FPS)

    def __countdown(self, level_number):
        countdown = cd.CountDown(level_number, self.level.name)
        self.__progress(countdown, s.COUNTDOWN_FPS)

    def __player_select(self):
        player_select = ps.PlayerSelect()
        self.__progress(player_select, s.PLAYER_SELECT_FPS)
        self.selected_player = player_select.selected

    def __credits_screen(self):
        credits = c.Credits()
        self.__progress(credits, s.CREDITS_FPS)
