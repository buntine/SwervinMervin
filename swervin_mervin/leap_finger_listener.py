import Leap, sys
import settings as s
from Leap import KeyTapGesture

class LeapFingerListener(Leap.Listener):
    """Listens for and handles leap events associated to finger pointing."""

    def __init__(self):
        Leap.Listener.__init__(self)
        self.x         = 0
        self.y         = 0
        self.finished  = False
        self.key       = None
        self.chars     = []
        self.key_map   = {
          "Q": (0, 40, 63, 66),
          "W": (63, 40, 63, 66),
          "E": (126, 40, 63, 66),
          "R": (189, 40, 63, 66),
          "T": (252, 40, 63, 66),
          "Y": (315, 40, 63, 66),
          "U": (378, 40, 63, 66),
          "I": (441, 40, 63, 66),
          "O": (504, 40, 63, 66),
          "P": (567, 40, 63, 66),
          "A": (44, 106, 63, 66),
          "S": (107, 106, 63, 66),
          "D": (170, 106, 63, 66),
          "F": (233, 106, 63, 66),
          "G": (296, 106, 63, 66),
          "H": (359, 106, 63, 66),
          "J": (422, 106, 63, 66),
          "K": (485, 106, 63, 66),
          "L": (548, 106, 63, 66),
          "Z": (92, 172, 63, 66),
          "X": (155, 172, 63, 66),
          "C": (218, 172, 63, 66),
          "V": (281, 172, 63, 66),
          "B": (344, 172, 63, 66),
          "N": (407, 172, 63, 66),
          "M": (470, 172, 63, 66),
          "ERASE": (63, 243, 186, 68),
          "DONE": (390, 244, 186, 68),
        }
        
    def on_init(self, controller):
        print "Leap Initialized"

    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);

        print "Leap Finger Connected"

    def on_disconnect(self, controller):
        print "Leap Finger Disconnected"

    def on_exit(self, controller):
        print "Leap Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        pos   = frame.hands[0].fingers[3].stabilized_tip_position

        self.x   = (s.DIMENSIONS[0] / 2) + int(pos[0] * 2.2)
        self.y   = s.DIMENSIONS[1] - int(pos[1] * 2.5)
        self.key = self.__map_key()

        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP and self.key:
                key_tap = KeyTapGesture(gesture)

                if len(self.key) == 1:
                    self.chars.append(self.key)
                elif self.key == "ERASE":
                    self.chars.pop()
                elif self.key == "DONE":
                    self.finished = True
                print "".join(self.chars)

    def __map_key(self):
        """Returns the character for the key the user is hovering over, if any."""
        state = None

        for k, pos in self.key_map.iteritems():
            if self.x >= pos[0] and self.x < pos[0] + pos[2] and\
               self.y >= pos[1] and self.y < pos[1] + pos[3]:
                state = k
                break

        return state
