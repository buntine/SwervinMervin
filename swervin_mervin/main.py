# Swervin' Mervin'
# v0.1
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys
from pygame.locals import *
import projection as p
import rendering as r
import settings as s

pygame.init()

# Game variables.
position     = 0
speed        = 1
player_x     = 0
direction_x  = 0
acceleration = 0
player_z     = s.CAMERA_HEIGHT * s.CAMERA_DEPTH
segments     = p.build_segments()
track_length = len(segments) * s.SEGMENT_HEIGHT

fps_clock = pygame.time.Clock()
window    = pygame.display.set_mode(s.DIMENSIONS)

while True:
    window.fill(s.COLOURS["sky"])

    position += s.FRAME_RATE * speed
    speed    += (s.ACCELERATION * acceleration)
    player_x += direction_x

    # TODO: Move.
    # Prevent player from going too far off track.
    if player_x < -1.8:
        player_x = -1.8
    elif player_x > 1.8:
        player_x = 1.8

    # TODO: Move.
    while position >= track_length:
        position -= track_length
    while position < 0:
        position += track_length

    # TODO: Move.
    if speed > s.TOP_SPEED:
        speed = s.TOP_SPEED
    if speed < 0:
        speed = 0

    base_segment = p.find_segment(position, segments)

    # Loop through segments we should draw for this frame.
    for i in range(s.DRAW_DISTANCE):
        index              = (base_segment["index"] + i) % len(segments)
        segment            = segments[index]
        projected_position = position

        # Past end of track and looped back.
        if segment["index"] < base_segment["index"]:
            projected_position -= track_length

        p.project_line(segment, "top", (player_x * s.ROAD_WIDTH), projected_position)
        p.project_line(segment, "bottom", (player_x * s.ROAD_WIDTH), projected_position)

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
        elif event.type == KEYDOWN:
            # Go left.
            if event.key == K_LEFT:
                direction_x = -(s.FRAME_RATE * 2 * (speed / s.TOP_SPEED))

            # Go right.
            elif event.key == K_RIGHT:
                direction_x = (s.FRAME_RATE * 2 * (speed / s.TOP_SPEED))

            # Accelerate!
            elif event.key == K_UP:
                acceleration = s.FRAME_RATE

            # Decelerate.
            elif event.key == K_DOWN:
                acceleration = -s.FRAME_RATE
        else:
            direction_x  = 0
            acceleration = 0

    pygame.display.update()
    fps_clock.tick(s.FPS)
