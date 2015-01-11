import pygame, sys, os, math
from pygame.locals import *
import player as p
import background as b
import level as l
import title_screen as ts
import countdown as cd
import settings as s
import high_scores as hs

class Game:
    """Represents the game flow."""

    def __init__(self, window, clock):
        self.window      = window
        self.clock       = clock
        self.waiting     = False
        self.high_scores = hs.HighScores()

    def play(self):
        ## Fire up the title screen.
        if s.TITLE_SCREEN:
            title_screen = ts.TitleScreen()
            pygame.mixer.music.load(os.path.join("lib", "mn84-theme.ogg"))
            pygame.mixer.music.play(-1)

            while not title_screen.finished:
                title_screen.progress(self.window)

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and title_screen.ready:
                            pygame.mixer.music.fadeout(1500)
                            title_screen.finished = True
                        elif event.key == pygame.K_ESCAPE and s.FULLSCREEN:
                            pygame.quit()
                            sys.exit()
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
                self.clock.tick(s.TITLE_FPS)

        ## Show countdown.
        if s.COUNTDOWN:
            countdown = cd.CountDown()

            while not countdown.finished:
                countdown.progress(self.window)

                pygame.display.update()
                self.clock.tick(s.COUNTDOWN_FPS)

        ## Now lets play!
        player      = p.Player()
        level       = l.Level("melbourne")
        backgrounds = [b.Background("sky", 0, 2, True),
                        b.Background("city", 0, 1)]

        level.build()

        pygame.mixer.music.load(os.path.join("lib", "lazerhawk-overdrive.ogg"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(s.MUSIC_VOLUME)

        while player.alive():
            player.travel(level.track_length(), self.window)

            base_segment   = level.find_segment(player.position)
            player_segment = level.find_segment(player.position + s.PLAYER_Z)

            player.accelerate()
            player.steer(player_segment)
            player.climb(base_segment)
            player.detect_collisions(player_segment)
            player.handle_crash()

            # Move the other players.
            for c in level.competitors:
                old_seg = level.find_segment(c.position)
                c.travel(level.track_length())
                new_seg = level.find_segment(c.position)

                if old_seg.index != new_seg.index:
                    if c in old_seg.competitors:
                        old_seg.competitors.remove(c)
                    new_seg.competitors.append(c)

            y_coverage  = 0
            curve       = 0
            curve_delta = -(base_segment.curve * player.segment_percent())

            # Position backgrounds according to current curve.
            for bg in backgrounds:
                if base_segment.curve != 0:
                    bg.step(base_segment.curve, player.speed_percent())
                bg.render(self.window)

            # Loop through segments we should draw for this frame.
            for i in range(s.DRAW_DISTANCE):
                segment            = level.offset_segment(base_segment.index + i)
                projected_position = player.position
                camera_x           = player.x * s.ROAD_WIDTH

                # Past end of track and looped back.
                if segment.index < base_segment.index:
                    projected_position -= level.track_length()

                segment.project(camera_x,
                  curve,
                  curve_delta,
                  projected_position,
                  player.y)

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
                for i in reversed(range(1, s.DRAW_DISTANCE)):
                    segment = level.offset_segment(base_segment.index + i)
                    segment.render_world_objects(self.window)

                player.render(self.window, base_segment)
                player.render_hud(self.window)

                if player.blood_alpha > 0:
                    player.render_blood(self.window)

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and s.FULLSCREEN):
                    pygame.quit()
                    sys.exit()

            # Steering, acceleration.
            keys = pygame.key.get_pressed()
            player.set_acceleration(keys)
            player.set_direction(keys)

            pygame.display.update()
            self.clock.tick(s.FPS)

        ## Post-game high scores and wait for new player.
        if self.high_scores.is_high_score(player.points):
            self.high_scores.add_high_score(math.trunc(player.points))

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
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and s.FULLSCREEN):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key in [K_UP, K_SPACE]:
                    self.waiting = False
     
            self.clock.tick(s.FPS)
