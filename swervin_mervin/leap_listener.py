import Leap, sys

class LeapListener(Leap.Listener):
    """Listens for and handles leap events."""

    def __init__(self):
        Leap.Listener.__init__(self)
        self.direction = "straight"

    def on_init(self, controller):
        print "Leap Initialized"

    def on_connect(self, controller):
        print "Leap Connected"

    def on_disconnect(self, controller):
        print "Leap Disconnected"

    def on_exit(self, controller):
        print "Leap Exited"

    def on_frame(self, controller):
        frame = controller.frame()

        if len(frame.hands) == 2:
            left  = frame.hands[0]
            right = frame.hands[1]

            if (left.palm_position[1] - 70) > right.palm_position[1]:
                self.direction = "left"
            elif (right.palm_position[1] - 70) > left.palm_position[1]:
                self.direction = "right"
            else:
                self.direction = "straight"
        else:
            self.direction = "straight"
