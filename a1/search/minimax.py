import math
import numpy as np
import time

from util import cls
from hexboard import HexBoard

class Minimax:

    def __init__(self, size, depth, time_limit, evaluate_class, live_play = True):
        self.board_size = size
        self.depth = depth
        self.time_limit = time_limit
        self.evaluate = evaluate_class
        self.live_play = live_play
        self.tp_table = {}
        self.stats = { 'nodes_searched': 0, 'cutoffs': 0, 'tt_lookups': 0 }

    def get_next_move(self, board, color):
        start_time = time.time()
        alpha = -math.inf
        beta = math.inf
        opposite_color = board.get_opposite_color(color)

        assert self.depth is not None or self.time_limit is not None

        if self.depth:
            print('Using depth %d' % self.depth)
            move, _ = self.alpha_beta_search(board, self.depth, color, opposite_color, alpha, beta, True)
        elif self.time_limit:
            print('Using time limit')
            max_depth = 1
            while (time.time() - start_time) < self.time_limit:
                move, _ = self.alpha_beta_search(board, max_depth, color, opposite_color, alpha, beta, True)
                max_depth += 1
        
        if self.live_play:
            elapsed_time = time.time() - start_time

            cls()
            print("Searched to depth %d, evaluated %d nodes, experienced %d cutoffs, and used %d TT lookups." % (max_depth, self.stats['nodes_searched'], self.stats['cutoffs'], self.stats['tt_lookups']))
            print("Generation of this next move took %f seconds." % elapsed_time)
        
        self.stats = { 'nodes_searched': 0, 'cutoffs': 0, 'tt_lookups': 0 }

        return move

    def alpha_beta_search(self, board, depth, color, opposite_color, alpha, beta, maximizing):
        hash_code = board.hash_code(color if maximizing else opposite_color)
        cached_best_move = None

        if hash_code in self.tp_table:
            if self.tp_table[hash_code][0] == depth:
                self.stats['tt_lookups'] += 1
                return (self.tp_table[hash_code][1], self.tp_table[hash_code][2])
            else:
                cached_best_move = self.tp_table[hash_code][1]
        
        if depth == 0 or board.game_over():
            score = self.evaluate.evaluate_board(board, color)
            self.stats['nodes_searched'] += 1
            return (None, score)

        moves = self.get_possible_moves(board)
        
        if cached_best_move is not None:
            moves.insert(0, cached_best_move)

        if maximizing:
            best_score = -math.inf
            best_move = None

            for move in moves:
                board.place(move, color)
                _, score = self.alpha_beta_search(board, depth - 1, color, opposite_color, alpha, beta, False)
                board.unplace(move)

                if score > best_score:
                    best_score = score
                    best_move = move

                    alpha = max(best_score, alpha)
                    if alpha >= beta:
                        self.stats['cutoffs'] += 1
                        break

            self.tp_table[board.hash_code(color)] = (depth, best_move, best_score)
            return (best_move, best_score)
            
        else:
            best_score = math.inf
            best_move = None

            for move in moves:
                board.place(move, opposite_color)
                _, score = self.alpha_beta_search(board, depth - 1, color, opposite_color, alpha, beta, True)
                board.unplace(move)

                if score < best_score:
                    best_score = score
                    best_move = move
                    
                    beta = min(best_score, beta)
                    if alpha >= beta:
                        self.stats['cutoffs'] += 1
                        break
                    
            self.tp_table[board.hash_code(opposite_color)] = (depth, best_move, best_score)
            return (best_move, best_score)

    def get_possible_moves(self, board):
        return [coord for coord, color in board.board.items() if color == HexBoard.EMPTY]