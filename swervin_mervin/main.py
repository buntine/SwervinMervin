# Swervin' Mervin'
# v0.1
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys
from pygame.locals import *

pygame.init()

# Game variables.
fps            = 50
dimensions     = (640, 480)
road_width     = 2000
speed          = 3 # TODO: Change to 0 once accel/decel implemented.
acceleration   = 3
white          = pygame.Color(255, 255, 255)
light_grey     = pygame.Color(193, 193, 193)
dark_grey      = pygame.Color(123, 123, 123)

fps_clock = pygame.time.Clock()
window    = pygame.display.set_mode(dimensions)

t = 0

while True:
    window.fill(white)

    z = t
    dz = 0
    ddz = 3

    for n in range(240):
        dz += ddz
        z += dz

        if z < 4000:
            color = dark_grey
        elif z > 8000:
            z = 0
            color = dark_grey
        elif z > 4000:
            color = light_grey

        pygame.draw.line(window, color, (0, 480 - n), (640, 480 - n), 1)

    if t > 8000:
        t = 0
    else:
        t += 800

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps_clock.tick(fps)
