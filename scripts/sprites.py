# Prints
#  - n sprites of a given type
#  - random step intervals over low and high
#  - randomized X position over low and high
#
# sprites("bush1", 100, 1000, 5, 12, 2.5, 4.8, 0.0)

import random

def sprites(name, amount, start, lstep, hstep, lpos, hpos, y):
    z = start

    for n in range(amount - 1):
        pos = random.uniform(lpos, hpos)
        z += random.randint(lstep, hstep)

        print "%d,%s,%.2f,%.1f" % (z, name, pos, y)
