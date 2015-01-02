import json, os

class HighScores():
    """Wrapper over the high scores file."""

    def __init__(self):
        self.high_scores = self.__read_high_scores()

    def is_high_score(self, score):
        scores = self.__scores_only()

        return any(map(lambda n: score > n, scores))

    def add_high_score(self, score):
        """Adds given score to high scores, knocking off lowest score."""
        pass

    def __write_high_scores(self):
        pass

    def __read_high_scores(self):
        hs  = open(os.path.join("dat", "highscores"), "r")
        jhs = json.load(hs)

        return jhs["scores"]

    def __scores_only(self):
        return map(lambda hs: hs[1], self.high_scores)
