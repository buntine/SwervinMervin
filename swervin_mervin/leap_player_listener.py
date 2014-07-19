import Leap

class LeapPlayerListener(Leap.Listener):
    """Listens for player interaction."""

    def __init__(self):
        Leap.Listener.__init__(self)
        self.clean()

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

            if not self.ready and left.id != self.hand_id and left.time_visible > 3000:
                self.ready = True

    def clean(self):
        # We store the Hand ID that we were last tracking with the directional listener.
        # This way we ensure that we don't just automatically play again before the player
        # removes their hand.
        self.ready   = False
        self.hand_id = None
