import os
import statistics
from collections import deque


class Stats:
    """This class holds some simple utility methods for generating averages and summaries of game performance"""

    def __init__(self):
        """Creates a simple statistics object that keeps track of the running average and total of game scores"""
        self.current_game_score = 0
        self.running_game_scores = deque([], maxlen=int(100))
        self.total_game_score = 0
        self.num_games_played = 0
        self.lives = 5
        self.max_game_score = 0

        self.save_stats(('game_id', 'score', 'max_game_score', 'avg_game_score'), clear=True)

    def finished_game(self):
        """Finishes a game, updating statistics and resetting current game score"""
        if self.current_game_score > self.max_game_score:
            self.max_game_score = self.current_game_score

        self.save_stats((self.num_games_played, self.current_game_score, self.max_game_score, statistics.mean(self.running_game_scores) if len(self.running_game_scores) > 0 else 0.0))

        self.num_games_played += 1
        self.running_game_scores.append(self.current_game_score)
        self.total_game_score += self.current_game_score
        self.print_summary()
        self.current_game_score = 0
        self.lives = 5

    def print_summary(self):
        """Prints a summary of the statistics obtained during this run so far to the console"""
        summary = (self.num_games_played, self.current_game_score, statistics.mean(self.running_game_scores))
        print('Ended game %d with score %d, running average is %.2f' % summary)

    def save_stats(self, data, clear=False):
        if not os.path.exists('breakout/output'): os.makedirs('breakout/output')

        fn = 'breakout/output/stats.csv'
        if clear and os.path.isfile(fn): os.remove(fn)

        with open(fn, 'a') as fd:
            fd.write(';'.join(map(str, data)) + '\n')
