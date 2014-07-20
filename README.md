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
  * Out Run (1986) for letting me steal some sprites.
  * Jim Gillette and Cary-Hiroyuki Tagawa for the sound bites.

### TODO
  
  * Randomly placed "things" on road that give additional points
  * Pedestrians that penalise points when hit
  * Refine collision offsets for sprites
  * Car sound effects
  * Countdown at start of game
  * Smoke when playing accelerating from 0
  * Competitors jumpy when close to player
  * Position (number of `laps + base_segment.index`)
  * Building sprites
  * Package better for distribution (ship with Pygame?)
  * General refactor and Pythonify of sloppy code
