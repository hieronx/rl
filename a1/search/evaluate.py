import math
import numpy as np

from util import cls
from hexboard import HexBoard
from minimax import Minimax

class Evaluate:

    def __init__(self, eval_method):
        self.eval_method = eval_method

    def find_shortest_path_to_border(self, board, color):
        source_coords = board.get_source_coordinates(color)
        target_coords = board.get_target_coordinates(color)
        
        min_score = math.inf
        for from_coord in source_coords:
            # Only count nodes without placed positions of this color
            score = np.random.uniform(0, 10) # TODO: replace this

            if score < min_score:
                min_score = score

        return min_score

    def evaluate_board(self, board, color):
        if self.eval_method == 'Dijkstra':
            player_sp = self.find_shortest_path_to_border(board, color)
            opponent_sp = self.find_shortest_path_to_border(board, board.get_opposite_color(color))

            return player_sp - opponent_sp
        else:
            return np.random.uniform(0, 1)