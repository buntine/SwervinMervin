import settings as s
import world_object as wo

class Sprite(wo.WorldObject):
    """Represents a single sprite in a level."""

    def __init__(self, offset, name):
        self.offset     = offset
        self.sprite     = s.SPRITES[name]
        self.quantifier = 3
