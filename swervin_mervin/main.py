# Swervin' Mervin'
# v0.3
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
player_y     = 0
direction_x  = 0
acceleration = 0
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
    base_segment    = se.find_segment(position, segments)
    base_percent    = (position % s.SEGMENT_HEIGHT) / s.SEGMENT_HEIGHT
    player_percent  = (position % track_length) / track_length
    player_x        = p.steer(player_x, direction_x)
    player_y        = (base_segment["bottom"]["world"]["y"] + (base_segment["top"]["world"]["y"] - base_segment["bottom"]["world"]["y"]) * player_percent)

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

        p.project_line(segment, "top", camera_x - curve - curve_delta, projected_position, player_y)
        p.project_line(segment, "bottom", camera_x - curve, projected_position, player_y)

        curve       += curve_delta
        curve_delta += segment["curve"]

        # Segment is behind us, so ignore it.
        if segment["top"]["camera"]["z"] <= s.CAMERA_DEPTH or\
           segment["bottom"]["screen"]["y"] >= segment["top"]["screen"]["y"]:
            continue

        r.render_grass(window, segment)
        r.render_road(window, segment)
        r.render_player(window, segment)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Steering, acceleration.
    keys         = pygame.key.get_pressed()
    acceleration = p.acceleration(keys)
    direction_x  = p.direction(keys, direction_speed)

    # SLow player down if they are on the grass.
    if player_x > 1.0 or player_x < -1.0:
        if speed > s.OFFROAD_TOP_SPEED:
            acceleration = -(acceleration * 3)

    pygame.display.update()
    fps_clock.tick(s.FPS)
