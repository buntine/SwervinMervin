import pygame
import settings as s

class Segment:
    """Represents a single segment in a level."""

    def __init__(self, palette, index, curve, start_y, end_y):
        self.index         = index
        self.curve         = curve
        self.sprites       = []
        self.competitors   = []
        self.pre_polygons  = []
        self.post_polygons = []
        self.clip          = [0, 0, 0]
        self.in_tunnel     = False
        self.tunnel_end    = False
        self.speed_boost   = False
        self.palette       = palette
        self.top           = self.__initialize_line(end_y, index + 1)
        self.bottom        = self.__initialize_line(start_y, index)

    def project(self, camera_x, curve, curve_delta, position, player_y):
        """Modifies the segment lines in place, projecting them to 2D coordinates."""
        self.__project_line("top", camera_x - curve - curve_delta, position, player_y)
        self.__project_line("bottom", camera_x - curve, position, player_y)

    def should_ignore(self, segment):
        """Returns true if this segment will be projected behind a hill, or behind us, etc."""
        return self.top["camera"]["z"] <= s.CAMERA_DEPTH or\
               self.top["screen"]["y"] <= segment.top["screen"]["y"] or\
               self.bottom["screen"]["y"] >= self.top["screen"]["y"]

    def render_grass(self, window):
        """Renders the grass for this segment to the given surface."""
        top    = self.top["screen"]
        bottom = self.bottom["screen"]
        height = top["y"] - bottom["y"]
        y      = s.DIMENSIONS[1] - top["y"]
        col    = s.COLOURS["tunnel"] if self.in_tunnel else self.palette["grass"]

        pygame.draw.rect(window, col,
          (0, y, s.DIMENSIONS[0], height),
          int(height <= 1))

    def render_road(self, window):
        """Renders the road for this segment to the given surface."""
        top      = self.top["screen"]
        bottom   = self.bottom["screen"]
        y_top    = (s.DIMENSIONS[1] - top["y"])
        y_bottom = (s.DIMENSIONS[1] - bottom["y"])
        col      = self.palette

        # Road.
        points = [((bottom["x"] - bottom["w"]), y_bottom),
                  ((bottom["x"] + bottom["w"]), y_bottom),
                  ((top["x"] + top["w"]),       y_top),
                  ((top["x"] - top["w"]),       y_top)]
        pygame.draw.polygon(window, col["road"], points)

        # Speed boost.
        if self.speed_boost and self.index % 5 == 0:
            points = [(bottom["x"], y_bottom),
                      (bottom["x"] + bottom["w"], y_bottom),
                      (top["x"] + (top["w"] / 2), y_top),
                      (bottom["x"], y_bottom)]
            pygame.draw.polygon(window, s.COLOURS["green"], points)

        top_footpath_width    = top["w"] / (s.LANES / 2.8)
        bottom_footpath_width = bottom["w"] / (s.LANES / 2.8)

        # Left footpath strip.
        if not self.in_tunnel:
            points = [((bottom["x"] - bottom["w"] - bottom_footpath_width), y_bottom),
                      ((bottom["x"] - bottom["w"]),                         y_bottom),
                      ((top["x"] - top["w"]),                               y_top),
                      ((top["x"] - top["w"] - top_footpath_width),          y_top)]
            pygame.draw.polygon(window, col["footpath"], points)

            # Left gutter.
            pygame.draw.line(window, s.COLOURS["gutter"],
              (bottom["x"] - bottom["w"], y_bottom), (top["x"] - top["w"], y_top))

            # Right footpath strip.
            points = [((bottom["x"] + bottom["w"] + bottom_footpath_width), y_bottom),
                      ((bottom["x"] + bottom["w"]),                         y_bottom),
                      ((top["x"] + top["w"]),                               y_top),
                      ((top["x"] + top["w"] + top_footpath_width),          y_top)]
            pygame.draw.polygon(window, col["footpath"], points)

            # Right gutter.
            pygame.draw.line(window, s.COLOURS["gutter"],
              (bottom["x"] + bottom["w"], y_bottom), (top["x"] + top["w"], y_top))

        if (self.index / s.RUMBLE_LENGTH) % 2 == 0:
            # Road lanes.
            top_line_width    = top["w"] / (s.LANES * 8)
            bottom_line_width = bottom["w"] / (s.LANES * 8)
            step              = 1 / float(s.LANES)

            # Render each lane separator.
            for lane in range(s.LANES - 1):
                lane_percent  = step * (lane + 1)
                lane_bottom_w = (bottom["w"] * 2) * lane_percent
                lane_top_w    = (top["w"] * 2) * lane_percent
                bottom_left   = bottom["x"] - bottom["w"] + lane_bottom_w
                bottom_right  = bottom_left + bottom_line_width
                top_left      = top["x"] - top["w"] + lane_top_w
                top_right     = top_left + top_line_width

                points = [(bottom_left,  y_bottom),
                          (bottom_right, y_bottom),
                          (top_right,    y_top),
                          (top_left,     y_top)]
                pygame.draw.polygon(window, col["line"], points)

    def render_polygons(self, window, full_clip):
        """Renders the polygons/shapes (if any) for this segment to the given surface.
           These are rendered after the track, but before the sprites."""
        for obj in self.pre_polygons:
            obj.render(window, self.bottom["screen"], self.clip, full_clip)

    def render_world_objects(self, window):
        """Renders the sprites/competitors (if any) for this segment to the given surface."""
        for obj in (self.sprites + self.competitors + self.post_polygons):
            obj.render(window, self)

    def render_tunnel_roof(self, window, highest_y):
        """Renders the tunnel roof, accounting for the exit hole if it's visible."""
        if not self.tunnel_end:
            pygame.draw.rect(window, s.COLOURS["tunnel"],
              (0, 0, s.DIMENSIONS[0], s.DIMENSIONS[1] - highest_y))
        else:
            # I am mirroring the roof and road segment heights here.
            # Not sure if this will work in all circumstances (hills, etc).
            pygame.draw.rect(window, s.COLOURS["tunnel"],
              (0, 0, s.DIMENSIONS[0], self.top["screen"]["y"] - (s.TUNNEL_HEIGHT / 4)))

    def render_left_tunnel(self, window):
        bottom   = self.bottom["screen"]
        y_bottom = (s.DIMENSIONS[1] - bottom["y"])

        points = [(0, y_bottom),
                  ((bottom["x"] - bottom["w"]), y_bottom),
                  ((bottom["x"] - bottom["w"]), 0),
                  (0, 0)]
        pygame.draw.polygon(window, s.COLOURS["tunnel"], points)

    def render_right_tunnel(self, window):
        bottom   = self.bottom["screen"]
        y_bottom = (s.DIMENSIONS[1] - bottom["y"])

        points = [((bottom["x"] + bottom["w"]), y_bottom),
                  (s.DIMENSIONS[0], y_bottom),
                  (s.DIMENSIONS[0], 0),
                  ((bottom["x"] + bottom["w"]), 0)]
        pygame.draw.polygon(window, s.COLOURS["tunnel"], points)

    def remove_sprite(self, sprite):
        """Permanently removes the given sprite from this segment."""
        try:
            self.sprites.remove(sprite)
        except Exception:
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

    def __initialize_line(self, y, height):
        return {"world": {"y": y,
                          "z": (height * s.SEGMENT_HEIGHT)},
                "camera": {},
                "screen": {}}
