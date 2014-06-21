import pygame

class Segment:
    """Represents a single segment in a level."""

    def __init__(palette, index, curve, start_y, end_y):
        self.index   = index
        self.curve   = curve
        self.sprites = sprites
        self.colour  = palette
        self.top     = self.__initialize_line(end_y, index + 1)
        self.bottom  = self.__initialize_line(start_y, index)

    def project(self, camera_x, curve, curve_delta, position, player_y):
        """Modifies the segment lines in place, projecting them to 2D coordinates."""
        self.__project_line("top", camera_x - curve - curve_delta, position, player_y)
        self.__project_line("bottom", camera_x - curve, position, player_y)

    def should_ignore(self, y_coverage):
        """Returns true if this segment will be projected behind a hill, or behind us, etc."""
        return self.top["camera"]["z"] <= s.CAMERA_DEPTH or\
               self.top["screen"]["y"] <= y_coverage or\
               self.bottom["screen"]["y"] >= self.top["screen"]["y"]

    def render_grass(self, window):
        """Renders the grass for this segment to the given surface."""
        top    = self.top["screen"]
        bottom = self.bottom["screen"]
        height = top["y"] - bottom["y"]
        y      = s.DIMENSIONS[1] - top["y"]

        pygame.draw.rect(window,
          self.colour["grass"],
          (0, y, s.DIMENSIONS[0], height),
          int(height <= 1))

    def render_road(self, window):
        """Renders the road for this segment to the given surface."""
        pass

    def render_sprites(self, window):
        """Renders the sprites (if any) for this segment to the given surface."""
        pass

    def __project_line(self, line, camera_x, camera_z, player_y):
        """Projects a 3D world position into 2D coordinates for the given line."""
        p      = getattr(self, line)
        width  = s.DIMENSIONS[0] / 2
        height = s.DIMENSIONS[1] / 2

        p["camera"]["x"] = p["world"].get("x", 0) - camera_x
        p["camera"]["y"] = p["world"].get("y", 0) - (s.CAMERA_HEIGHT + player_y)
        p["camera"]["z"] = p["world"].get("z", 0) - camera_z
        p["screen"]["s"] = s.CAMERA_DEPTH / p["camera"]["z"]
        p["screen"]["x"] = round(width + (p["screen"]["s"] * p["camera"]["x"] * width))
        p["screen"]["y"] = round(height + (p["screen"]["s"] * p["camera"]["y"] * height))
        p["screen"]["w"] = round(p["screen"]["s"] * s.ROAD_WIDTH * width)

    def __initialize_line(y, height)
        return {"world": {"y": y,
                          "z": (height * s.SEGMENT_HEIGHT)},
                "camera": {},
                "screen": {}}
