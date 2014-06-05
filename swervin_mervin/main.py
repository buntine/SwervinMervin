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
road_width     = 2000
speed          = 4 # TODO: Change to 0 once accel/decel implemented.
acceleration   = 4
white          = pygame.Color(255, 255, 255)
light_grey     = pygame.Color(193, 193, 193)
dark_grey      = pygame.Color(123, 123, 123)

fps_clock = pygame.time.Clock()
window    = pygame.display.set_mode(dimensions)
window.fill(white)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps_clock.tick(fps)
