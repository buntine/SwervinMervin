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
speed          = 3 # TODO: Change to 0 once accel/decel implemented.
acceleration   = 3
white          = pygame.Color(255, 255, 255)
light_grey     = pygame.Color(193, 193, 193)
dark_grey      = pygame.Color(123, 123, 123)

fps_clock = pygame.time.Clock()
window    = pygame.display.set_mode(dimensions)

height = 50

while True:
    window.fill(white)

    for n in range(10):
        color = dark_grey if (n % 2 == 0) else light_grey
        pygame.draw.rect(window, color, (0, (480 - height), 640, height), 0)
        height = (height - acceleration);

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    height = 50

    pygame.display.update()
    fps_clock.tick(fps)
