# Swervin' Mervin'
# v0.9
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame
#from pygame.locals import *
import game as g
import settings as s

pygame.init()

fps_clock = pygame.time.Clock()
window    = pygame.display.set_mode(s.DIMENSIONS)
game      = g.Game(window, fps_clock)

while True:
   if game.waiting:
       game.wait()
   else:
       game.play()
