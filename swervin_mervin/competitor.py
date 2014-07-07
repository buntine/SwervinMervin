import settings as s

class Competitor:
    """Represents a single competitor car in a level."""

    def __init__(self, position, offset, name, speed):
        self.position = position
        self.offset   = offset
        self.sprite   = s.SPRITES[name]
        self.speed    = speed

    def travel(self, track_length):
        # Update Z position.
        pos = self.position + (s.FRAME_RATE * self.speed)

        if pos >= track_length:
            pos -= track_length

        if pos < 0:
            pos += track_length

        self.position = pos
