import Leap

class LeapDirectionListener(Leap.Listener):
    """Listens for and handles leap events associated to steering."""

    def __init__(self):
        Leap.Listener.__init__(self)
        self.direction = "straight"

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

        if len(frame.hands) == 1:
            left = frame.hands[0]
            pos  = left.palm_position[0]

            if pos > 30:
                self.direction = "right"
            elif pos < -30:
                self.direction = "left"
            else:
                self.direction = "straight"

    def reset(self):
        self.direction = "straight"
