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
            print("Searched %d nodes and experienced %d cutoffs, transposition table size is %d." % (nodes_searched, cutoffs, len(self.tp_table)))
            print(self.tp_table[list(self.tp_table)[len(list(self.tp_table))-1]])

            elapsed_time = time.time() - start_time
            print("Generation of this next move took %f seconds." % elapsed_time)
        
        return move

    def alpha_beta_search(self, board, depth, color, opposite_color, alpha, beta, maximizing):
        hash_code = board.hash_code(color if maximizing else opposite_color)
        tt_best_move = None

        if hash_code in self.tp_table:
            if self.tp_table[hash_code][0] == depth:
                return (self.tp_table[hash_code][1], self.tp_table[hash_code][2], 0, 0)
            else:
                tt_best_move = self.tp_table[hash_code][1]
        
        if depth == 0 or board.game_over():
            score = self.evaluate.evaluate_board(board, color)
            return (None, score, 1, 0)

        # tt_best_move = None
        moves = self.get_possible_moves(board)
        if tt_best_move is not None:
            # if tt_best_move in moves: moves.remove(tt_best_move)
            moves.insert(0, tt_best_move)

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

            self.put_in_tp_table(board, color, depth, best_move, best_score)
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
                    
            self.put_in_tp_table(board, opposite_color, depth, best_move, best_score)
            return (best_move, best_score, total_nodes_searched, total_cutoffs)

    def get_possible_moves(self, board):
        empty_coordinates = [coord for coord, color in board.board.items() if color == HexBoard.EMPTY]
        return empty_coordinates

    def put_in_tp_table(self, board, color, depth, move, score):
        hash_code = board.hash_code(color)
        self.tp_table[hash_code] = (depth, move, score)

        # if hash_code not in self.tp_table:
        #     self.tp_table[hash_code] = (depth, move, score)
