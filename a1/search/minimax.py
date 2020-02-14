import math
import numpy as np

from util import cls
from hexboard import HexBoard

char_to_row_idx = {'a': 0, 'b': 1, 'c': 2, 'd': 3}

class Minimax:

    def __init__(self, size, depth, evaluate_class):
        self.board_size = size
        self.search_depth = depth
        self.evaluate = evaluate_class

    def alpha_beta_search(self, board, depth, color, lower_bound_a, upper_bound_b, maximizing = True):
        if depth == 0:
            return (None, self.evaluate.evaluate_board(board, color), 1, 0)

        moves = self.get_possible_moves(board)

        best_score = math.inf if not maximizing else -math.inf
        best_move = None

        total_nodes_searched = 0
        total_cutoffs = 0

        for move in moves:
            new_board = board.make_move(move, color)
            _, score, nodes_searched, cutoffs = self.alpha_beta_search(new_board, depth - 1, board.get_opposite_color(color), lower_bound_a, upper_bound_b, not maximizing)
            total_nodes_searched += nodes_searched
            total_cutoffs += cutoffs

            if maximizing and score > best_score:
                best_move = move
                best_score = score
                
                if score >= lower_bound_a:
                    lower_bound_a = score

                    if lower_bound_a >= upper_bound_b:
                        return (best_move, best_score, total_nodes_searched, 1)

            elif not maximizing and score < best_score:
                best_move = move
                best_score = score

                if score <= upper_bound_b:
                    upper_bound_b = score
                    
                    if upper_bound_b <= lower_bound_a:
                        return (best_move, best_score, total_nodes_searched, 1)

        return (best_move, best_score, total_nodes_searched, total_cutoffs)

    def get_next_move(self, board, depth, color):
        lower_bound_a = -math.inf
        upper_bound_b = math.inf
        
        move, _, nodes_searched, cutoffs = self.alpha_beta_search(board, depth, color, lower_bound_a, upper_bound_b, True)
        cls()
        print("Searched %d nodes and experienced %d cutoffs" % (nodes_searched, cutoffs))
        return move

    def get_possible_moves(self, board):
        empty_coordinates = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board.is_empty((x, y)):
                    empty_coordinates.append((x, y))

        return empty_coordinates