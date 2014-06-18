# Game constants.

from pygame import Color
import math

FPS               = 60
FRAME_RATE        = (1.0 / FPS)
DIMENSIONS        = (640, 480)
SEGMENT_HEIGHT    = 260
RUMBLE_LENGTH     = 3
DRAW_DISTANCE     = 200
ROAD_WIDTH        = 2100
LANES             = 4
BOUNDS            = 1.8
CENTRIFUGAL_FORCE = 0.266
TOP_SPEED         = (SEGMENT_HEIGHT / (1.0/FPS)) * 1.6
OFFROAD_TOP_SPEED = TOP_SPEED / 2.0
ACCELERATION      = TOP_SPEED / 5.0
DECELERATION      = 2.3
FIELD_OF_VIEW     = 100 # Degrees
CAMERA_HEIGHT     = 1400
CAMERA_DEPTH      = 1 / math.tan((FIELD_OF_VIEW / 2) * math.pi / 180);
PLAYER_Z          = (CAMERA_HEIGHT * CAMERA_DEPTH)
COLOURS           = {"white": Color(255, 255, 255),
                     "sky":   Color(142, 169, 232),
                     "light": {"road":   Color(193, 193, 193),
                               "grass":  Color(61, 212, 76),
                               "rumble": Color(223, 215, 1),
                               "line":   Color(255, 255, 255)},
                     "dark":  {"road":   Color(188, 188, 188),
                               "grass":  Color(55, 199, 66),
                               "rumble": Color(192, 186, 0),
                               "line":   Color(255, 255, 255)}}
