import logging
import random
import math
import time
from collections import defaultdict
from operator import attrgetter

from util import cls
from util.hexboard import HexBoard
from . import HexSearchMethod
from search.debug import log_tree

logger = logging.getLogger(__name__)

class MCTS(HexSearchMethod):
    """This object houses all the code necessary for the MCTS implementation"""

    def __init__(self, num_iterations, time_limit = None, Cp = 1.4, live_play = True):
        self.num_iterations = num_iterations
        self.time_limit = time_limit
        self.Cp = Cp
        self.live_play = live_play
        
    def get_next_move(self, board, color, debug=False):
        start_time = time.time()
        self.root = MCTSNode(board, parent=None, player=color)

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
        
        if debug: log_tree(self.root)

        next_board = self.root.child_with_most_visits().board
        return HexBoard.get_move_between_boards(self.root.board, next_board)
    
    def run_iteration(self):
        node = self.select_and_expand()
        reward = node.simulate()
        node.backpropagate(reward)

    def select_and_expand(self):
        current_node = self.root
        while not current_node.board.game_over():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child(self.Cp) # UCT select
        return current_node

class MCTSNode:

    def __init__(self, board, player, parent=None):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = []
        self.untried_moves = self.board.get_possible_moves()
        self.num_visits = 0
        self.reward = 0

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def expand(self):
        move = self.untried_moves.pop() # TODO: should be cached
        next_board = self.board.make_move(move, self.player)
        child_node = MCTSNode(next_board, parent=self, player=self.player)
        self.children.append(child_node)
        return child_node
    
    def simulate(self):
        current_board = self.board
        all_moves = current_board.get_possible_moves()
        turn = self.player
        while not current_board.game_over():
            move = random.choice(all_moves)
            all_moves.remove(move)
            current_board = current_board.make_move(move, turn)

            turn = current_board.get_opposite_color(self.player) if turn == self.player else self.player

        return current_board.get_reward(self.player)

    def backpropagate(self, reward):
        self.num_visits += 1
        self.reward += reward
        if self.parent is not None:
            self.parent.backpropagate(reward)
    
    def child_with_most_visits(self):
        return max(self.children, key=attrgetter('num_visits'))

    def best_child(self, Cp):
        ln_N = math.log(self.num_visits)
        def uct(c):
            return (c.reward / c.num_visits) + Cp * math.sqrt((2 * ln_N / c.num_visits))
        return max(self.children, key=uct)