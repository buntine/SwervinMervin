import settings as s
import util as u
import pygame
from pygame.locals import *

class Player:
    """Represents the player in the game world."""

    def __init__(self):
        self.x            = 0
        self.y            = 0
        self.position     = 0
        self.direction    = 0
        self.acceleration = 0
        self.speed        = 1

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
    
        sprite   = s.SPRITES[sprite]
        s_width  = int(sprite["width"] * scale * s.ROAD_WIDTH * 1.2)
        s_height = int(sprite["height"] * scale * s.ROAD_WIDTH * 1.2)

        p = pygame.image.load("lib/" + sprite["path"])
        p = pygame.transform.scale(p, (s_width, s_height))
        window.blit(p, (width - (s_width / 2), s.DIMENSIONS[1] - s_height - s.BOTTOM_OFFSET))

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
        return (s.FRAME_RATE * 2 * self.speed_percent())

    def segment_percent(self):
        """Returns a value between 0 and 1 indicating how far through the current segment we are."""
        return ((self.position + s.PLAYER_Z) % s.SEGMENT_HEIGHT) / s.SEGMENT_HEIGHT
