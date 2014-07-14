# Swervin' Mervin'
# v0.9
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys, os
from game import *
import level as l
import settings as s

pygame.init()

window = pygame.display.set_mode(s.DIMENSIONS)
level  = l.Level("melbourne")

title_sequence(window, level)
