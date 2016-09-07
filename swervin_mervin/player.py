import pygame, math, datetime, os
from pygame.locals import *
from enum import Enum
import settings as s
import util as u

class PlayerStatus(Enum):
    alive = 0
    game_over  = 1
    level_over = 2

class Player:
    """Represents the player in the game world."""

    def __init__(self, high_score, selected_player):
        self.settings       = s.PLAYERS[selected_player]
        self.points         = 0
        self.high_score     = high_score
        self.next_milestone = s.POINT_MILESTONE

        self.reset()

    def reset(self, total_laps=s.LAPS_PER_LEVEL):
        """Resets player variables for the start of a new level."""
        self.status          = PlayerStatus.alive
        self.level_over_lag  = s.LEVEL_OVER_LAG
        self.x               = 0
        self.y               = 0
        self.position        = 0
        self.lap_percent     = 0
        self.direction       = 0
        self.acceleration    = 0
        self.speed           = 1
        self.speed_boost     = 1
        self.animation_frame = 1
        self.new_lap         = False
        self.lap_bonus       = 0
        self.time_bonus      = 0
        self.lap             = 1
        self.total_laps      = total_laps
        self.lap_time        = 0
        self.lap_margin      = 0
        self.blood_alpha     = 0
        self.in_tunnel       = False
        self.fastest_lap     = s.CHECKPOINT
        self.checkpoint      = s.CHECKPOINT
        self.time_left       = s.CHECKPOINT
        self.last_checkpoint = None
        self.crashed         = False
        self.special_text    = None
        self.screech_sfx     = None

        self.__set_checkpoint()

    def steer(self, segment):
        """Updates x to simulate steering."""
        bounds = s.TUNNEL_BOUNDS if self.in_tunnel else s.BOUNDS
        self.x = u.limit(self.x + self.direction, -bounds, bounds)

        # Apply centrifugal force if we are going around a corner.
        if segment.curve != 0 and self.status == PlayerStatus.alive:
            # Congratulate player if they've broken personal record.
            self.x -= (self.direction_speed() * self.speed_percent() * segment.curve * self.settings["centrifugal_force"])

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
                    if sp.is_hooker():
                        if not sp.hit:
                            sp.hit = True
                            self.__hit_hooker()
                    elif sp.is_bonus():
                        segment.remove_sprite(sp)
                        self.__hit_bonus()
                    elif sp.is_speed_boost():
                        self.__hit_speed_boost()
                    else:
                        self.__hit_world_object()

                    break

            for comp in segment.competitors:
                if self.__collided_with_sprite(comp):
                    self.__hit_competitor()

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

        # Show smoke if player is fangin' it around a corner.
        if abs(segment.curve) > s.MINIMUM_CORNER_SMOKE and\
           self.direction != 0 and\
           self.speed > (self.settings["top_speed"] / 1.2):
            sprite += "_smoke"
            self.__run_screech()
        elif self.screech_sfx:
            self.__stop_screech()

        sprite += "1" if (self.animation_frame < s.PLAYER_ANIM_HOLD) else "2"

        sprite   = self.settings["sprites"][sprite]
        s_width  = int(sprite["width"] * scale * s.ROAD_WIDTH * 1.2)
        s_height = int(sprite["height"] * scale * s.ROAD_WIDTH * 1.2)

        p = pygame.image.load(os.path.join("lib", sprite["path"]))
        p = pygame.transform.scale(p, (s_width, s_height))

        self.rendered_area = [width - (s_width / 2), width + (s_width / 2)]

        window.blit(p, (width - (s_width / 2), s.DIMENSIONS[1] - s_height - s.BOTTOM_OFFSET))

        # Finish up the round.
        if self.status != PlayerStatus.alive:
            self.level_over_lag -= 1

    def render_hud(self, window):
        """Renders a Head-Up display on the active window."""
        center      = (75, s.DIMENSIONS[1] - 80)
        speedo_rect = (35, s.DIMENSIONS[1] - 120, 80, 80)
        orbit_pos   = (self.speed / (self.settings["top_speed"] / 4.7)) + 2.35
        start       = self.__circular_orbit(center, -10, orbit_pos)
        finish      = self.__circular_orbit(center, 36, orbit_pos)
        speed       = round((self.speed / s.SEGMENT_HEIGHT) * 1.5, 1)
        font        = pygame.font.Font(s.FONTS["retro_computer"], 16)
        st          = self.special_text
        time_colour = s.COLOURS["text"] if self.time_left > 5 else s.COLOURS["red"]

        # Speedometer.
        pygame.draw.circle(window, s.COLOURS["black"], center, 50, 2)
        pygame.draw.circle(window, s.COLOURS["black"], center, 4)
        pygame.draw.line(window, s.COLOURS["black"], start, finish, 3)
        pygame.draw.arc(window, s.COLOURS["black"], speedo_rect, 0.2, math.pi * 1.25, 5)
        pygame.draw.arc(window, s.COLOURS["red"], speedo_rect, -0.73, 0.2, 5)

        u.render_text("kmph", window, font, s.COLOURS["text"], (110, s.DIMENSIONS[1] - 24))
        u.render_text(str(speed), window, font, s.COLOURS["text"], (10, s.DIMENSIONS[1] - 24))
        u.render_text("Lap", window, font, s.COLOURS["text"], (s.DIMENSIONS[0] - 130, 10))
        u.render_text("%s/%s" % (self.lap, self.total_laps) , window, font, s.COLOURS["text"], (s.DIMENSIONS[0] - 58, 10))

        u.render_text("Time", window, font, time_colour, (10, 10))
        u.render_text(str(math.trunc(self.time_left)), window, font, time_colour, (90, 10))

        # Render special text.
        if st:
            td = (datetime.datetime.now() - st[0])

            if td.seconds > st[1]:
                self.special_text = None
            else:
                bonus_colour = "bonus_a" if (td.microseconds / 25000.0) % 10 > 5 else "bonus_b"
                u.render_text(st[2], window, font, s.COLOURS[bonus_colour], (10, 36))

        # Points rendering needs more care because it grows so fast.
        p_val_text  = font.render(str(math.trunc(self.points)), 1, s.COLOURS["text"])
        p_name_text = font.render("Points", 1, s.COLOURS["text"])
        p_val_x     = s.DIMENSIONS[0] - p_val_text.get_width() - 10

        window.blit(p_val_text, (p_val_x, s.DIMENSIONS[1] - 24))
        window.blit(p_name_text, (p_val_x - 112, s.DIMENSIONS[1] - 24))

        # Hit a point milestone.
        if self.points > self.next_milestone and self.status == PlayerStatus.alive:
            milestone_sfx = pygame.mixer.Sound(os.path.join("lib", "excellent.ogg"))
            milestone_sfx.play()

            self.next_milestone += s.POINT_MILESTONE

            self.__set_special_text("Nice driving!", 2)

        # On the leaderboard!
        if self.high_score > 0 and self.points > self.high_score:
            high_score_sfx = pygame.mixer.Sound(os.path.join("lib", "excellent.ogg"))
            high_score_sfx.play()

            self.high_score = 0

            self.__set_special_text("New High Score!", 2)

        if self.status == PlayerStatus.game_over:
            self.__game_over_overlay(window)
        elif self.status == PlayerStatus.level_over:
            self.__level_over_overlay(window)

        # Display lap difference (unless we've only done one lap).
        if self.lap_margin != 0 and self.lap > 2 and self.lap_percent < 20:
            diff = self.lap_margin

            if diff <= 0:
                colour = "red"
                sign   = "+"
            else:
                colour = "green"
                sign   = "-"

            u.render_text(sign + str(round(abs(diff), 1)), window, font, s.COLOURS[colour], (10, 40))

    def render_blood(self, window):
        """Renders a blood splatter if we've killed someone."""
        b = pygame.image.load(os.path.join("lib", "blood.png"))
        b.set_alpha(self.blood_alpha)

        x = (s.DIMENSIONS[0] - b.get_size()[0]) / 2
        y = ((s.DIMENSIONS[1] - b.get_size()[1]) / 2) - 30
 
        window.blit(b, (x, y))

        self.blood_alpha -= 1

    def accelerate(self):
        """Updates speed at appropriate acceleration level."""
        curr_speed = self.speed_boost * (self.speed + ((self.settings["top_speed"] / self.settings["acceleration_factor"]) * self.acceleration))
        self.speed = u.limit(curr_speed, 0, self.speed_boost * self.settings["top_speed"])

    def travel(self, track_length, window):
        """Updates position, reflecting how far we've travelled since the last frame."""
        pos        = self.position + (s.FRAME_RATE * self.speed)
        td         = (datetime.datetime.now() - self.last_checkpoint)
        total_secs = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6 # td.total_seconds() not implemented in Python 2.6

        self.new_lap = False

        if self.speed_boost > 1:
            self.speed_boost -= s.SPEED_BOOST_DECREASE

        if self.status == PlayerStatus.alive:
            self.points   += (self.speed / s.SEGMENT_HEIGHT) / s.POINTS
            self.time_left = round(self.checkpoint - total_secs, 1) + self.lap_bonus

            if self.time_left <= 0:
                go_sfx = pygame.mixer.Sound(os.path.join("lib", "loser.ogg"))
                go_sfx.play()
                self.status = PlayerStatus.game_over
            elif self.time_left == 5:
                self.__set_special_text("Hurry up!", 2)

        # New lap.
        if pos >= track_length:
            self.__set_checkpoint()

            self.lap_bonus  = 0
            self.new_lap    = True
            self.lap_time   = total_secs
            self.lap_margin = self.fastest_lap - self.lap_time

            # Finished level.
            if self.status == PlayerStatus.alive and self.lap == self.total_laps:
                self.status = PlayerStatus.level_over
            else:    
                self.lap += 1

                lap_sfx = pygame.mixer.Sound(os.path.join("lib", "570.wav"))
                lap_sfx.play()

            if self.status != PlayerStatus.game_over:
                # Reduce checkpoint time every lap to increase difficulty.
                checkpoint_diff = (self.checkpoint - self.lap_time) / s.LAP_DIFFICULTY_FACTOR
                bonus_points    = self.time_left * s.POINTS * self.lap

                self.checkpoint -= max(checkpoint_diff, s.MINIMUM_DIFFICULTY)
                self.time_bonus += bonus_points
                self.points     += bonus_points

                if self.__fastest_lap():
                    # Congratulate player if they've broken personal record.
                    if self.lap > 2:
                        self.points += self.lap_margin * s.POINTS * self.lap
                        fast_lap_sfx = pygame.mixer.Sound(os.path.join("lib", "jim.ogg"))
                        fast_lap_sfx.play()

                    self.fastest_lap = self.lap_time

            pos -= track_length

        if pos < 0:
            pos += track_length

        self.position    = pos
        self.lap_percent = round((pos / track_length) * 100)

    def set_acceleration(self, keys):
        """Updates the acceleration factor depending on world conditions."""
        a = -s.FRAME_RATE

        # Slow player down if they are on the grass or crashed.
        if self.crashed:
            a = 0
        else:
            if (self.x > 1.0 or self.x < -1.0) and self.speed > (self.settings["top_speed"] / self.settings["offroad_top_speed_factor"]):
                a = a * 3
            else:
                if keys[K_UP] or keys[K_x] or s.AUTO_DRIVE or self.status != PlayerStatus.alive:
                    a = s.FRAME_RATE
                elif keys[K_DOWN]:
                    a = -(s.FRAME_RATE * self.settings["deceleration"])

        self.acceleration = a

    def set_direction(self, keys):
        """Updates the direction the player is going, accepts a key-map."""
        d = 0

        if self.status == PlayerStatus.alive:
            if keys[K_LEFT]:
                d = -self.direction_speed()
            elif keys[K_RIGHT]:
                d = self.direction_speed()

        self.direction = d

    def speed_percent(self):
        return self.speed / self.settings["top_speed"]

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
                pygame.mixer.music.set_volume(s.MUSIC_VOLUME)
                self.crashed = False

    def finished(self):
        return self.level_over_lag == 0

    def alive(self):
        return self.status != PlayerStatus.game_over

    def __set_special_text(self, text, time):
        """Defines the special text to show and for how long we should show it."""
        st = self.special_text

        if not st or st[2] != text:
            self.special_text = [datetime.datetime.now(), time, text]

    def __collided_with_sprite(self, sprite):
        r_area = list(sprite.rendered_area)
        p_area = sprite.sprite["collision"]
        width  = r_area[1] - r_area[0]

        # Apply offsets.
        r_area[0] += (width * p_area[0])
        r_area[1] -= (width * p_area[1])

        return (self.rendered_area[0] < r_area[1] and\
                self.rendered_area[1] > r_area[0])
 
    def __circular_orbit(self, center, radius, t):
        """Returns the X/Y coordinate for a given time (t) in a circular orbit."""
        theta = math.fmod(t, math.pi * 2)
        c     = math.cos(theta)
        s     = math.sin(theta)

        return center[0] + radius * c, center[1] + radius * s

    def __set_checkpoint(self):
        self.last_checkpoint = datetime.datetime.now()

    def __hit_hooker(self):
        crash_sfx        = pygame.mixer.Sound(os.path.join("lib", "scream.ogg"))
        splat_sfx        = pygame.mixer.Sound(os.path.join("lib", "blood.ogg"))
        self.blood_alpha = 255

        # Yeah, I'm a sicko....
        if self.status == PlayerStatus.alive:
            self.points += s.POINT_GAIN_PROSTITUTE
            self.__set_special_text("+%d points!" % s.POINT_GAIN_PROSTITUTE, 2)

        crash_sfx.play()
        splat_sfx.play()

    def __hit_bonus(self):
        if self.status == PlayerStatus.alive:
            self.lap_bonus += s.BONUS_AMOUNT

        bonus_sfx = pygame.mixer.Sound(os.path.join("lib", "oh_yeah.ogg"))
        bonus_sfx.play()

        self.__set_special_text("Bonus time!", 2)

    def __hit_speed_boost(self):
        if self.speed_boost == 1:
            boost_sfx = pygame.mixer.Sound(os.path.join("lib", "speed_boost.ogg"))
            boost_sfx.play()

            self.__set_special_text("Speed boost!", 2)

        self.speed_boost = 1.6

    def __hit_world_object(self):
        pygame.mixer.music.set_volume(0.2)

        crash_sfx        = pygame.mixer.Sound(os.path.join("lib", "you_fool.ogg"))
        self.crashed     = True
        self.speed       = 0
        self.speed_boost = 1

        crash_sfx.play()

        if self.status == PlayerStatus.alive:
            deduction    = self.points * s.POINT_LOSS_SPRITE
            self.points -= deduction
            self.__set_special_text("-%d points!" % deduction, 2)

    def __hit_competitor(self):
        crash_sfx = pygame.mixer.Sound(os.path.join("lib", "car_crash.ogg"))
        crash_sfx.play()

        self.speed = self.speed / s.CRASH_DIVISOR

        if self.status == PlayerStatus.alive:
            self.points -= self.points * s.POINT_LOSS_COMP

    def __fastest_lap(self):
        return self.status != PlayerStatus.game_over and self.lap_time < self.fastest_lap

    def __run_screech(self):
        if not self.screech_sfx:
            self.screech_sfx = pygame.mixer.Sound(os.path.join("lib", "screech_short.ogg"))
            self.screech_sfx.set_volume(0.4)
            self.screech_sfx.play(-1)

    def __stop_screech(self):
        self.screech_sfx.stop()
        self.screech_sfx = None

    def __game_over_overlay(self, window):
        go_font = pygame.font.Font(s.FONTS["retro_computer"], 44)
        txt_go  = go_font.render("Game Over", 1, s.COLOURS["red"])
        x       = (s.DIMENSIONS[0] - txt_go.get_size()[0]) / 2
        y       = (s.DIMENSIONS[1] - txt_go.get_size()[1]) / 2
        overlay = pygame.Surface(s.DIMENSIONS, pygame.SRCALPHA)

        overlay.fill((255, 255, 255, 90))
        overlay.blit(txt_go, (x, y))
        window.blit(overlay, (0,0))

    def __level_over_overlay(self, window):
        lo_font      = pygame.font.Font(s.FONTS["fipps"], 38)
        s_font       = pygame.font.Font(s.FONTS["retro_computer"], 30)
        txt_lo       = lo_font.render("Level Complete!", 1, s.COLOURS["dark_text"])
        txt_lap      = s_font.render("Best Lap", 1, s.COLOURS["dark_text"])
        txt_lap_v    = s_font.render("%.1fs" % round(self.fastest_lap, 1), 1, s.COLOURS["dark_text"])
        txt_bonus    = s_font.render("Time bonus", 1, s.COLOURS["dark_text"])
        txt_bonus_v  = s_font.render(str(math.trunc(self.time_bonus)), 1, s.COLOURS["dark_text"])
        txt_points   = s_font.render("Points", 1, s.COLOURS["dark_text"])
        txt_points_v = s_font.render(str(math.trunc(self.points)), 1, s.COLOURS["dark_text"])
        overlay      = pygame.Surface(s.DIMENSIONS, pygame.SRCALPHA)

        overlay.fill((255, 255, 255, 150))
        overlay.blit(txt_lo, (s.DIMENSIONS[0] / 2 - txt_lo.get_size()[0] / 2, 20))
        overlay.blit(txt_lap, (20, 180))
        overlay.blit(txt_lap_v, (s.DIMENSIONS[0] - txt_lap_v.get_size()[0] - 10, 190))
        overlay.blit(txt_bonus, (20, 260))
        overlay.blit(txt_bonus_v, (s.DIMENSIONS[0] - txt_bonus_v.get_size()[0] - 10, 270))
        overlay.blit(txt_points, (20, 340))
        overlay.blit(txt_points_v, (s.DIMENSIONS[0] - txt_points_v.get_size()[0] - 10, 350))

        window.blit(overlay, (0,0))
