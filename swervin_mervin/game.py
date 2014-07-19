import pygame, sys, os
from pygame.locals import *
import settings as s
import background as b
import leap_direction_listener as ldl
import leap_player_listener as lpl
import Leap

class Game:
    """Represents the overall game flow"""

    def __init__(self, window, player, level):
        self.window             = window
        self.player             = player
        self.level              = level
        self.fps_clock          = pygame.time.Clock()
        self.backgrounds        = [b.Background("sky", 0, 2, True),
                                b.Background("city", 0, 1)]
        self.leap_controller    = Leap.Controller()
        self.direction_listener = ldl.LeapDirectionListener()
        self.player_listener    = lpl.LeapPlayerListener()

    def setup(self):
        self.waiting_for_player = False

        self.direction_listener.reset()
        self.player_listener.reset()

        self.leap_controller.add_listener(self.direction_listener)
        pygame.mixer.music.load(os.path.join("lib", "lazerhawk-overdrive.mp3"))
        pygame.mixer.music.play(-1)

    def progress(self):
        """Animate the next frame"""
        self.player.travel(self.level.track_length())

        base_segment   = self.level.find_segment(self.player.position)
        player_segment = self.level.find_segment(self.player.position + s.PLAYER_Z)

        self.player.accelerate()
        self.player.steer(player_segment)
        self.player.climb(base_segment)
        self.player.detect_collisions(player_segment)
        self.player.handle_crash()

        # Move the other players.
        for c in self.level.competitors:
            old_seg = self.level.find_segment(c.position)
            c.travel(self.level.track_length())
            new_seg = self.level.find_segment(c.position)

            if old_seg.index != new_seg.index:
                if c in old_seg.competitors:
                    old_seg.competitors.remove(c)
                new_seg.competitors.append(c)

        y_coverage  = 0
        curve       = 0
        curve_delta = -(base_segment.curve * self.player.segment_percent())

        # Position backgrounds according to current curve.
        for bg in self.backgrounds:
            if base_segment.curve != 0:
                bg.step(base_segment.curve, self.player.speed_percent())
            bg.render(self.window)

        # Loop through segments we should draw for this frame.
        for i in range(s.DRAW_DISTANCE):
            segment            = self.level.offset_segment(base_segment.index + i)
            projected_position = self.player.position
            camera_x           = self.player.x * s.ROAD_WIDTH

            # Past end of track and looped back.
            if segment.index < base_segment.index:
                projected_position -= self.level.track_length()

            segment.project(camera_x,
              curve,
              curve_delta,
              projected_position,
              self.player.y)

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
                segment = self.level.offset_segment(base_segment.index + i)
                segment.render_world_objects(self.window)

            self.player.render(base_segment)
            self.player.render_hud(self.level.high_scores)

        # Steering, acceleration.
        keys = pygame.key.get_pressed()
        self.player.set_acceleration(keys)
        self.player.set_direction(keys, self.direction_listener.direction)

        for event in pygame.event.get():
            if event.type == QUIT:
                self.leap_controller.remove_listener(self.direction_listener) 
                pygame.quit()
                sys.exit()

        pygame.display.update()
        self.fps_clock.tick(s.FPS)

    def finished(self):
        if self.waiting_for_player:
            return self.player_listener.ready
        else:
            return self.player.game_over

    def high_score(self):
        return False

    def game_over(self):
        """Puts the game in 'Game Over' mode"""
        self.waiting_for_player = True

        pygame.mixer.music.fadeout(6000)

        self.leap_controller.remove_listener(self.direction_listener)
        self.leap_controller.add_listener(self.player_listener)

    def clean(self):
        pass
