import pygame, sys, os
from pygame.locals import *
import player as p
import background as b
import settings as s
import leap_direction_listener as ldl
import leap_finger_listener as lfl
import title_screen as ts
import Leap

def title_sequence(window):
    fps_clock       = pygame.time.Clock()
    title_screen = ts.TitleScreen()

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

def play(window, level):
    fps_clock       = pygame.time.Clock()
    player             = p.Player()
    backgrounds        = [b.Background("sky", 0, 2, True),
                         b.Background("city", 0, 1)]
    direction_listener = ldl.LeapDirectionListener()

    leap_controller = Leap.Controller()

    leap_controller.add_listener(direction_listener)
    level.build()

    pygame.mixer.music.load(os.path.join("lib", "lazerhawk-overdrive.mp3"))
    pygame.mixer.music.play(-1)

    while not (player.game_over and level.is_high_score(player.points)):
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
                segment.render_world_objects(window)

            player.render(window, base_segment)
            player.render_hud(window, level.high_scores)

        # Steering, acceleration.
        keys = pygame.key.get_pressed()
        player.set_acceleration(keys)
        player.set_direction(keys, direction_listener.direction)

        for event in pygame.event.get():
            if event.type == QUIT:
                leap_controller.remove_listener(direction_listener) 
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fps_clock.tick(s.FPS)

    leap_controller.remove_listener(direction_listener) 

    return player

def high_score_entry(window, player):
    fps_clock       = pygame.time.Clock()
    keyboard        = pygame.image.load(os.path.join("lib", "keyboard.png"))
    finger_listener = lfl.LeapFingerListener()

    leap_controller = Leap.Controller()

    leap_controller.add_listener(finger_listener)

    while True:
        window.fill(s.COLOURS["white"])
        window.blit(keyboard, (0, 40))

        pygame.draw.circle(window, s.COLOURS["red"], (finger_listener.x, finger_listener.y), 4)

        for event in pygame.event.get():
            if event.type == QUIT:
                leap_controller.remove_listener(finger_listener) 
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fps_clock.tick(s.FPS)
