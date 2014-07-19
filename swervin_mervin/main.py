# Swervin' Mervin'
# v0.9
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame
import level as l
import settings as s
import game as g
import player as p
import high_score as hs
import title_screen as ts

pygame.init()

#window = pygame.display.set_mode(s.DIMENSIONS)
#level  = l.Level("melbourne")

# Maybe each stage shuldbe a class that can .setup() and .progress() while .alive() is true?

#title_sequence(window, level)

###

window       = pygame.display.set_mode(s.DIMENSIONS)
level        = l.Level("melbourne")
title_screen = ts.TitleScreen(window)
player       = p.Player(window)
game         = g.Game(window, player, level)

while True:
    # Fire up the title screen.
    title_screen.setup()
    while not title_screen.finished:
        title_screen.progress()

    # Play the game.
    game.setup()
    while not game.finished():
        game.progress()

    # Enter name for high score record.
    if game.high_score():
        high_score = hs.HighScore(window, player, level)
        high_score.setup()
        while not high_score.finished():
            high_score.progress()
        high_score.clean()

    # Resume game in "game over" mode, waiting for new player.
    game.game_over()
    while not game.finished():
        game.progress()

    # New player found, reset everything and resume.
    game.clean()
    player.clean()
