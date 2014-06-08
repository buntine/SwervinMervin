# Swervin' Mervin'
# v0.1
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys, math
from pygame.locals import *
from projection import *

pygame.init()

# Game variables.
fps            = 50
position       = 0
dimensions     = (640, 480)
segment_height = 200
rumble_length  = 3
speed          = 1
draw_distance  = 100
road_width     = 1500
top_speed      = (segment_height / (1.0/fps))
acceleration   = top_speed / 5.0
field_of_view  = 100 # Degrees
camera_height  = 1000
camera_depth   = 1 / math.tan((field_of_view / 2) * math.pi / 180);
player_x       = 0
player_z       = camera_height * camera_depth
colours        = {"white": pygame.Color(255, 255, 255),
                  "light_grey": pygame.Color(193, 193, 193),
                  "dark_grey": pygame.Color(123, 123, 123)}

segments       = build_segments(segment_height, rumble_length, colours["dark_grey"], colours["light_grey"])
track_length   = len(segments) * segment_height

fps_clock = pygame.time.Clock()
window    = pygame.display.set_mode(dimensions)

while True:
    window.fill(colours["white"])

    position += (0.02 * speed)
    speed += (acceleration * 0.02)

    if position > track_length:
        position = 0

    if speed > top_speed:
        speed = top_speed

    base_segment = find_segment(position, segments, segment_height)

    for s in range(draw_distance):
        index             = (base_segment["index"] + s) % len(segments)
        segment           = segments[index]

        segment["bottom"] = project_line(segment, "bottom", (player_x * road_width), camera_height, position, camera_depth, dimensions, road_width)
        segment["top"]    = project_line(segment, "top", (player_x * road_width), camera_height, position, camera_depth, dimensions, road_width)
        segments[index]   = segment

        # Segment is behind us.
        if segment["bottom"]["camera"]["z"] <= camera_depth:
            continue

        print segments[index]
        render_segment(segment)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps_clock.tick(fps)
