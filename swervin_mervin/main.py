# Swervin' Mervin'
# v0.8
# (c) Andrew Buntine
# https://github.com/buntine/swervin_mervin

import pygame, sys, os
from pygame.locals import *
import player as p
import background as b
import level as l
import title_screen as ts
import settings as s
import Leap
import leap_listener as ll

pygame.init()

fps_clock    = pygame.time.Clock()
window       = pygame.display.set_mode(s.DIMENSIONS)
title_screen = ts.TitleScreen()

## Fire up the title screen.
pygame.mixer.music.load(os.path.join("lib", "mn84-theme.mp3"))
pygame.mixer.music.play(-1)

while not title_screen.finished:
    title_screen.progress(window)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and title_screen.ready:
                pygame.mixer.music.fadeout(1500)
                title_screen.finished = True
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps_clock.tick(s.TITLE_FPS)

## Now lets play!
player      = p.Player()
level       = l.Level("melbourne")
backgrounds = [b.Background("sky", 0, 2, True),
                b.Background("city", 0, 1)]
listener    = ll.LeapListener()
controller  = Leap.Controller()

controller.add_listener(listener)
level.build()

pygame.mixer.music.load(os.path.join("lib", "lazerhawk-overdrive.mp3"))
pygame.mixer.music.play(-1)

while True:
    player.travel(level.track_length(), window)

    base_segment   = level.find_segment(player.position)
    player_segment = level.find_segment(player.position + s.PLAYER_Z)

    player.accelerate()
    player.steer(player_segment)
    player.climb(base_segment)
    player.detect_collisions(player_segment)
    player.handle_crash()

    # Move the other players.
    for c in level.competitors:
        old_seg = level.find_segment(c.position)
        c.travel(level.track_length())
        new_seg = level.find_segment(c.position)

        if old_seg.index != new_seg.index:
            if c in old_seg.competitors:
                old_seg.competitors.remove(c)
            new_seg.competitors.append(c)

    y_coverage  = 0
    curve       = 0
    curve_delta = -(base_segment.curve * player.segment_percent())

    # Position backgrounds according to current curve.
    for bg in backgrounds:
        if base_segment.curve != 0:
            bg.step(base_segment.curve, player.speed_percent())
        bg.render(window)

    # Loop through segments we should draw for this frame.
    for i in range(s.DRAW_DISTANCE):
        segment            = level.offset_segment(base_segment.index + i)
        projected_position = player.position
        camera_x           = player.x * s.ROAD_WIDTH

        # Past end of track and looped back.
        if segment.index < base_segment.index:
            projected_position -= level.track_length()

        segment.project(camera_x,
          curve,
          curve_delta,
          projected_position,
          player.y)

        curve       += curve_delta
        curve_delta += segment.curve

        # Remember highest Y coordinate so we can clip sprites later.
        segment.clip = y_coverage

        if segment.should_ignore(y_coverage):
            continue

        segment.render_grass(window)
        segment.render_road(window)

        if (segment.top["screen"]["y"] > y_coverage):
            y_coverage = segment.top["screen"]["y"]

    # Draw sprites in from back to front (painters algorithm).
    if segment.index != base_segment.index:
        for i in reversed(range(1, s.DRAW_DISTANCE)):
            segment = level.offset_segment(base_segment.index + i)
            segment.render_sprites(window)
            segment.render_competitors(window)

        player.render(window, base_segment)
        player.render_hud(window)

    for event in pygame.event.get():
        if event.type == QUIT:
            controller.remove_listener(listener) 
            pygame.quit()
            sys.exit()

    # Steering, acceleration.
    keys = pygame.key.get_pressed()
    player.set_acceleration(keys)
    player.set_direction(keys, listener.direction)

    pygame.display.update()
    fps_clock.tick(s.FPS)
