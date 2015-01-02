import json, os
from datetime import date

class HighScores():
    """Wrapper over the high scores file."""

    def __init__(self):
        self.high_scores = self.__read_high_scores()

    def is_high_score(self, score):
        scores = self.__scores_only()

        return any(map(lambda n: score > n, scores))

    def add_high_score(self, score):
        """Adds given score to high scores, knocking off lowest score."""
        today = date.today().strftime("%Y-%m-%d")

        self.high_scores.append([today, score])
        self.high_scores.sort(key=lambda hs: hs[1])
        self.high_scores.pop()

    def __write_high_scores(self):
        hs = open(os.path.join("dat", "highscores"), "w")

        json.dump(self.high_scores, hs)
        hs.close()

    def __read_high_scores(self):
        hs  = open(os.path.join("dat", "highscores"), "r")
        jhs = json.load(hs)

        hs.close()

        return jhs

    def __scores_only(self):
        return map(lambda hs: hs[1], self.high_scores)
