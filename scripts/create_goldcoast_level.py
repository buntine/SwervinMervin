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
segments += l.add_corner(30, 45, 40, 6, l.last_y(segments)) #1155
segments += l.add_straight(90, l.last_y(segments))
segments += l.add_hill(30, 30, 30, 0, l.last_y(segments)) #1335
segments += l.add_straight(150, l.last_y(segments)) # 1485
print "Segments: %d" % len(segments)
segments += l.add_corner(30, 45, 40, 6, l.last_y(segments))
segments += l.add_straight(200, l.last_y(segments))
segments += l.add_hill(80, 80, 80, 40, l.last_y(segments))
segments += l.add_hill(20, 20, 20, 35, l.last_y(segments))
segments += l.add_straight(50, l.last_y(segments))
segments += l.add_hill(20, 20, 20, 20, l.last_y(segments))
print "Segments: %d" % len(segments)
segments += l.add_corner(30, 45, 40, -6, l.last_y(segments))
segments += l.add_corner(30, 45, 40, 4, l.last_y(segments))
segments += l.add_straight(50, l.last_y(segments))
segments += l.add_hill(20, 20, 20, 40, l.last_y(segments))
segments += l.add_straight(50, l.last_y(segments))
segments += l.add_corner(25, 45, 25, 5, l.last_y(segments), 30)
print "Segments: %d" % len(segments)
segments += l.add_corner(25, 45, 25, -5, l.last_y(segments), 20)
segments += l.add_corner(25, 45, 25, 5, l.last_y(segments), 10)
segments += l.add_corner(25, 45, 25, -5, l.last_y(segments), 0)
segments += l.add_straight(300, l.last_y(segments))
segments += l.add_corner(120, 120, 120, -6, l.last_y(segments), 0)
segments += l.add_straight(200, l.last_y(segments))
print "Segments: %d" % len(segments)
segments += l.add_corner(120, 200, 120, 6, l.last_y(segments), 0)
segments += l.add_straight(300, l.last_y(segments))
print "Segments: %d" % len(segments)

l.write("swervin_mervin/levels/tracks/{0}.csv".format(name), segments)
