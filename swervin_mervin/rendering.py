# Helper functions for rendering.

import pygame
import settings as s

def render_road(window, segment):
    """Renders the polygons for the road, markers, etc."""
    top      = segment["top"]["screen"]
    bottom   = segment["bottom"]["screen"]
    y_top    = (s.DIMENSIONS[1] - top["y"])
    y_bottom = (s.DIMENSIONS[1] - bottom["y"])
    colour   = segment["colour"]

    # Road.
    points = [((bottom["x"] - bottom["w"]), y_bottom),
              ((bottom["x"] + bottom["w"]), y_bottom),
              ((top["x"] + top["w"]),       y_top),
              ((top["x"] - top["w"]),       y_top)]
    pygame.draw.polygon(window, colour["road"], points)

    top_rumble_width    = top["w"] / (s.LANES * 2)
    bottom_rumble_width = bottom["w"] / (s.LANES * 2)

    # Left rumble strip.
    points = [((bottom["x"] - bottom["w"] - bottom_rumble_width), y_bottom),
              ((bottom["x"] - bottom["w"]),                       y_bottom),
              ((top["x"] - top["w"]),                             y_top),
              ((top["x"] - top["w"] - top_rumble_width),          y_top)]
    pygame.draw.polygon(window, colour["rumble"], points)

    # Right rumble strip.
    points = [((bottom["x"] + bottom["w"] + bottom_rumble_width), y_bottom),
              ((bottom["x"] + bottom["w"]),                       y_bottom),
              ((top["x"] + top["w"]),                             y_top),
              ((top["x"] + top["w"] + top_rumble_width),          y_top)]
    pygame.draw.polygon(window, colour["rumble"], points)

    if (segment["index"] / s.RUMBLE_LENGTH) % 2 == 0:
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
            pygame.draw.polygon(window, colour["line"], points)

def render_grass(window, segment):
    """Renders grass strip for the given segment"""
    top    = segment["top"]["screen"]
    bottom = segment["bottom"]["screen"]
    height = top["y"] - bottom["y"]
    y      = s.DIMENSIONS[1] - top["y"]

    pygame.draw.rect(window,
      segment["colour"]["grass"],
      (0, y, s.DIMENSIONS[0], height),
      int(height <= 1))

def render_player(window, segment, direction_x, player_percent):
    """Renders the players car to the screen, with appropriate scaling and rotation"""
    top    = segment["top"]
    bottom = segment["bottom"]
    width  = s.DIMENSIONS[0] / 2
    height = s.DIMENSIONS[1] / 2
    scale  = s.CAMERA_DEPTH / (s.CAMERA_HEIGHT * s.CAMERA_DEPTH)
    sprite = "straight"

    if direction_x > 0:
        sprite = "right"
    elif direction_x < 0:
        sprite = "left"

    if top["world"]["y"] > bottom["world"]["y"]:
        sprite = "uphill_" + sprite
    elif top["world"]["y"] < bottom["world"]["y"]:
        sprite = "downhill_" + sprite

    sprite   = s.SPRITES[sprite]
    s_width  = int(sprite["width"] * scale * s.ROAD_WIDTH * 1.2)
    s_height = int(sprite["height"] * scale * s.ROAD_WIDTH * 1.2)

    player = pygame.image.load("lib/" + sprite["path"])
    player = pygame.transform.scale(player, (s_width, s_height))
    window.blit(player, (width - (s_width / 2), s.DIMENSIONS[1] - s_height - s.BOTTOM_OFFSET))

def render_sprites(window, segment):
    """Renders the sprites with the appropriate scaling for the given segment"""
    bottom = segment["bottom"]["screen"]

    for sp in segment["sprites"]:
        s_width  = int(sp["sprite"]["width"] * bottom["s"] * s.ROAD_WIDTH * 1.2)
        s_height = int(sp["sprite"]["height"] * bottom["s"] * s.ROAD_WIDTH * 1.2)
        x        = (bottom["x"] - s_width) + (bottom["w"] * sp["offset"])
        y        = s.DIMENSIONS[1] - bottom["y"] - s_height
        sprite   = pygame.image.load("lib/" + sp["sprite"]["path"])
        sprite   = pygame.transform.scale(sprite, (s_width, s_height))

        window.blit(sprite, (x, y))

def render_background(window, curve):
    pass
