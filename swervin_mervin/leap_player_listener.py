import Leap

class LeapPlayerListener(Leap.Listener):
    """Listens for player interaction."""

    def __init__(self):
        Leap.Listener.__init__(self)
        self.ready = False

    def on_init(self, controller):
        print "Leap Initialized"

    def on_connect(self, controller):
        print "Leap Player Connected"

    def on_disconnect(self, controller):
        print "Leap Player Disconnected"

    def on_exit(self, controller):
        print "Leap Exited"

    def on_frame(self, controller):
        frame = controller.frame()

        if len(frame.hands) > 0:
            left = frame.hands[0]

            if not self.ready and left.time_visible > 1000:
                self.ready = True

    def reset(self):
        self.ready = False
