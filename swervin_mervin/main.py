# Swervin' Mervin'
# v0.9
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys, os
from game import *
import level as l
import settings as s

pygame.init()

window          = pygame.display.set_mode(s.DIMENSIONS)
level           = l.Level("melbourne")

if s.TITLE_SCREEN:
    title_sequence(window)

player = play(window, level)

if level.is_high_score(player.points):
    high_score_entry(window, player)
