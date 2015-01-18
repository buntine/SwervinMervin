import json, os
import datetime as dt

class HighScores():
    """Wrapper over the high scores file."""

    def __init__(self):
        self.high_scores = self.__read_high_scores()
        self.__sort()

    def is_high_score(self, score):
        scores = self.__scores_only()

        return any(map(lambda n: score > n, scores))

    def minimum_score(self):
        """returns the minimum score required to be on the high score list."""
        scores = self.__scores_only()

        return scores[-1]

    def add_high_score(self, score):
        """Adds given score to high scores, knocking off lowest score."""
        today = dt.date.today()

        self.high_scores.append([today, score])
        self.__sort()
        self.high_scores.pop()

        self.__write_high_scores()

    def __sort(self):
        self.high_scores.sort(key=lambda hs: hs[1])
        self.high_scores.reverse()

    def __write_high_scores(self):
        hs    = open(os.path.join("dat", "highscores"), "w")
        jdata = map(lambda hs: [hs[0].strftime("%Y-%m-%d"), hs[1]], self.high_scores)

        json.dump(jdata, hs)
        hs.close()

    def __read_high_scores(self):
        hs  = open(os.path.join("dat", "highscores"), "r")
        jhs = map(lambda hs: [dt.datetime.strptime(hs[0], "%Y-%m-%d"), hs[1]], json.load(hs))

        hs.close()

        return jhs

    def __scores_only(self):
        return map(lambda hs: hs[1], self.high_scores)
