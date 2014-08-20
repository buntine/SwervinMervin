![Swervin' Mervin](/lib/box.png?raw=true "Swervin' Mervin")

Swervin Mervin: A recreation of 80's-style pseudo-3D arcade racing games, written in Python and Pygame.

Accelleration and steering is performed via the arrow keys.

Here is a [small video of me playing](https://www.youtube.com/watch?v=T08Oe1l7nhk) (poorly).

Note, this project is purely an exercise in enjoyment. Don't expect to find a lot of beautiful code within these walls!

### Playing

Ensure that you have the pygame llibraries installed, and then:

```
  $ python swervin_mervin/main.py 
```

### Credits

  * [Jake at codeincomplete.com](http://codeincomplete.com/) and [Lou at extentofthejam.com](http://extentofthejam.com/) for their fantastic articles on the subject.
  * My beautiful girlfriend, Mel, for all of the original pixel art.
  * LazerHawk and Miami Nights 1984 for the music.
  * Out Run (1986) for "letting me" use some sprites.
  * Jim Gillette and Cary-Hiroyuki Tagawa for the sound bites.

### TODO
  
  * Accumulating point system
    * Level system that lowers amount of time given for checkpoint
    * Randomly placed "things" on road that give additional points
    * Pedestrians that penalise points when hit
  * Leaderboard
  * Refine LEAP integration
  * Refine collision offsets for sprites
  * Car sound effects
  * Countdown at start of game
  * Smoke when playing accelerating from 0
  * Competitors jumpy when close to player
  * Position (number of `laps + base_segment.index`)
  * Building sprites
  * Package better for distribution (ship with Pygame?)
  * General refactor and Pythonify of sloppy code
