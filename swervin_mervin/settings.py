# Game constants.

from pygame import Color
import math

FPS              = 50
FRAME_RATE       = (1.0 / FPS)
DIMENSIONS       = (640, 480)
SEGMENT_HEIGHT   = 220
RUMBLE_LENGTH    = 3
DRAW_DISTANCE    = 100
ROAD_WIDTH       = 1900
LANES            = 3
BOUNDS           = 1.8
TOP_SPEED        = (SEGMENT_HEIGHT / (1.0/FPS))
ACCELERATION     = TOP_SPEED / 7.0
FIELD_OF_VIEW    = 100 # Degrees
CAMERA_HEIGHT    = 1400
CAMERA_DEPTH     = 1 / math.tan((FIELD_OF_VIEW / 2) * math.pi / 180);
COLOURS          = {"white": Color(255, 255, 255),
                    "sky":   Color(142, 169, 232),
                    "light": {"road":   Color(193, 193, 193),
                              "grass":  Color(61, 212, 76),
                              "rumble": Color(223, 215, 1),
                              "line":   Color(255, 255, 255)},
                    "dark":  {"road":   Color(173, 173, 173),
                              "grass":  Color(50, 186, 62),
                              "rumble": Color(192, 186, 0),
                              "line":   Color(255, 255, 255)}}
