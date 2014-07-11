# SWERVIN' MERVIN

![Swervin' Mervin](/lib/box.png?raw=true "Swervin' Mervin")

A recreation of 80's-style pseudo-3D arcade racing games, written in Python and Pygame.

Accelleration and steering can be performed by integrating with a LEAP Motion Controller (if you have one), otherwise just use the arrow keys.

### Playing

```
  $ python swervin_mervin/main.py 
```

### Credits

  * Jake at codeincomplete.com and Lou at extentofthejam.com for their fantastic articles on the subject.
  * My beautiful girlfriend, Mel, for all of the original pixel art.
  * LazerHawk and Miami Nights 1984 for the music.

### TODO
  
  * Accumulating point system
  * Leaderboard
  * Refine LEAP integration
  * Refine collision offsets for sprites
  * Car sound effects
  * Competitors jumpy when close to player
  * Should `render_competitors` actually be in `Competitor` class?
  * Use class for sprites instead of dict (and refactor `render_sprites` / `render_competitors`)
  * Position (number of `laps + base_segment.index`)
  * Building sprites
  * Package better for distribution
  * General refactor and Pythonify of sloppy code
