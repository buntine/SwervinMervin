![Swervin' Mervin](/lib/box.png?raw=true "Swervin' Mervin")

Swervin Mervin: A recreation of 80's-style pseudo-3D arcade racing games, written in Python over the course of way too much time.

Accelleration and steering is performed via the arrow keys. [ENTER] to start, [ESC] to kill the game in fullscreen mode.

Here is a [small video of me playing](https://www.youtube.com/watch?v=T08Oe1l7nhk) (poorly).

### The Arcade Edition

![Swervin' Mervin Arcade Edition](/lib/arcade.jpg?raw=true "Swervin' Mervin Arcade Edition")

Yes, it's real. Ships with MAME, SNES and NES (1000+ games). Want something similar for the office? Email me.

### Playing

Ensure that you have the [pygame](http://www.pygame.org/download.shtml) libraries installed, and then:

```
  $ ./play
```

### What people are saying

> "It's no Sonic the Hedgehog"

And...

> "You actually get points for killing people?"

And even...

> "I've taken dumps that were better than this steaming pile of assmilk..."

### Credits

  * [Jake at codeincomplete.com](http://codeincomplete.com/) and [Lou at extentofthejam.com](http://extentofthejam.com/) for their fantastic articles on pseudo-3d racing games.
  * My beautiful girlfriend, [Mel](http://melaniehuang.com), for all of the original pixel art. [See here](http://melaniehuang.com/projects/swervinmervin.html) for more information.
  * [LazerHawk](https://lazerhawk.bandcamp.com/), [Miami Nights 1984](https://soundcloud.com/miami-nights-1984), [Timecop 1983](https://timecop1983.bandcamp.com/) and [Alverna Gunn](http://www.metal-archives.com/bands/Alverna_Gunn/10011) for the excellent music.
  * Out Run (1986) for "letting me" use some sprites.
  * Jim Gillette, Macho Man Randy Savage and Cary-Hiroyuki Tagawa and Myself for the sound bites.
  * [SoundBible](http://soundbible.com) and [FreeSFX](http://freesfx.co.uk) for some sound effects.
  * This project is dedicated to Adam Hillier (RIP), for his love of retro video games, and Zak Harvey (RIP), for his love of reckless driving.

### TODO
  
  * !Design 2nd and 3rd level properly
  * !Congratulations sequence when game is finished
  * !Package better for distribution (ship with Pygame?)
  * Rethink player checkpoint logic to fix "time left" bug in pause and make countdown easy to disable/enable.
    * Move all time/checkpoint stuff into game (or maybe level?) and out of player.
  * Local highscore file outside of git
  * Engine sounds based on speed
  * Screech sound and sprite when hitting tunnel wall
  * Walls
  * Multiple roads with forks
  * Get Mel to create art for: Bonuses, Tunnel roof, Other players, Other levels
  * Random boxes that penalise time-left when hit
  * Random boxes that give player temporary speed boost
  * General refactor and Pythonify of sloppy code
