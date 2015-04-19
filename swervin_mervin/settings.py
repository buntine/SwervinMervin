from pygame import Color
import math, os

FPS                   = 60
TITLE_FPS             = 20
COUNTDOWN_FPS         = 1
PLAYER_SELECT_FPS     = 10
GAME_OVER_LAG         = 5 * FPS
TITLE_SCREEN          = True
COUNTDOWN             = True
PLAYER_SELECT         = True
FULLSCREEN            = True
FRAME_RATE            = (1.0 / FPS)
DIMENSIONS            = (640, 480)
MUSIC_VOLUME          = 0.7
SEGMENT_HEIGHT        = 260
RUMBLE_LENGTH         = 3
DRAW_DISTANCE         = 140
SPRITE_DRAW_DISTANCE  = 110
ROAD_WIDTH            = 2100
LANES                 = 4
BOUNDS                = 2.1
TUNNEL_BOUNDS         = 0.85
TUNNEL_HEIGHT         = 20
AUTO_DRIVE            = False
PLAYER_ANIM_HOLD      = 8
CHECKPOINT            = 47
LAP_DIFFICULTY_FACTOR = 3
LAPS_PER_LEVEL        = 2
MINIMUM_DIFFICULTY    = 3
MINIMUM_ENGINE_DIST   = 4000
CRASH_DIVISOR         = 2
POINTS                = 15
CHANCE_OF_BONUSES     = 3
BONUS_AMOUNT          = 3
POINT_GAIN_PROSTITUTE = 500
POINT_LOSS_SPRITE     = 0.03
POINT_LOSS_COMP       = 0.02
POINT_MILESTONE       = 20000
MINIMUM_CORNER_SMOKE  = 3
FIELD_OF_VIEW         = 100 # Degrees
CAMERA_HEIGHT         = 1300
CAMERA_DEPTH          = 1 / math.tan((FIELD_OF_VIEW / 2) * math.pi / 180)
BOTTOM_OFFSET         = 5
SPEED_BOOST_DECREASE  = 0.004
HARD_TOP_SPEED        = [(SEGMENT_HEIGHT / (1.0/FPS)) * 1.5, (SEGMENT_HEIGHT / (1.0/FPS)) * 2.4]
HARD_HANDLING         = [0.1, 0.45]
HARD_ACCELERATION     = [2.0, 7.0]
PLAYER_Z              = (CAMERA_HEIGHT * CAMERA_DEPTH)
FONTS                 = {"retro_computer": os.path.join("lib", "PressStart2P.ttf"),
                         "fipps": os.path.join("lib", "Fipps-Regular.otf")}
COLOURS               = {"white": Color(255, 255, 255),
                         "opaque_white": Color(255, 255, 255, 80),
                         "text": Color(172, 199, 252),
                         "selection": [Color(172, 199, 252),Color(100, 149, 252)],
                         "sky": Color(10, 10, 10),
                         "gutter": Color(100, 100, 100),
                         "red": Color(204, 0, 0),
                         "bonus_a": Color(255, 78, 0),
                         "bonus_b": Color(255, 178, 0),
                         "green": Color(0, 204, 0),
                         "black": Color(0, 0, 0),
                         "tunnel": Color(0, 30, 70),
                         "light": {"road":     Color(34, 54, 56),
                                   "grass":    Color(0, 30, 70),
                                   "footpath": Color(82, 96, 115),
                                   "line":     Color(185, 185, 185)},
                         "dark":  {"road":     Color(48, 64, 81),
                                   "grass":    Color(0, 16, 56),
                                   "footpath": Color(68, 84, 101),
                                   "line":     Color(185, 185, 185)}}
LEVELS             = [{"id": "melbourne",
                       "name": "Melbourne, VIC",
                       "song": "lazerhawk-overdrive.ogg",
                       "laps": LAPS_PER_LEVEL,
                       "backgrounds": [
                         {"id": "sky",
                          "speed": 2,
                          "convert": True},
                         {"id": "city",
                          "speed": 1,
                          "convert": False}
                       ]},
                      {"id": "goldcoast",
                       "name": "Gold Coast",
                       "song": "timecop1983-summerheat.ogg",
                       "laps": LAPS_PER_LEVEL,
                       "backgrounds": [
                         {"id": "sky",
                          "speed": 2,
                          "convert": True},
                         {"id": "city",
                          "speed": 1,
                          "convert": False}
                       ]},
                      {"id": "nullarbor",
                       "name": "Nullarbor Desert",
                       "song": "alvernagunn-maddog.ogg",
                       "laps": LAPS_PER_LEVEL,
                       "backgrounds": [
                         {"id": "sky",
                          "speed": 2,
                          "convert": True},
                         {"id": "city",
                          "speed": 1,
                          "convert": False}
                       ]}
                     ]
