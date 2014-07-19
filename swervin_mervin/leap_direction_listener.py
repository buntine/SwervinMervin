import Leap
import settings as s

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

        if len(frame.hands) == 1:
            left = frame.hands[0]
            pos  = left.palm_position[0]

            self.hand_id = left.id

            if pos > s.DIR_THRESHOLD:
                self.direction = "right"
            elif pos < -s.DIR_THRESHOLD:
                self.direction = "left"
            else:
                self.direction = "straight"

    def clean(self):
        self.direction = "straight"
        self.hand_id   = None
