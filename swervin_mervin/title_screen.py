class TitleScreen():
    """Plays a title screen and waits for user to insert coin."""

    def __init__(self, window):
        self.finished = False
        self.ready    = False
        self.window   = window
        self.frame    = 0

    def progress(self):
        self.ready = True
