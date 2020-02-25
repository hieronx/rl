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
        alpha = -math.inf
        beta = math.inf
        opposite_color = board.get_opposite_color(color)
        
        move, _, = self.alpha_beta_search(board, self.search_depth, color, opposite_color, alpha, beta, True)
        
        if self.live_play:
            cls()
            print("Searched %d nodes and experienced %d cutoffs." % (nodes_searched, cutoffs))

            elapsed_time = time.time() - start_time
            print("Generation of this next move took %f seconds." % elapsed_time)
        return move

    def alpha_beta_search(self, board, depth, color, opposite_color, alpha, beta, maximizing):
        # hash_code = board.hash_code(perspective_player)
        # if hash_code in self.tp_table:
        #     return (self.tp_table[hash_code][0], self.tp_table[hash_code][1], 0, 0)
        
        if depth == 0 or board.game_over:
            score = self.evaluate.evaluate_board(board, color)
            return (None, score)

        moves = self.get_possible_moves(board)
        assert len(moves) > 0

        if maximizing:
            best_score = -math.inf
            best_move = None

            for move in moves:
                new_board = board.make_move(move, color)
                _, score = self.alpha_beta_search(new_board, depth - 1, color, opposite_color, lower_bound_a, upper_bound_b, False)

                if score > best_score:
                    best_score = score
                    best_move = move

            return (best_move, best_score)
            
        else:
            best_score = math.inf
            best_move = None

            for move in moves:
                new_board = board.make_move(move, opposite_color)
                _, score = self.alpha_beta_search(new_board, depth - 1, color, opposite_color, lower_bound_a, upper_bound_b, True)

                if score < best_score:
                    
                    best_score = score
                    best_move = move
                    
            return (best_move, best_score)

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
