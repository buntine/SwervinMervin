import pygame, os
import settings as s
import world_object as wo

class Competitor(wo.WorldObject):
    """Represents a single competitor car in a level."""

    def __init__(self, position, offset, name, speed):
        self.position   = position * s.SEGMENT_HEIGHT
        self.offset     = offset
        self.offset_y   = 0.0
        self.sprite     = s.SPRITES[name]
        self.speed      = speed
        self.quantifier = 1.8

    def travel(self, track_length):
        # Update Z position.
        pos = self.position + (s.FRAME_RATE * self.speed)

        if pos >= track_length:
            pos -= track_length

        if pos < 0:
            pos += track_length

        self.position = pos

    def path(self):
        return pygame.image.load(os.path.join("lib", self.sprite["path"]))
