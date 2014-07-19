import pygame, sys, os
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
        self.leap_controller = Leap.Controller()
        self.player_listener = lfl.LeapFingerListener()

    def setup(self):
        self.finger_listener.clean()

        self.leap_controller.add_listener(self.finger_listener)

    def progress(self):
        """Animate the next frame"""
        pass

    def finished(self):
        return False  
