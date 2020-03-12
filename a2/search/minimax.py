import math
import time

from util import cls
from util.hexboard import HexBoard
from . import HexSearchMethod

class Minimax(HexSearchMethod):
    """This object houses all the code necessary for the minimax implementation"""

    def __init__(self, depth, time_limit, evaluate_class, live_play = True, disable_tt = False):
        """Initializes a new minimax object that is either depth-bound or time-limit bound"""
        assert depth is not None or time_limit is not None

        self.depth = depth
        self.time_limit = time_limit
        self.evaluate = evaluate_class
        self.live_play = live_play
        self.disable_tt = disable_tt
        self.start_time = 0

        self.tp_table = {}
        self.stats = { 'nodes_searched': 0, 'cutoffs': 0, 'tt_lookups': 0 }

    def get_next_move(self, board, color):
        """Returns the best next move for the provided color on the provided board/state"""
        self.start_time = time.time()
        alpha = -math.inf
        beta = math.inf
        opposite_color = HexBoard.get_opposite_color(color)

        max_depth = self.depth or 1
        if self.depth:
            best_move, _ = self.alpha_beta_search(board, self.depth, color, opposite_color, alpha, beta, True)
        elif self.time_limit:
            best_move = None
            while (time.time() - self.start_time) < self.time_limit:
                new_move, new_score = self.alpha_beta_search(board, max_depth, color, opposite_color, alpha, beta, True)
                if new_move is not None and new_score is not None:
                    best_move = new_move
                max_depth += 1
        
        if self.live_play:
            elapsed_time = time.time() - self.start_time

            cls()
            print("Searched to depth %d, evaluated %d nodes, experienced %d cutoffs, and used %d TT lookups." % (max_depth, self.stats['nodes_searched'], self.stats['cutoffs'], self.stats['tt_lookups']))
            print("Generation of this next move took %.2f seconds." % elapsed_time)
        
        self.stats = { 'nodes_searched': 0, 'cutoffs': 0, 'tt_lookups': 0 }

        return best_move

    def alpha_beta_search(self, board, depth, color, opposite_color, alpha, beta, maximizing):
        """Handles minimax search using alpha beta pruning and good use of move-ordering and transposition tables"""
        cached_best_move = None

        # stop handling any code and immediately drop all your responsibilities if times has passed
        if self.time_limit is not None and (time.time() - self.start_time) >= self.time_limit: 
            return (None, None)
        
        if not self.disable_tt:
            hash_code = board.hash_code(color if maximizing else opposite_color)

            if hash_code in self.tp_table:
                if self.tp_table[hash_code][0] == depth:
                    self.stats['tt_lookups'] += 1
                    return (self.tp_table[hash_code][1], self.tp_table[hash_code][2])
                else:
                    cached_best_move = self.tp_table[hash_code][1]
        
        if depth == 0 or board.get_winner() is not None:
            score = self.evaluate.evaluate_board(board, color)
            self.stats['nodes_searched'] += 1
            return (None, score)

        moves = board.get_possible_moves()
        
        if cached_best_move is not None:
            moves.insert(0, cached_best_move)

        if maximizing:
            best_score = -math.inf
            best_move = None

            for move in moves:
                board.place(move, color)
                _, score = self.alpha_beta_search(board, depth - 1, color, opposite_color, alpha, beta, False)
                board.place(move, HexBoard.EMPTY)

                if score == None:
                    return (None, None)

                if score > best_score:
                    best_score = score
                    best_move = move

                    alpha = max(best_score, alpha)
                    if alpha >= beta:
                        self.stats['cutoffs'] += 1
                        break

            if not self.disable_tt: self.tp_table[board.hash_code(color)] = (depth, best_move, best_score)
            return (best_move, best_score)
            
        else:
            best_score = math.inf
            best_move = None

            for move in moves:
                board.place(move, opposite_color)
                _, score = self.alpha_beta_search(board, depth - 1, color, opposite_color, alpha, beta, True)
                board.place(move, HexBoard.EMPTY)

                if score == None:
                    return (None, None)

                if score < best_score:
                    best_score = score
                    best_move = move
                    
                    beta = min(best_score, beta)
                    if alpha >= beta:
                        self.stats['cutoffs'] += 1
                        break
                    
            if not self.disable_tt: self.tp_table[board.hash_code(opposite_color)] = (depth, best_move, best_score)
            return (best_move, best_score)