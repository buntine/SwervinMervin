import Leap
import settings as s
import pygame

class LeapDirectionListener(Leap.Listener):
    """Listens for and handles leap events associated to steering."""

    def __init__(self):
        Leap.Listener.__init__(self)
        self.clean()

    def on_init(self, controller):
        print "Leap Initialized"

    def on_connect(self, controller):
        print "Leap Direction Connected"

    def on_disconnect(self, controller):
        print "Leap Direction Disconnected"

    def on_exit(self, controller):
        print "Leap Exited"

    def on_frame(self, controller):
        frame = controller.frame()

        if len(frame.hands) == 2:
            self.active = True

            left  = frame.hands.leftmost
            right = frame.hands.rightmost
            pos   = right.stabilized_palm_position[1] - left.stabilized_palm_position[1]

            self.hand_id = left.id

            if pos > s.DIR_THRESHOLD:
                self.direction = "right"
            elif pos < -s.DIR_THRESHOLD:
                self.direction = "left"
            else:
                self.direction = "straight"
        else:
            self.active = False

    def clean(self):
        self.direction = "straight"
        self.hand_id   = None
        self.active    = True
