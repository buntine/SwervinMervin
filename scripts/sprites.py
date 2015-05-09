# Prints
#  - n sprites
#  - random type over names
#  - random step intervals over low and high
#  - random X position over low and high
#
# sprites(100, 1000, ["bush1", "boulder1"], [5, 12], [2.5, 4.8], 0.0)

import random

def sprites(amount, start, names, steps, pos, y):
    z = start

    for n in range(amount - 1):
        stype = random.choice(names)
        spos = random.uniform(*pos)
        z += random.randint(*steps)

        print "%d,%s,%.2f,%.1f" % (z, stype, spos, y)
