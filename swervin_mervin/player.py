import settings as s
import util as u
import pygame, math, datetime, os
from pygame.locals import *

class Player:
    """Represents the player in the game world."""

    def __init__(self, window):
        self.x               = 0
        self.y               = 0
        self.position        = 0
        self.lap_percent     = 0
        self.direction       = 0
        self.acceleration    = 0
        self.speed           = 1
        self.animation_frame = 1
        self.lap             = 1
        self.lap_time        = 0
        self.lap_margin      = 0
        self.points          = 0
        self.fastest_lap     = s.CHECKPOINT
        self.checkpoint      = s.CHECKPOINT
        self.time_left       = s.CHECKPOINT
        self.last_checkpoint = None
        self.crashed         = False
        self.game_over       = False
        self.window          = window

        self.__set_checkpoint()

    def steer(self, segment):
        """Updates x to simulate steering."""
        self.x = u.limit(self.x + self.direction, -s.BOUNDS, s.BOUNDS)

        # Apply centrifugal force if we are going around a corner.
        if segment.curve != 0 and not self.game_over:
            self.x -= (self.direction_speed() * self.speed_percent() * segment.curve * s.CENTRIFUGAL_FORCE)

    def climb(self, segment):
        """Updates y to simulate hill and valley ascension."""
        top_y    = segment.top["world"]["y"]
        bottom_y = segment.bottom["world"]["y"]

        self.y = top_y + (top_y - bottom_y) * self.speed_percent()

    def detect_collisions(self, segment):
        """Detects and handles player collisions with sprites."""
        if not self.crashed:
            for sp in segment.sprites:
                if sp.sprite.has_key("collision") and self.__collided_with_sprite(sp):
                    pygame.mixer.music.set_volume(0.2)
                    crash_sfx    = pygame.mixer.Sound(os.path.join("lib", "you_fool.ogg"))
                    self.crashed = True
                    self.speed   = 0

                    if not self.game_over:
                        self.points -= self.points * s.POINT_LOSS_SPRITE

                    crash_sfx.play()
                    break

            for comp in segment.competitors:
                if self.__collided_with_competitor(comp):
                    self.speed = 0

                    if not self.game_over:
                        self.points -= self.points * s.POINT_LOSS_COMP
                    break

    def render(self, window, segment):
        """Renders the player sprite to the given surface."""
        top    = segment.top
        bottom = segment.bottom
        width  = s.DIMENSIONS[0] / 2
        height = s.DIMENSIONS[1] / 2
        scale  = s.CAMERA_DEPTH / (s.CAMERA_HEIGHT * s.CAMERA_DEPTH)
        sprite = "straight"

        if self.direction > 0:
            sprite = "right"
        elif self.direction < 0:
            sprite = "left"

        if top["world"]["y"] > bottom["world"]["y"]:
            sprite = "uphill_" + sprite
        elif top["world"]["y"] < (bottom["world"]["y"] - 10):  # TODO: Fix this. Should not need -10 here.
            sprite = "downhill_" + sprite

        if self.speed > 0:
            self.animation_frame += 1

            if self.animation_frame > (s.PLAYER_ANIM_HOLD * 2):
                self.animation_frame = 1

        sprite += "1" if (self.animation_frame < s.PLAYER_ANIM_HOLD) else "2"

        sprite   = s.SPRITES[sprite]
        s_width  = int(sprite["width"] * scale * s.ROAD_WIDTH * 1.2)
        s_height = int(sprite["height"] * scale * s.ROAD_WIDTH * 1.2)

        p = pygame.image.load(os.path.join("lib", sprite["path"]))
        p = pygame.transform.scale(p, (s_width, s_height))
        window.blit(p, (width - (s_width / 2), s.DIMENSIONS[1] - s_height - s.BOTTOM_OFFSET))

    def render_hud(self, window, high_scores):
        """Renders a Head-Up display on the active window."""
        center      = (75, s.DIMENSIONS[1] - 75)
        speedo_rect = (35, s.DIMENSIONS[1] - 115, 80, 80)
        orbit_pos   = (self.speed / (s.TOP_SPEED / 4.7)) + 2.35
        start       = self.__circular_orbit(center, -10, orbit_pos)
        finish      = self.__circular_orbit(center, 36, orbit_pos)
        speed       = round((self.speed / s.SEGMENT_HEIGHT) * 1.5, 1)
        font        = pygame.font.Font(s.FONTS["bladerunner"], 20)

        pygame.draw.circle(window, s.COLOURS["black"], center, 50, 2)
        pygame.draw.circle(window, s.COLOURS["black"], center, 4)
        pygame.draw.line(window, s.COLOURS["black"], start, finish, 3)
        pygame.draw.arc(window, s.COLOURS["black"], speedo_rect, 0.2, math.pi * 1.25, 5)
        pygame.draw.arc(window, s.COLOURS["red"], speedo_rect, -0.73, 0.2, 5)

        u.render_text("kmph", window, font, s.COLOURS["text"], (70, s.DIMENSIONS[1] - 24))
        u.render_text(str(speed), window, font, s.COLOURS["text"], (10, s.DIMENSIONS[1] - 24))
        u.render_text("lap", window, font, s.COLOURS["text"], (s.DIMENSIONS[0] - 100, 10))
        u.render_text(str(self.lap), window, font, s.COLOURS["text"], (s.DIMENSIONS[0] - 28, 10))
        u.render_text("time", window, font, s.COLOURS["text"], (10, 10))
        u.render_text(str(self.time_left), window, font, s.COLOURS["text"], (90, 10))

        # Points rendering needs more care because it grows so fast.
        p_val_text  = font.render(str(math.trunc(self.points)), 1, s.COLOURS["text"])
        p_name_text = font.render("points", 1, s.COLOURS["text"])
        p_val_x     = s.DIMENSIONS[0] - p_val_text.get_width() - 10

        window.blit(p_val_text, (p_val_x, s.DIMENSIONS[1] - 24))
        window.blit(p_name_text, (p_val_x - 112, s.DIMENSIONS[1] - 24))

        if self.game_over:
            go_font = pygame.font.Font(s.FONTS["bladerunner"], 24)
            go      = go_font.render("Game Over", 1, s.COLOURS["red"]);
            hs_font = pygame.font.Font(s.FONTS["bladerunner"], 44)
            hs      = hs_font.render("High Scores", 1, s.COLOURS["dark_text"]);
            go_x    = (s.DIMENSIONS[0] - go.get_size()[0]) / 2
            go_y    = ((s.DIMENSIONS[1] * 0.2) - go.get_size()[1]) / 2 
            hs_x    = (s.DIMENSIONS[0] - hs.get_size()[0]) / 2
            hs_y    = go_y + 50
            overlay = pygame.Surface(s.DIMENSIONS, pygame.SRCALPHA)

            overlay.fill((255, 255, 255, 99))
            overlay.blit(go, (go_x, go_y))
            overlay.blit(hs, (hs_x, hs_y))

            record_offset = hs_y + hs.get_height() + 10
            record_font   = pygame.font.Font(s.FONTS["bladerunner"], 24)

            for record in high_scores:
                r_name  = record_font.render(record[0], 1, s.COLOURS["dark_text"])
                r_score = record_font.render(str(record[1]), 1, s.COLOURS["dark_text"])

                overlay.blit(r_name, (hs_x, record_offset))
                overlay.blit(r_score, (hs_x + hs.get_width() - r_score.get_width(), record_offset))

                record_offset += r_name.get_height() + 10

            window.blit(overlay, (0,0))

        # Display lap difference (unless we've only done one lap).
        if self.lap_margin != 0 and self.lap > 2 and self.lap_percent < 20:
            diff = self.lap_margin

            if diff <= 0:
                colour = "red"
                sign   = "+"
            else:
                colour = "green"
                sign   = "-"

            u.render_text(sign + str(abs(diff)), window, font, s.COLOURS[colour], (10, 40))

    def accelerate(self):
        """Updates speed at appropriate acceleration level."""
        self.speed = u.limit(self.speed + (s.ACCELERATION * self.acceleration), 0, s.TOP_SPEED)

    def travel(self, track_length, window):
        """Updates position, reflecting how far we've travelled since the last frame."""
        pos       = self.position + (s.FRAME_RATE * self.speed)
        timedelta = (datetime.datetime.now() - self.last_checkpoint)

        if not self.game_over:
            self.points += (self.speed / s.SEGMENT_HEIGHT) / s.POINTS

        if not self.game_over:
            self.time_left = round(self.checkpoint - timedelta.total_seconds(), 1)

        if self.time_left <= 0:
            self.game_over = True
            pygame.mixer.music.fadeout(6000)

        # New lap.
        if pos >= track_length:
            self.__set_checkpoint()

            self.lap_time    = timedelta.total_seconds()
            self.lap        += 1
            self.lap_margin  = self.fastest_lap - self.lap_time

            if not self.game_over:
                # Reduce checkpoint time every lap to increase difficulty.
                self.checkpoint -= 1
                self.points     += self.time_left * s.POINTS * self.lap

            if self.__fastest_lap():
                if self.lap > 2:
                    self.points += self.lap_margin * s.POINTS * self.lap
                    lap_sfx      = pygame.mixer.Sound(os.path.join("lib", "jim.ogg"))
                    lap_sfx.play()

                self.fastest_lap = self.lap_time

            pos -= track_length

        if pos < 0:
            pos += track_length

        self.position    = pos
        self.lap_percent = round((pos / track_length) * 100)

    def set_acceleration(self, keys):
        """Updates the acceleration factor depending on world conditions."""
        a = -s.FRAME_RATE

        # Slow player down if they are on the grass.
        if self.crashed:
            a = 0
        else:
            if (self.x > 1.0 or self.x < -1.0) and self.speed > s.OFFROAD_TOP_SPEED:
                a = a * 3
            else:
                if keys[K_UP] or s.AUTO_DRIVE or self.game_over:
                    a = s.FRAME_RATE
                elif keys[K_DOWN]:
                    a = -(s.FRAME_RATE * s.DECELERATION)

        self.acceleration = a

    def set_direction(self, keys, leap_direction="straight"):
        """Updates the direction the player is going, accepts a key-map."""
        d = 0

        if not self.game_over:
            if keys[K_LEFT] or leap_direction == "left":
                d = -self.direction_speed()
            elif keys[K_RIGHT] or leap_direction == "right":
                d = self.direction_speed()

        self.direction = d

    def speed_percent(self):
        return self.speed / s.TOP_SPEED

    def direction_speed(self):
        return (s.FRAME_RATE * 3 * self.speed_percent())

    def segment_percent(self):
        """Returns a value between 0 and 1 indicating how far through the current segment we are."""
        return ((self.position + s.PLAYER_Z) % s.SEGMENT_HEIGHT) / s.SEGMENT_HEIGHT

    def handle_crash(self):
        """Proceeds player through crash state."""
        if self.crashed:
            step = -0.025 if self.x > 0 else 0.025

            if round(self.x, 1) != 0:
                self.x += step
            else:
                pygame.mixer.music.set_volume(1.0)
                self.crashed = False

    def __collided_with_sprite(self, sprite):
        s = sprite.sprite
        o = sprite.offset

        return (self.x < (o + s["collision"][1]) and o < 0) or\
               (self.x > (o + s["collision"][0]) and o > 0)
 
    def __collided_with_competitor(self, c):
        o = c.offset

        return (self.x > o - 0.45) and (self.x < o + 0.23)
 
    def __circular_orbit(self, center, radius, t):
        """Returns the X/Y coordinate for a given time (t) in a circular orbit."""
        theta = math.fmod(t, math.pi * 2)
        c     = math.cos(theta)
        s     = math.sin(theta)

        return center[0] + radius * c, center[1] + radius * s

    def __set_checkpoint(self):
        self.last_checkpoint = datetime.datetime.now()

    def __fastest_lap(self):
        return not self.game_over and self.lap_time < self.fastest_lap
