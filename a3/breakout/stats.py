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

    def finished_game(self):
        """Finishes a game, updating statistics and resetting current game score"""
        self.num_games_played += 1
        self.running_game_scores.append(current_game_score)
        self.total_game_score += current_game_score
        self.print_summary()
        self.current_game_score = 0

    def print_summary(self):
        """Prints a summary of the statistics obtained during this run so far to the console"""
        summary = (num_games_played, current_game_score, statistics.mean(running_game_scores))
        print('Ended game %d with score %d, running average is %.2f' % summary)