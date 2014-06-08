# Helper functions for rendering.

def segment_pointlist(segment):
    top    = segment["top"]["screen"]
    bottom = segment["bottom"]["screen"]

    return [((bottom["x"] - bottom["w"]), (480 - bottom["y"])),
            ((bottom["x"] + bottom["w"]), (480 - bottom["y"])),
            ((top["x"] + top["w"]), (480 - top["y"])),
            ((top["x"] - top["w"]), (480 - top["y"]))]

def render_player():
    pass
