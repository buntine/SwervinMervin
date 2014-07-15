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

# Maybe each stage shuldbe a class that can .setup() and .progress() while .alive() is true?

title_sequence(window, level)

#ts = title_screen(window)

#while True:
#    p  = Player()
#    l  = Level()
#    g  = Game(window, p, l)

#    Fire up the title screen.
#    ts.setup()
#    while not ts.finished:
#        ts.progress()
#    ts.clean()

#    Play the game.
#    g.setup()
#    while not g.finished:
#        g.progress()
#    g.clean()

#    Enter name for high score entry.
#    if p.high_score():
#        h = HighScore(window, p, l)
#        h.setup()
#        while not h.finished():
#            h.progress()
#        h.clean()

#    Resume game in "game over" mode, waiting for new player.
#    g.game_over()
#    while not g.finished:
#        g.progress()
#    g.clean()
