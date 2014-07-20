import pygame, sys, os, math
from pygame.locals import *
import settings as s
import leap_finger_listener as lfl
import Leap

class HighScore:
    """Represents the overall game flow"""

    def __init__(self, window, player, level):
        self.window          = window
        self.player          = player
        self.level           = level
        self.fps_clock       = pygame.time.Clock()
        self.keyboard        = pygame.image.load(os.path.join("lib", "keyboard.png"))
        self.leap_controller = Leap.Controller()
        self.finger_listener = lfl.LeapFingerListener()

    def setup(self):
        self.finger_listener.clean()

        self.leap_controller.add_listener(self.finger_listener)

    def progress(self):
        """Animate the next frame"""
        self.window.fill(s.COLOURS["white"])
        self.window.blit(self.keyboard, (0, 40))

        pygame.draw.circle(self.window, s.COLOURS["red"], (self.finger_listener.x, self.finger_listener.y), 4)

        for event in pygame.event.get():
            if event.type == QUIT:
                self.leap_controller.remove_listener(self.finger_listener) 
                pygame.quit()
                sys.exit()

        pygame.display.update()
        self.fps_clock.tick(s.FPS)

    def finished(self):
        return self.finger_listener.finished

    def save(self):
        """Writes high score to appropriate file"""
        score = math.trunc(self.player.points)

        self.level.add_high_score(self.finger_listener.name(), score)
        self.level.flush_high_scores()

    def reset(self):
        self.leap_controller.remove_listener(self.finger_listener) 
