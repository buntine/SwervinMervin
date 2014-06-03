# Swervin' Mervin'
# v0.1
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys
from pygame.locals import *

pygame.init()

# Game variables.
fps            = 30
dimensions     = (640, 480)
segments       = []
road_width     = 2000
segment_length = 200
track_length   = None
lanes          = 3
field_of_view  = 100
camera_height  = 1000
camera_depth   = None
draw_distance  = 300
player_x       = 0
player_z       = None
position       = 0
speed          = 0
max_speed      = segment_length / (1 / fps)
acceleration   = max_speed / 5
breaking       = -max_speed
deceleration   = -max_speed / 5
off_road_decel = -max_speed / 2
off_road_min   = -max_speed / 4

fps_clock = pygame.time.Clock()
window    = pygame.display.set_mode(dimensions)

white = pygame.Color(255, 255, 255)

while True:
    window.fill(white)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps_clock.tick(fps)
