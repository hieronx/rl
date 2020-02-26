import math
import numpy as np
import time

from util import cls
from hexboard import HexBoard

class Minimax:

    def __init__(self, size, search_depth, evaluate_class, live_play = True):
        self.board_size = size
        self.depth = search_depth
        self.evaluate = evaluate_class
        self.live_play = live_play
        self.tp_table = {}

    def get_next_move(self, board, color):
        start_time = time.time()
        alpha = -math.inf
        beta = math.inf
        opposite_color = board.get_opposite_color(color)
        
        for i in range(1, 4):
            move, _, nodes_searched, cutoffs = self.alpha_beta_search(board, i, color, opposite_color, alpha, beta, True)
        
        if self.live_play:
            cls()
            print("Searched %d nodes and experienced %d cutoffs." % (nodes_searched, cutoffs))

            elapsed_time = time.time() - start_time
            print("Generation of this next move took %f seconds." % elapsed_time)
        
        return move

    def alpha_beta_search(self, board, depth, color, opposite_color, alpha, beta, maximizing):
        hash_code = board.hash_code(color if maximizing else opposite_color)
        if hash_code in self.tp_table:
            return (self.tp_table[hash_code][0], self.tp_table[hash_code][1], 0, 0)
        
        if depth == 0 or board.game_over():
            score = self.evaluate.evaluate_board(board, color)
            return (None, score, 1, 0)

        moves = self.get_possible_moves(board)
        assert len(moves) > 0

        total_nodes_searched = 0
        total_cutoffs = 0

        if maximizing:
            best_score = -math.inf
            best_move = None

            for move in moves:
                board.place(move, color)
                _, score, nodes_searched, cutoffs = self.alpha_beta_search(board, depth - 1, color, opposite_color, alpha, beta, False)
                board.unplace(move)
                
                total_nodes_searched += nodes_searched
                total_cutoffs += cutoffs

                if score > best_score:
                    best_score = score
                    best_move = move

                    alpha = max(best_score, alpha)
                    if alpha >= beta:
                        total_cutoffs += 1
                        break

            self.put_in_tp_table(board, color, best_move, best_score)
            return (best_move, best_score, total_nodes_searched, total_cutoffs)
            
        else:
            best_score = math.inf
            best_move = None

            for move in moves:
                board.place(move, opposite_color)
                _, score, nodes_searched, cutoffs = self.alpha_beta_search(board, depth - 1, color, opposite_color, alpha, beta, True)
                board.unplace(move)
                
                total_nodes_searched += nodes_searched
                total_cutoffs += cutoffs

                if score < best_score:
                    best_score = score
                    best_move = move
                    
                    beta = min(best_score, beta)
                    if alpha >= beta:
                        total_cutoffs += 1
                        break
                    
            self.put_in_tp_table(board, opposite_color, best_move, best_score)
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

        if hash_code not in self.tp_table:
            self.tp_table[hash_code] = (move, score)
