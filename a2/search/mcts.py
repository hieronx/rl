import logging
import random
import math
import time
from collections import defaultdict

from util import cls
from util.hexboard import HexBoard
from . import HexSearchMethod

logger = logging.getLogger(__name__)

class MCTS(HexSearchMethod):
    """This object houses all the code necessary for the MCTS implementation"""

    def __init__(self, iterations, Cp, live_play = True):
        self.iterations = iterations
        self.Cp = Cp
        self.live_play = live_play
        
    def get_next_move(self, board, color):
        self.start_time = time.time()
        self.root = MCTSNode(board, parent=None, player=color)

        # Run the main MCTS loop iterations times
        for _ in range(self.iterations):
            C = self.select_and_expand()
            reward = C.simulate()
            C.backpropagate(reward)

        if self.live_play:
            elapsed_time = time.time() - self.start_time
            cls()
            print("Generation of this next move took %f seconds." % elapsed_time)

        next_board = self.root.best_child(self.Cp).board
        return HexBoard.get_move_between_boards(self.root.board, next_board)

    def select_and_expand(self):
        current_node = self.root
        while not current_node.board.game_over():
            if not current_node.is_fully_expanded():
                return current_node.expand() # This calls expand
            else:
                current_node = current_node.best_child(self.Cp) # UCT select
        return current_node


class MCTSNode:

    def __init__(self, board, player, parent=None):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = []
        self._untried_actions = None
        self.num_visits = 0
        self.reward = 0

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.board.get_possible_moves()
        return self._untried_actions

    def expand(self):
        move = self.untried_actions.pop() # TODO: should be cached
        next_board = self.board.make_move(move, self.player)
        child_node = MCTSNode(next_board, parent=self, player=self.player)
        self.children.append(child_node)
        return child_node
    
    def simulate(self):
        current_board = self.board
        while not current_board.game_over():
            move = random.choice(current_board.get_possible_moves()) # TODO: should be cached
            current_board = current_board.make_move(move, self.player)
        return current_board.get_reward(self.player)

    def backpropagate(self, reward):
        self.num_visits += 1
        self.reward += reward
        if self.parent is not None:
            self.parent.backpropagate(1 - reward)

    def best_child(self, Cp):
        ln_N = math.log(self.num_visits)    
        def uct(c):
            return (c.reward / c.num_visits) + Cp * math.sqrt((2 * ln_N / c.num_visits))
        return max(self.children, key=uct)