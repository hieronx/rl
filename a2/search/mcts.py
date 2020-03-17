import logging
import random
import math
import time
from collections import defaultdict
from operator import attrgetter

from util import cls
from util.hexboard import HexBoard
from search import HexSearchMethod
from search.debug import log_tree
from search import selection_rules

logger = logging.getLogger(__name__)

class MCTS(HexSearchMethod):
    """This object houses all the code necessary for the MCTS implementation"""

    def __init__(self, num_iterations, time_limit = None, Cp = 1.4, live_play=True, amaf_alpha=0.0, debug=False):
        self.num_iterations = num_iterations
        self.time_limit = time_limit
        self.Cp = Cp
        self.live_play = live_play
        self.amaf_alpha = amaf_alpha
        self.debug = debug
        
    def get_next_move(self, board, color):
        start_time = time.time()
        self.root = MCTSNode(board.copy(), parent=None, player=color, turn=color, amaf_alpha=self.amaf_alpha)

        # Run the main MCTS loop num_iterations times
        i = 0
        if self.num_iterations:
            for _ in range(self.num_iterations):
                self.run_iteration()
                i += 1
        else:
            while (time.time() - start_time) < self.time_limit:
                self.run_iteration()
                i += 1

        if self.live_play:
            elapsed_time = time.time() - start_time
            cls()
            print("Generation of this next move took %.2f seconds, ran %d iterations." % (elapsed_time, i))

        if self.debug: log_tree(self.root)

        next_board = self.root.child_with_most_visits().board
        return HexBoard.get_move_between_boards(self.root.board, next_board)
    
    def run_iteration(self):
        node = self.select_and_expand()
        reward = node.simulate()
        node.backpropagate(reward)

    def select_and_expand(self):
        current_node = self.root
        winner = current_node.board.get_winner()
        while winner is None:
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child(self.Cp) # UCT select
            winner = current_node.board.get_winner()
        return current_node

    def __str__(self):
        return 'MCTS(%d, %.2fs, %.2f, %.2f)' % (
            self.num_iterations if self.num_iterations is not None else 0,
            self.time_limit if self.time_limit is not None else 0,
            self.Cp,
            self.amaf_alpha
        )
        
class MCTSNode:

    def __init__(self, board, player, parent=None, turn=None, amaf_alpha=0.0):
        self.board = board
        self.player = player
        self.parent = parent
        self.turn = turn
        
        self.children = []
        self.untried_moves = self.board.get_possible_moves()

        self.simulated_moves = []

        self.num_visits, self.num_amaf_visits = 0, 0
        self.reward, self.amaf_reward = 0, 0

        self.amaf_alpha = amaf_alpha

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def expand(self):
        move = self.untried_moves.pop() 
        next_board = self.board.make_move(move, self.player)
        child_node = MCTSNode(next_board, parent=self, player=self.player, turn=HexBoard.get_opposite_color(self.turn))
        self.children.append(child_node)
        return child_node
    
    def simulate(self):
        self.simulated_moves = []

        current_board = self.board.copy()
        all_moves = current_board.get_possible_moves()
        random.shuffle(all_moves)

        turn = self.player
        winner = current_board.get_winner()

        while winner is None:
            move = all_moves.pop()
<<<<<<< HEAD
=======
            self.simulated_moves.append(move) # Store a list of all simulated moves

>>>>>>> 59733ffd13f5c992e051fe3bff3aaf7e1f2932d9
            current_board.place(move, turn)
            turn = HexBoard.RED if turn == HexBoard.BLUE else HexBoard.BLUE
            winner = current_board.get_winner()

        return HexBoard.get_reward(self.player, winner)

    def backpropagate(self, reward, simulated_boards=None):
        self.num_visits += 1
        self.reward += reward

        # AMAF
        # the AMAF update adjusts the counts at the backpropagated nodes
        # as well as all siblings of the backpropagated nodes that correspond to a move made by the same player later in the play-out

        # https://ris.utwente.nl/ws/portalfiles/portal/5338883/polyy.pdf
        #  The indirect pair maintains the cumulative wins iw and samples is of all playouts made from any sibling of n where the move corresponding to n was played in the playout by the player who’s turn it is

        # https://durhamgo.club/GoByGo.pdf
        # When using AMAF, all the moves played out during the simulation phase need to be remembered. When it then comes to updating the tree, the algorithm not only updates the nodes that were visited, but also increments the AMAF scores for any sibling nodes which represent moves that were played at some point further on in that game.

        if self.parent is not None:
            # Run All-Moves-As-First
            simulated_boards = [self.parent.board.make_move(move, HexBoard.get_opposite_color(self.turn)).hash_code() for move in self.simulated_moves]

            for sibling in self.parent.children:
                if sibling.board.hash_code() in simulated_boards:
                    sibling.num_amaf_visits += 1
                    sibling.amaf_reward += reward

            # Backpropagate further up
            self.parent.backpropagate(reward)
    
    def child_with_most_visits(self):
        return self.best_child(0.0)

        # return max(self.children, key=attrgetter('num_visits'))

    def best_child(self, Cp):
        ln_N = selection_rules.log_n(self.num_visits)

        if self.amaf_alpha > 0.0:
            return max(self.children, key=lambda child: selection_rules.alpha_amaf_score(child, self.amaf_alpha, Cp, ln_N))
        else:
            return max(self.children, key=lambda child: selection_rules.uct_score(child.reward, child.num_visits, Cp, ln_N))