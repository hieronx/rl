import math
import numpy as np

from util import cls
from hexboard import HexBoard

import time

char_to_row_idx = {'a': 0, 'b': 1, 'c': 2, 'd': 3}

class Minimax:

    def __init__(self, size, depth, evaluate_class, live_play = True):
        self.board_size = size
        self.search_depth = depth
        self.evaluate = evaluate_class
        self.live_play = live_play
        self.tp_table = {}

    def get_next_move(self, board, color):
        start_time = time.time()
        lower_bound_a = -math.inf
        upper_bound_b = math.inf
        
        move, _, nodes_searched, cutoffs = self.alpha_beta_search(board, self.search_depth, color, lower_bound_a, upper_bound_b, False)

        if self.live_play:
            cls()
            print("Searched %d nodes and experienced %d cutoffs." % (nodes_searched, cutoffs))

            elapsed_time = time.time() - start_time
            print("Generation of this next move took %f seconds." % elapsed_time)
        return move

    def alpha_beta_search(self, board, depth, color, lower_bound_a, upper_bound_b, maximizing):
        # hash_code = board.hash_code(perspective_player)
        # if hash_code in self.tp_table:
        #     return (self.tp_table[hash_code][0], self.tp_table[hash_code][1], 0, 0)
        
        if depth == 0 or board.game_over:
            score = self.evaluate.evaluate_board(board, color)
            return (None, score, 1, 0)

        moves = self.get_possible_moves(board)
        assert len(moves) > 0

        best_score = -math.inf if maximizing else math.inf
        best_move = None
        perspective_player = color if not maximizing else board.get_opposite_color(color)

        total_nodes_searched = 0
        total_cutoffs = 0

        for move in moves:
            new_board = board.make_move(move, perspective_player)
            _, score, nodes_searched, cutoffs = self.alpha_beta_search(new_board, depth - 1, color, lower_bound_a, upper_bound_b, not maximizing)

            total_nodes_searched += nodes_searched
            total_cutoffs += cutoffs

            if maximizing and score > best_score:
                best_move = move
                best_score = score
                
                # if score >= lower_bound_a:
                #     lower_bound_a = score

                #     if lower_bound_a >= upper_bound_b:
                #         # self.put_in_tp_table(board, perspective_player, best_move, best_score)
                #         return (best_move, best_score, total_nodes_searched, 1)

            elif not maximizing and score < best_score:
                best_move = move
                best_score = score

                # if score <= upper_bound_b:
                #     upper_bound_b = score
                    
                #     if upper_bound_b <= lower_bound_a:
                #         # self.put_in_tp_table(board, current_color, best_move, best_score)
                #         return (best_move, best_score, total_nodes_searched, 1)
        
        # self.put_in_tp_table(board, current_color, best_move, best_score)

        assert best_move is not None

        return (best_move, best_score, total_nodes_searched, total_cutoffs)

    def get_possible_moves(self, board):
        empty_coordinates = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board.is_empty((x, y)):
                    empty_coordinates.append((x, y))
        
        return empty_coordinates

    def put_in_tp_table(self, board, color, move, score):
        best_move_board = board.make_move(move, color)
        hash_code = best_move_board.hash_code(color)
        if hash_code not in self.tp_table or (hash_code in self.tp_table and self.tp_table[hash_code][1] > score):
            self.tp_table[hash_code] = (move, score)
