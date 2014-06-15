# Swervin' Mervin'
# v0.1
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys
from pygame.locals import *
import projection as p
import rendering as r
import segmentation as se
import settings as s

pygame.init()

# Game variables.
position     = 0
speed        = 1
player_x     = 0
direction_x  = 0
acceleration = 0
player_z     = s.CAMERA_HEIGHT * s.CAMERA_DEPTH
segments     = se.build_level()
track_length = len(segments) * s.SEGMENT_HEIGHT

fps_clock = pygame.time.Clock()
window    = pygame.display.set_mode(s.DIMENSIONS)

while True:
    window.fill(s.COLOURS["sky"])

    position        = p.position(position, speed, track_length)
    speed           = p.accelerate(speed, acceleration)
    speed_percent   = speed / s.TOP_SPEED
    direction_speed = (s.FRAME_RATE * 2 * speed_percent)
    player_x        = p.steer(player_x, direction_x)
    base_segment    = se.find_segment(position, segments)
    base_percent    = (position % s.SEGMENT_HEIGHT) / s.SEGMENT_HEIGHT

    player_x    -= (direction_speed * speed_percent * base_segment["curve"] * s.CENTRIFUGAL_FORCE)
    curve_delta  = -(base_segment["curve"] * base_percent)
    curve        = 0

    r.render_background(window, curve_delta)

    # Loop through segments we should draw for this frame.
    for i in range(s.DRAW_DISTANCE):
        index              = (base_segment["index"] + i) % len(segments)
        segment            = segments[index]
        projected_position = position
        camera_x           = player_x * s.ROAD_WIDTH

        # Past end of track and looped back.
        if segment["index"] < base_segment["index"]:
            projected_position -= track_length

        p.project_line(segment, "top", camera_x - curve - curve_delta, projected_position)
        p.project_line(segment, "bottom", camera_x - curve, projected_position)

        curve       += curve_delta
        curve_delta += segment["curve"]

        # Segment is behind us, so ignore it.
        if segment["bottom"]["camera"]["z"] <= s.CAMERA_DEPTH:
            continue

        r.render_grass(window, segment)
        r.render_road(window, segment)
        r.render_player(window, segment)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[K_UP]:
        acceleration = s.FRAME_RATE
    else:
        acceleration = -s.FRAME_RATE

    if keys[K_DOWN]:
        acceleration = -(s.FRAME_RATE * s.DECELERATION)

    if keys[K_LEFT]:
        direction_x = -direction_speed
    elif keys[K_RIGHT]:
        direction_x = direction_speed
    else:
        direction_x = 0

    pygame.display.update()
    fps_clock.tick(s.FPS)