PLAYERS            = [{"name": "Swervin' Mervin",
                       "age": 48,
                       "top_speed": (SEGMENT_HEIGHT / (1.0/FPS)) * 1.9,
                       "offroad_top_speed_factor": 2.0,
                       "acceleration_factor": 4.6,
                       "deceleration": 2.3,
                       "centrifugal_force": 0.261,
                       "city": "Melbourne",
                       "select_sfx": "swervin_mervin_select.ogg",
                       "sprites":
                         {"mugshot_small": {
                           "path": "swervin_mervin_small.png",
                           "width": 60,
                           "height": 60},
                          "mugshot_large": {
                           "path": "swervin_mervin_large.png",
                           "width": 320,
                           "height": 400},
                          "straight1": {
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
                          "left_smoke1": {
                           "path": "left_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "left_smoke2": {
                           "path": "left_smoke2.png",
                           "width": 100,
                           "height": 56},
                          "right_smoke1": {
                           "path": "right_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "right_smoke2": {
                           "path": "right_smoke2.png",
                           "width": 100,
                           "height": 56},
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
                          "uphill_left_smoke1": {
                           "path": "uphill_left_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "uphill_left_smoke2": {
                           "path": "uphill_left_smoke2.png",
                           "width": 100,
                           "height": 56},
                          "uphill_right_smoke1": {
                           "path": "uphill_right_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "uphill_right_smoke2": {
                           "path": "uphill_right_smoke2.png",
                           "width": 100,
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
                          "downhill_left_smoke1": {
                           "path": "downhill_left_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "downhill_left_smoke2": {
                           "path": "downhill_left_smoke2.png",
                           "width": 100,
                           "height": 56},
                          "downhill_right_smoke1": {
                           "path": "downhill_right_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "downhill_right_smoke2": {
                           "path": "downhill_right_smoke2.png",
                           "width": 100,
                           "height": 56}}},
                       {"name": "Candy",
                        "age": 21,
                        "top_speed": (SEGMENT_HEIGHT / (1.0/FPS)) * 2.2,
                        "offroad_top_speed_factor": 1.8,
                        "acceleration_factor": 5.2,
                        "deceleration": 2.5,
                        "centrifugal_force": 0.366,
                        "city": "Surfers Paradise, QLD",
                        "select_sfx": "candy_select.ogg",
                        "sprites":
                         {"mugshot_small": {
                           "path": "candy_small.png",
                           "width": 60,
                           "height": 60},
                          "mugshot_large": {
                           "path": "candy_large.png",
                           "width": 320,
                           "height": 400},
                          "straight1": {
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
                          "left_smoke1": {
                           "path": "left_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "left_smoke2": {
                           "path": "left_smoke2.png",
                           "width": 100,
                           "height": 56},
                          "right_smoke1": {
                           "path": "right_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "right_smoke2": {
                           "path": "right_smoke2.png",
                           "width": 100,
                           "height": 56},
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
                          "uphill_left_smoke1": {
                           "path": "uphill_left_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "uphill_left_smoke2": {
                           "path": "uphill_left_smoke2.png",
                           "width": 100,
                                "height": 56},
                          "uphill_right_smoke1": {
                           "path": "uphill_right_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "uphill_right_smoke2": {
                           "path": "uphill_right_smoke2.png",
                           "width": 100,
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
                          "downhill_left_smoke1": {
                           "path": "downhill_left_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "downhill_left_smoke2": {
                           "path": "downhill_left_smoke2.png",
                           "width": 100,
                           "height": 56},
                          "downhill_right_smoke1": {
                           "path": "downhill_right_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "downhill_right_smoke2": {
                           "path": "downhill_right_smoke2.png",
                           "width": 100,
                           "height": 56}}},
                       {"name": "Burl",
                        "age": 37,
                        "top_speed": (SEGMENT_HEIGHT / (1.0/FPS)) * 1.73,
                        "offroad_top_speed_factor": 1.75,
                        "acceleration_factor": 3.8,
                        "deceleration": 2.2,
                        "centrifugal_force": 0.188,
                        "city": "Nullarbor Roadhouse, SA",
                        "select_sfx": "burl_select.ogg",
                        "sprites":
                         {"mugshot_small": {
                           "path": "burl_small.png",
                           "width": 60,
                           "height": 60},
                          "mugshot_large": {
                           "path": "burl_large.png",
                           "width": 320,
                           "height": 400},
                          "straight1": {
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
                          "left_smoke1": {
                           "path": "left_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "left_smoke2": {
                           "path": "left_smoke2.png",
                           "width": 100,
                           "height": 56},
                          "right_smoke1": {
                           "path": "right_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "right_smoke2": {
                           "path": "right_smoke2.png",
                           "width": 100,
                           "height": 56},
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
                          "uphill_left_smoke1": {
                           "path": "uphill_left_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "uphill_left_smoke2": {
                           "path": "uphill_left_smoke2.png",
                           "width": 100,
                                "height": 56},
                          "uphill_right_smoke1": {
                           "path": "uphill_right_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "uphill_right_smoke2": {
                           "path": "uphill_right_smoke2.png",
                           "width": 100,
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
                          "downhill_left_smoke1": {
                           "path": "downhill_left_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "downhill_left_smoke2": {
                           "path": "downhill_left_smoke2.png",
                           "width": 100,
                           "height": 56},
                          "downhill_right_smoke1": {
                           "path": "downhill_right_smoke1.png",
                           "width": 100,
                           "height": 56},
                          "downhill_right_smoke2": {
                           "path": "downhill_right_smoke2.png",
                           "width": 100,
                           "height": 56}}}]

SPRITES           = {"column": {
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
                       "path": "toll_point.png",
                       "width": 240,
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
                     "speed_boost": {
                       "path": "speed_boost.png",
                       "collision": [-1.1, 0.7],
                       "speed_boost": True,
                       "width": 42,
                       "height": 42},
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

if os.path.isfile("swervin_mervin/settings_local.py"):
    execfile("swervin_mervin/settings_local.py")
