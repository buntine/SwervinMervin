# Swervin Mervin: A recreation of 80's pseudo-3D arcade racing games

![Swervin' Mervin](/lib/box.png?raw=true "Swervin' Mervin")
![Gameplay A](/lib/gameplay_a.gif)
![Gameplay B](/lib/gameplay_b.gif)

Written in Python over the course of way too much time.

Here is a [small video of me playing](https://www.youtube.com/watch?v=isLmdHhFFgQ&feature=youtu.be) (poorly).

And here is my bosses son, Jesse, [playing the arcade version](https://www.youtube.com/watch?v=uZsDYY9bZ7A). Sorry for the portrait mode.

More info on the pixel art is available over at my girlfriends website: [MelanieHuang.com](http://melaniehuang.com/projects/swervinmervin.html).

### The Arcade Edition

![Swervin' Mervin Arcade Edition](/lib/arcade.jpg?raw=true "Swervin' Mervin Arcade Edition")

Yes, it's real. Ships with MAME, SNES and NES (1000+ games). Want something similar for the office? Email me.

### Playing

Ensure that you have [Python 2.x](https://www.python.org/) and [Pygame](http://www.pygame.org/download.shtml) installed, and then:

```
  $ ./play
```

Accelleration and steering is performed via the arrow keys. [ENTER] to start, [ESC] to kill the game in fullscreen mode.

Many in-game settings can be changed in `./swervin_mervin/settings.py` but I'll also load in settings that are defined in `./swervin_mervin/settings_local.py` (which is gitignored).

### What people are saying

> "It's no Sonic the Hedgehog"

And...

> "You actually get points for killing people? I don't remember that bit in the originals..."

And even...

> "I've taken dumps that were more fun than this steaming assheap..."

### Credits

  * [Jake at codeincomplete.com](http://codeincomplete.com/) and [Lou at extentofthejam.com](http://extentofthejam.com/) for their fantastic articles on pseudo-3d racing games.
  * My beautiful girlfriend, [Mel](http://melaniehuang.com), for all of the original pixel art. 
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
    * Use current actual FPS to determine time left.
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
