# Helper functions for rendering.

def segment_pointlist(segment):
    top    = segment["top"]["screen"]
    bottom = segment["bottom"]["screen"]

    return [((bottom["x"] - bottom["w"]), bottom["y"]),
            ((bottom["x"] + bottom["w"]), bottom["y"]),
            ((top["x"] + top["w"]), top["y"]),
            ((top["x"] - top["w"]), top["y"])]

def render_player():
    pass
