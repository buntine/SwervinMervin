![Swervin' Mervin](/lib/box.png?raw=true "Swervin' Mervin")

Swervin Mervin: A recreation of 80's-style pseudo-3D arcade racing games, written in Python and Pygame.

Accelleration and steering is performed via the arrow keys.

Here is a [small video of me playing](https://www.youtube.com/watch?v=T08Oe1l7nhk) (poorly).

Note, this project is purely an exercise in enjoyment and my first foray into Pygame. Any pointers are welcome!

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
  * [SoundBible](http://soundbible.com) and [FreeSFX](http://freesfx.co.uk) for some sound bites.

### TODO
  
  * Animate highscores in, fade them out on new game
  * User notification of + or - to score during gameplay
  * User notification of high score either during or directly after game
  * Random time extensions dropped onto road
  * Pedestrians that penalise points when hit
  * Allow for multiple levels (easy, regular, hard)
  * Refine collision offsets for sprites
  * Car sound effects
  * Smoke when player accelerating from 0
  * Position (number of `laps + base_segment.index`)
  * Package better for distribution (ship with Pygame?)
  * General refactor and Pythonify of sloppy code
