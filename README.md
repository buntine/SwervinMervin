![Swervin' Mervin](/lib/box.png?raw=true "Swervin' Mervin")

Swervin Mervin: A recreation of 80's-style pseudo-3D arcade racing games, written in Python and Pygame.

Accelleration and steering is performed via the arrow keys. [ENTER] is akin to inserting coins. [ESC] to kill the game in fullscreen mode.

Here is a [small video of me playing](https://www.youtube.com/watch?v=T08Oe1l7nhk) (poorly).

### Playing

Ensure that you have the pygame libraries installed, and then:

```
  $ python swervin_mervin/main.py 
```

### Credits

  * [Jake at codeincomplete.com](http://codeincomplete.com/) and [Lou at extentofthejam.com](http://extentofthejam.com/) for their fantastic articles on the subject.
  * My beautiful girlfriend, Mel, for all of the original pixel art.
  * LazerHawk, Miami Nights 1984, Timecop 1983 and Alverna Gunn for the excellent music.
  * Out Run (1986) for "letting me" use some sprites.
  * Jim Gillette, Macho Man Randy Savage and Cary-Hiroyuki Tagawa for the sound bites.
  * [SoundBible](http://soundbible.com) and [FreeSFX](http://freesfx.co.uk) for some sound effects.
  * This project is dedicated to Adam Hillier (RIP), for his love of retro video games, and Zak Harvey (RIP), for his love of reckless driving.

### TODO
  
  * Rethink player checkpoint logic to fix "time left" bug in pause and make countdown easy to disable/enable.
    * Move all time/checkpoint stuff into game (or maybe level?) and out of player.
  * Local highscore file outside of git
  * Don't use sprite for speed up. Render triangles onto road
    * Or just use sprite that can stand upright...
  * Congratulations sequence when level is finished
  * Congratulations sequence when game is finished
  * Engine sounds based on speed
  * Proper tunnels
  * Animate highscores in, fade them out on new game
  * Get Mel to create art for: Bonuses, Tunnel roof, Other players, Other levels
  * Random boxes that penalise time-left when hit
  * Random boxes that give player temporary speed boost
  * Refine collision offsets for sprites
  * Position (number of `laps + base_segment.index`)
  * Package better for distribution (ship with Pygame?)
  * General refactor and Pythonify of sloppy code
