![Swervin' Mervin](/lib/box.png?raw=true "Swervin' Mervin")

Swervin Mervin: A recreation of 80's-style pseudo-3D arcade racing games, written in Python and Pygame.

Accelleration and steering is performed via the arrow keys. Space Bar is akin to inserting coins. [ESC] to kill the game in fullscreen mode.

Here is a [small video of me playing](https://www.youtube.com/watch?v=T08Oe1l7nhk) (poorly).

Note, this project is purely an exercise in enjoyment and my first foray into Pygame. Any pointers are welcome!

### Playing

Ensure that you have the pygame libraries installed, and then:

```
  $ python swervin_mervin/main.py 
```

### Credits

  * [Jake at codeincomplete.com](http://codeincomplete.com/) and [Lou at extentofthejam.com](http://extentofthejam.com/) for their fantastic articles on the subject.
  * My beautiful girlfriend, Mel, for all of the original pixel art.
  * LazerHawk and Miami Nights 1984 for the music.
  * Out Run (1986) for "letting me" use some sprites.
  * Jim Gillette, Macho Man Randy Savage and Cary-Hiroyuki Tagawa for the sound bites.
  * [SoundBible](http://soundbible.com) and [FreeSFX](http://freesfx.co.uk) for some sound effects.
  * This project is dedicated to Adam Hillier (RIP), for his love of retro video games, and Zak Harvey (RIP), for his love of reckless driving.

### TODO
  
  * Pause
  * Local highscore file outside of git
  * More levels. If player gets to lap N, then move onto next level
  * Animate highscores in, fade them out on new game
  * Get Mel to create art for: Bonuses, Tunnel roof, corner smoke
  * Pedestrians that penalise points when hit
  * Refine collision offsets for sprites
  * Car sound effects (when player passes other car, when player is smoking around corner)
  * Position (number of `laps + base_segment.index`)
  * Package better for distribution (ship with Pygame?)
  * General refactor and Pythonify of sloppy code
