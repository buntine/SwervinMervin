

from pygame import Color
import math, os

DEV_MODE              = True
FPS                   = 60
TITLE_FPS             = 20
COUNTDOWN_FPS         = 1
GAME_OVER_LAG         = 5 * FPS
TITLE_SCREEN          = True
COUNTDOWN             = True
FULLSCREEN            = True
FRAME_RATE            = (1.0 / FPS)
DIMENSIONS            = (640, 480)
MUSIC_VOLUME          = 0.7
SEGMENT_HEIGHT        = 260
RUMBLE_LENGTH         = 3
DRAW_DISTANCE         = 160
ROAD_WIDTH            = 2100
LANES                 = 4
BOUNDS                = 2.1
AUTO_DRIVE            = False
CENTRIFUGAL_FORCE     = 0.266
PLAYER_ANIM_HOLD      = 8
CHECKPOINT            = 50
LAP_DIFFICULTY_FACTOR = 3
MINIMUM_DIFFICULTY    = 2
CRASH_DIVISOR         = 2
POINTS                = 15
CHANCE_OF_BONUSES     = 3
BONUS_AMOUNT          = 3
POINT_GAIN_PROSTITUTE = 500
POINT_LOSS_SPRITE     = 0.03
POINT_LOSS_COMP       = 0.02
POINT_MILESTONE       = 20000
TOP_SPEED             = (SEGMENT_HEIGHT / (1.0/FPS)) * 1.9
OFFROAD_TOP_SPEED     = TOP_SPEED / 2.0
ACCELERATION          = TOP_SPEED / 5.0
DECELERATION          = 2.3
FIELD_OF_VIEW         = 100 # Degrees
CAMERA_HEIGHT         = 1400
CAMERA_DEPTH          = 1 / math.tan((FIELD_OF_VIEW / 2) * math.pi / 180);
BOTTOM_OFFSET         = 5
PLAYER_Z              = (CAMERA_HEIGHT * CAMERA_DEPTH)
FONTS                 = {"bladerunner": os.path.join("lib", "br_font.ttf"),
                        "arcade":    os.path.join("lib", "arcade.ttf")}
COLOURS               = {"white":  Color(255, 255, 255),
                        "text":   Color(172, 199, 252),
                        "sky":    Color(10, 10, 10),
                        "gutter": Color(100, 100, 100),
                        "red":    Color(204, 0, 0),
                        "bonus_a": Color(255, 78, 0),
                        "bonus_b": Color(255, 178, 0),
                        "green":  Color(0, 204, 0),
                        "black":  Color(0, 0, 0),
                        "light": {"road":     Color(34, 54, 56),
                                  "grass":    Color(0, 30, 70),
                                  "footpath": Color(82, 96, 115),
                                  "line":     Color(185, 185, 185)},
                        "dark":  {"road":     Color(48, 64, 81),
                                  "grass":    Color(0, 16, 56),
                                  "footpath": Color(68, 84, 101),
                                  "line":     Color(185, 185, 185)}}
