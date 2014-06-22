#!/usr/bin/env python

## Generates a level CSV file and writes it to ./swervin_mervin/levels/.

        y = 0
        last_y = 0
        for n in range(25):
            last_y = y
            y = u.ease_in_out(0, (20 * 260), n / 75.0)
            self.add_segment(0, last_y, y)

        for n in range(25):
            last_y = y
            y = u.ease_in_out(0, (20 * 260), (n + 25) / 75.0)
            self.add_segment(0, last_y, y)

        for n in range(25):
            last_y = y
            y = u.ease_in_out(0, (20 * 260), (n + 50) / 75.0)
            self.add_segment(0, last_y, y)

        end_y = y
        for n in range(25):
            self.add_segment(0, y, y)

        for n in range(25):
            last_y = y
            y = u.ease_in_out(end_y, 0, n / 75.0)
            self.add_segment(0, last_y, y)

        for n in range(25):
            last_y = y
            y = u.ease_in_out(end_y, 0, (n + 25) / 75.0)
            self.add_segment(0, last_y, y)

        for n in range(25):
            last_y = y
            y = u.ease_in_out(end_y, 0, (n + 50) / 75.0)
            self.add_segment(0, last_y, y)

        self.add_corner(50, 25, 100, 4)
        self.add_corner(50, 25, 100, -6)

        for n in range(100):
            sprites = []

            if (n % 10 == 0):
                sprites.append({"sprite": s.SPRITES["column"], "offset": -1.1})
                sprites.append({"sprite": s.SPRITES["column"], "offset": 1.4})

            self.add_segment(0, 0, 0, sprites)

    def add_corner(self, enter, hold, exit, curve):
        """Writes a curve (with easing) into the segments array"""
        # Ease into corner.
        for n in range(enter):
            self.add_segment(u.ease_in(0, curve, n / enter))

        # Hold.
        for n in range(hold):
            self.add_segment(curve)

        # Ease out of corner.
        for n in range(exit):
            self.add_segment(u.ease_in_out(curve, 0, n / exit))


