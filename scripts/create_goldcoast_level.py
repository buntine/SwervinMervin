#!/usr/bin/env python

import level as l

segments = []
sprites  = []
name     = "goldcoast"

segments += l.add_straight(100, 0)
segments += l.add_hill(50, 50, 50, 40, l.last_y(segments))
segments += l.add_straight(500, l.last_y(segments))
segments += l.add_hill(30, 30, 30, 20, l.last_y(segments))
segments += l.add_straight(200, l.last_y(segments))
segments += l.add_corner(30, 45, 40, 7, l.last_y(segments))
segments += l.add_straight(90, 0)
segments += l.add_hill(30, 30, 30, 0, l.last_y(segments))
segments += l.add_straight(150, 0)

l.write("swervin_mervin/levels/tracks/{0}.csv".format(name), segments)
