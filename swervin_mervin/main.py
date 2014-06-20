# Swervin' Mervin'
# v0.3
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys
from pygame.locals import *
import player as pl
import projection as p
import util as u
import rendering as r
import segmentation as se
import settings as s

pygame.init()

player       = pl.Player()
segments     = se.build_level()
track_length = len(segments) * s.SEGMENT_HEIGHT
fps_clock    = pygame.time.Clock()
window       = pygame.display.set_mode(s.DIMENSIONS)

while True:
    window.fill(s.COLOURS["sky"])

    player.travel(track_length)

    base_segment   = se.find_segment(player.position, segments)
    player_segment = se.find_segment((player.position + s.PLAYER_Z), segments)

    player.accelerate()
    player.steer(player_segment)
    player.climb(base_segment)
 
    y_coverage  = 0
    curve       = 0
    curve_delta = -(base_segment["curve"] * player.segment_percent())

    r.render_background(window, curve_delta)

    # Loop through segments we should draw for this frame.
    for i in range(s.DRAW_DISTANCE):
        index              = (base_segment["index"] + i) % len(segments)
        segment            = segments[index]
        projected_position = player.position
        camera_x           = player.x * s.ROAD_WIDTH

        # Past end of track and looped back.
        if segment["index"] < base_segment["index"]:
            projected_position -= track_length

        p.project_line(segment, "top", camera_x - curve - curve_delta, projected_position, player.y)
        p.project_line(segment, "bottom", camera_x - curve, projected_position, player.y)

        curve       += curve_delta
        curve_delta += segment["curve"]

        # Segment is behind us or over a hill, so ignore it.
        if segment["top"]["camera"]["z"] <= s.CAMERA_DEPTH or\
           segment["top"]["screen"]["y"] <= y_coverage or\
           segment["bottom"]["screen"]["y"] >= segment["top"]["screen"]["y"]:
            continue

        if (segment["top"]["screen"]["y"] > y_coverage):
            y_coverage = segment["top"]["screen"]["y"]

        r.render_grass(window, segment)
        r.render_road(window, segment)

    # Draw sprites in from back to front (painters algorithm).
    for i in reversed(range(1, s.DRAW_DISTANCE)):
        index   = (base_segment["index"] + i) % len(segments)
        segment = segments[index]
 
        r.render_sprites(window, segment)

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
