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
        self.engine_sfx = pygame.mixer.Sound(os.path.join("lib", "engine.ogg"))

        self.engine_sfx.set_volume(0)

        wo.WorldObject.__init__(self, 1.8)

    def travel(self, track_length):
        # Update Z position.
        pos = self.position + (s.FRAME_RATE * self.speed)

        if pos >= track_length:
            pos -= track_length

        if pos < 0:
            pos += track_length

        self.position = pos

    def play_engine(self, player_position):
        """Plays or stops the engine depending on how far away this competitor is
           from the player."""
        v = self.__engine_volume(player_position)

        if v > 0:
            if self.engine_sfx.get_volume() == 0:
                self.engine_sfx.play()
        else:
            self.engine_sfx.stop()

        self.engine_sfx.set_volume(v)

    def path(self):
        return pygame.image.load(os.path.join("lib", self.sprite["path"]))

    def __engine_volume(self, player_position):
        """Returns a value between 0.0 and 1.0 to indicate how loud this competitors engine
           will sound from the persperctive of the player."""
        distance = abs(self.position - player_position)

        if distance > s.MINIMUM_ENGINE_DIST:
            return 0
        else:
            volume = round(float(distance) / s.MINIMUM_ENGINE_DIST, 1)
            return round(volume - ((volume - 0.5) * 2), 1)
