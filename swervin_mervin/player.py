import settings as s
import util as u
import pygame
from pygame.locals import *
import math

class Player:
    """Represents the player in the game world."""

    def __init__(self):
        self.x               = 0
        self.y               = 0
        self.position        = 0
        self.direction       = 0
        self.acceleration    = 0
        self.speed           = 1
        self.animation_frame = 1
        self.crashed         = False

    def steer(self, segment):
        """Updates x to simulate steering."""
        self.x = u.limit(self.x + self.direction, -s.BOUNDS, s.BOUNDS)

        # Apply centrifugal force if we are going around a corner.
        if segment.curve != 0:
            self.x -= (self.direction_speed() * self.speed_percent() * segment.curve * s.CENTRIFUGAL_FORCE)

    def climb(self, segment):
        """Updates y to simulate hill and valley ascension."""
        top_y    = segment.top["world"]["y"]
        bottom_y = segment.bottom["world"]["y"]

        self.y = top_y + (top_y - bottom_y) * self.speed_percent()

    def detect_collisions(self, segment):
        """Detects and handles player collisions with sprites."""
        if self.speed > 0:
            for sp in segment.sprites:
                if sp["sprite"].has_key("collision") and self.__collided_with(sp):
                    pygame.mixer.music.set_volume(0.2)
                    crash_sf     = pygame.mixer.Sound("lib/you_fool.ogg")
                    self.crashed = True
                    self.speed   = 0
                    print "crash"

                    crash_sf.play()
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
        elif top["world"]["y"] < bottom["world"]["y"]:
            sprite = "downhill_" + sprite

        if self.speed > 0:
            self.animation_frame += 1

            if self.animation_frame > (s.PLAYER_ANIM_HOLD * 2):
                self.animation_frame = 1

        sprite += "1" if (self.animation_frame < s.PLAYER_ANIM_HOLD) else "2"

        sprite   = s.SPRITES[sprite]
        s_width  = int(sprite["width"] * scale * s.ROAD_WIDTH * 1.2)
        s_height = int(sprite["height"] * scale * s.ROAD_WIDTH * 1.2)

        p = pygame.image.load("lib/" + sprite["path"])
        p = pygame.transform.scale(p, (s_width, s_height))
        window.blit(p, (width - (s_width / 2), s.DIMENSIONS[1] - s_height - s.BOTTOM_OFFSET))

    def render_hud(self, window):
        """Renders a Head-Up display on the active window."""
        center    = (70, s.DIMENSIONS[1] - 70)
        orbit_pos = (self.speed / 6300) + 2.35
        start     = self.__circular_orbit(center, -10, orbit_pos)
        finish    = self.__circular_orbit(center, 36, orbit_pos)

        pygame.draw.circle(window, s.COLOURS["black"], center, 50, 2)
        pygame.draw.circle(window, s.COLOURS["black"], center, 4)
        pygame.draw.line(window, s.COLOURS["black"], start, finish, 3)

    def accelerate(self):
        """Updates speed at appropriate acceleration level."""
        self.speed = u.limit(self.speed + (s.ACCELERATION * self.acceleration), 0, s.TOP_SPEED)

    def travel(self, track_length):
        """Updates position, reflecting how far we've travelled since the last frame."""
        pos = self.position + (s.FRAME_RATE * self.speed)

        while pos >= track_length:
            pos -= track_length

        while pos < 0:
            pos += track_length

        self.position = pos

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
                if keys[K_UP]:
                    a = s.FRAME_RATE
                elif keys[K_DOWN]:
                    a = -(s.FRAME_RATE * s.DECELERATION)

        self.acceleration = a

    def set_direction(self, keys):
        """Updates the direction the player is going, accepts a key-map."""
        d = 0

        if keys[K_LEFT]:
            d = -self.direction_speed()
        elif keys[K_RIGHT]:
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
            step = -0.03 if self.x > 0 else 0.03

            if round(self.x, 1) != 0:
                self.x += step
            else:
                pygame.mixer.music.set_volume(1.0)
                self.crashed = False

    def __collided_with(self, sprite):
        s = sprite["sprite"]
        o = sprite["offset"]

        return (self.x < (o + s["collision"][1]) and o < 0) or\
               (self.x > (o + s["collision"][0]) and o > 0)
 
    def __circular_orbit(self, center, radius, t):
        """Returns the X/Y coordinate for a given time (t) in a circular orbit."""
        theta = math.fmod(t, math.pi * 2)
        c     = math.cos(theta)
        s     = math.sin(theta)

        return center[0] + radius * c, center[1] + radius * s
