import settings as s
import world_object as wo

class Sprite(wo.WorldObject):
    """Represents a single sprite in a level."""

    def __init__(self, offset, name):
        self.offset     = offset
        self.sprite     = s.SPRITES[name]
        self.quantifier = 3

    def is_hooker(self):
        """Returns True if this sprite is a live hooker."""
        return self.sprite.has_key("hooker")