SPRITES            = {"straight1": {
                       "path": "straight1.png",
                       "width": 80,
                       "height": 50},
                     "straight2": {
                       "path": "straight2.png",
                       "width": 80,
                       "height": 50},
                     "left1": {
                       "path": "left1.png",
                       "width": 80,
                       "height": 50},
                     "left2": {
                       "path": "left2.png",
                       "width": 80,
                       "height": 50},
                     "right1": {
                       "path": "right1.png",
                       "width": 80,
                       "height": 50},
                     "right2": {
                       "path": "right2.png",
                       "width": 80,
                       "height": 50},
                     "uphill_straight1": {
                       "path": "uphill_straight1.png",
                       "width": 80,
                       "height": 56},
                     "uphill_straight2": {
                       "path": "uphill_straight2.png",
                       "width": 80,
                       "height": 56},
                     "uphill_left1": {
                       "path": "uphill_left1.png",
                       "width": 80,
                       "height": 56},
                     "uphill_left2": {
                       "path": "uphill_left2.png",
                       "width": 80,
                       "height": 56},
                     "uphill_right1": {
                       "path": "uphill_right1.png",
                       "width": 80,
                       "height": 56},
                     "uphill_right2": {
                       "path": "uphill_right2.png",
                       "width": 80,
                       "height": 56},
                     "downhill_straight1": {
                       "path": "downhill_straight1.png",
                       "width": 80,
                       "height": 56},
                     "downhill_straight2": {
                       "path": "downhill_straight2.png",
                       "width": 80,
                       "height": 56},
                     "downhill_left1": {
                       "path": "downhill_left1.png",
                       "width": 80,
                       "height": 56},
                     "downhill_left2": {
                       "path": "downhill_left2.png",
                       "width": 80,
                       "height": 56},
                     "downhill_right1": {
                       "path": "downhill_right1.png",
                       "width": 80,
                       "height": 56},
                     "downhill_right2": {
                       "path": "downhill_right2.png",
                       "width": 80,
                       "height": 56},
                     "column": {
                       "path": "column.png",
                       "collision": [-0.9, 0.1],
                       "width": 80,
                       "height": 126},
                     "tunnel": {
                       "path": "tunnel.png",
                       "width": 480,
                       "height": 40},
                     "boat_house": {
                       "path": "boat_house.png",
                       "collision": [-0.9, 0.1],
                       "width": 119,
                       "height": 86},
                     "bush1": {
                       "path": "bush1.png",
                       "collision": [-0.9, 0.1],
                       "width": 86,
                       "height": 52},
                     "palm_tree": {
                       "path": "palm_tree.png",
                       "collision": [-0.9, 0.1],
                       "width": 86,
                       "height": 216},
                     "tree1": {
                       "path": "tree1.png",
                       "collision": [-0.9, 0.1],
                       "width": 144,
                       "height": 144},
                     "billboard3": {
                       "path": "billboard03.png",
                       "collision": [-0.9, 0.1],
                       "width": 92,
                       "height": 88},
                     "billboard4": {
                       "path": "billboard04.png",
                       "collision": [-0.9, 0.1],
                       "width": 107,
                       "height": 68},
                     "start": {
                       "path": "start.png",
                       "width": 210,
                       "height": 120},
                     "boulder1": {
                       "path": "boulder1.png",
                       "collision": [-0.9, 0.1],
                       "width": 67,
                       "height": 99},
                     "post": {
                       "path": "post.png",
                       "collision": [-0.9, 0.1],
                       "width": 30,
                       "height": 56},
                     "light_post1": {
                       "path": "light_post1.png",
                       "width": 40,
                       "height": 90},
                     "light_post2": {
                       "path": "light_post2.png",
                       "width": 40,
                       "height": 90},
                     "left_sign": {
                       "path": "left_sign.png",
                       "width": 40,
                       "height": 90},
                     "right_sign": {
                       "path": "right_sign.png",
                       "width": 40,
                       "height": 90},
                     "traffic_light": {
                       "path": "traffic_light.png",
                       "width": 40,
                       "height": 90},
                     "competitor1": {
                       "path": "competitor1.png",
                       "width": 80,
                       "height": 50},
                     "competitor2": {
                       "path": "competitor2.png",
                       "width": 80,
                       "height": 50},
                     "competitor3": {
                       "path": "competitor3.png",
                       "width": 80,
                       "height": 50},
                     "bonus": {
                       "path": "bonus.png",
                       "collision": [-0.4, 0.1],
                       "bonus": True,
                       "width": 25,
                       "height": 25},
                     "hooker1": {
                       "path": "hooker1.png",
                       "collision": [-0.4, 0.1],
                       "hooker": True,
                       "width": 25,
                       "height": 42},
                     "hooker2": {
                       "path": "hooker2.png",
                       "collision": [-0.4, 0.1],
                       "hooker": True,
                       "width": 25,
                       "height": 42},
                     "hooker3": {
                       "path": "hooker3.png",
                       "collision": [-0.4, 0.1],
                       "hooker": True,
                       "width": 25,
                       "height": 42}}

if DEV_MODE:
    TITLE_SCREEN    = False
    COUNTDOWN       = False
    FULLSCREEN      = False
    CHECKPOINT      = 55
