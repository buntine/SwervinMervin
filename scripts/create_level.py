#!/usr/bin/env python

import level as l

segments = []
sprites  = []
name     = "test"

segments += l.add_straight(50, 0)
segments += l.add_hill(25, 25, 25, 20, 0)
segments += l.add_straight(25, l.last_y(segments))
segments += l.add_hill(25, 25, 25, 0, l.last_y(segments))
segments += l.add_corner(50, 25, 100, 4)
segments += l.add_corner(50, 25, 100, -6)

for n in range(100):
    if (n % 3 == 0):
        sprites.append([len(segments), -1.1, "column"])
        sprites.append([len(segments), 1.4, "column"])

    segments.append([0, 0, 0])

l.write("swervin_mervin/levels/{0}.csv".format(name), segments)
