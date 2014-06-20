class Player:
    """Represents the player in the game world."""

    def __init__(self):
        self.x            = 0
        self.y            = 0
        self.position     = 0
        self.direction    = 0
        self.acceleration = 0
        self.speed        = 0

    def steer(self):
        """Updates x to simulate steering."""
        pass

    def climb(self):
        """Updates y to simulate hill and valley ascension."""
        pass

    def render(self, window, segment):
        """Renders the player sprite to the given surface."""
        pass

    def accelerate(self):
        """Updates speed at appropriate acceleration level."""
        pass

    def set_acceleration(self):
        """Updates the acceleration factor depending on world conditions."""
        pass

    def set_direction(self, keys):
        """Updates the direction the player is going, accepts a key-map."""
        pass
