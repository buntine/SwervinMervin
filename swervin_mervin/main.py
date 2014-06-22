# Swervin' Mervin'
# v0.3
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys
from pygame.locals import *
import player as p
import level as l
import rendering as r
import settings as s

pygame.init()

player    = p.Player()
level     = l.Level("levels/city.lvl")
fps_clock = pygame.time.Clock()
window    = pygame.display.set_mode(s.DIMENSIONS)

level.build()

while True:
    window.fill(s.COLOURS["sky"])

    player.travel(level.track_length())

    base_segment   = level.find_segment(player.position)
    player_segment = level.find_segment(player.position + s.PLAYER_Z)

    player.accelerate()
    player.steer(player_segment)
    player.climb(base_segment)
 
    y_coverage  = 0
    curve       = 0
    curve_delta = -(base_segment.curve * player.segment_percent())

    r.render_background(window, curve_delta)

    # Loop through segments we should draw for this frame.
    for i in range(s.DRAW_DISTANCE):
        segment            = level.offset_segment(base_segment.index + i)
        projected_position = player.position
        camera_x           = player.x * s.ROAD_WIDTH

        # Past end of track and looped back.
        if segment.index < base_segment.index:
            projected_position -= level.track_length()

        segment.project(camera_x,
          curve,
          curve_delta,
          projected_position,
          player.y)

        curve       += curve_delta
        curve_delta += segment.curve

        if segment.should_ignore(y_coverage):
            continue

        if (segment.top["screen"]["y"] > y_coverage):
            y_coverage = segment.top["screen"]["y"]

        segment.render_grass(window)
        segment.render_road(window)

    # Draw sprites in from back to front (painters algorithm).
    for i in reversed(range(1, s.DRAW_DISTANCE)):
        segment = level.offset_segment(base_segment.index + i)
        segment.render_sprites(window)

    player.render(window, base_segment)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Steering, acceleration.
    keys = pygame.key.get_pressed()
    player.set_acceleration(keys)
    player.set_direction(keys)

    pygame.display.update()
    fps_clock.tick(s.FPS)
