# Swervin' Mervin'
# v0.1
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys
from pygame.locals import *

pygame.init()

fps_clock = pygame.time.Clock()
window    = pygame.display.set_mode((640, 480))

white = pygame.Color(255, 255, 255)

while True:
    window.fill(white)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps_clock.tick(30)
