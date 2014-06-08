# Helper functions for rendering.

def segment_pointlist(segment):
    bottom = segment["bottom"]["screen"]
    top    = segment["top"]["screen"]

    return [((bottom["x"] - bottom["w"]), bottom["y"]),
            ((bottom["x"] + bottom["w"]), bottom["y"]),
            ((top["x"] + top["w"]), top["y"]),
            ((top["x"] - top["w"]), top["y"])]

def render_player():
    pass
