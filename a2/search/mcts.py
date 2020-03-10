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

    def __init__(self, N, Cp, evaluate_class, live_play = True):
        self.N = N
        self.Cp = Cp
        self.evaluate_class = evaluate_class
        self.live_play = live_play

        self.visits = defaultdict(int)
        self.rewards = defaultdict(int)
        self.children = dict()

    def get_next_move(self, board, color):
        self.start_time = time.time()

        # Run the main Select-Expand-Simulate-Backpropagate loop N times
        for _ in range(self.N):
            selected_path, selected_leaf = self.select(board, color) # Select
            selected_board = HexBoard.from_hash_code(selected_leaf)

            self.expand(selected_leaf, selected_board, color) # Expand
            reward = self.simulate(selected_board, color, board.get_opposite_color(color)) # Simulate
            self.backpropagate(selected_path, reward, color) # Backpropagate

        # If the root node wasn't visited, then return a random move (not sure why it wouldn't be visited?)
        if board.hash_code(color) not in self.children:
            return random.choice(self.get_possible_moves(board))
        
        if self.live_play:
            elapsed_time = time.time() - self.start_time
            cls()
            print("Generation of this next move took %f seconds." % elapsed_time)

        # Return move with the highest number of visits
        # NOTE: This first line is different from the reference implementation, so it should be fixed and removed
        self.visits.pop(board.hash_code(color), None)
        best_hash_code = max(self.visits, key=(lambda key: self.visits[key]))
        return board.get_move_between_boards(HexBoard.from_hash_code(best_hash_code))
        
    def select(self, board, color):
        path = []
        node = board.hash_code(color)
        
        while True:
            path.append(node)

            # First visit the root node
            if node not in self.children or not self.children[node]:
                return path, path[-1]
            
            # Every key in self.children is a visited node, while every child without these parents is an unvisited node
            unvisited = self.children[node] - self.children.keys()

            if unvisited:
                path.append(unvisited.pop())
                return path, path[-1]
            
            node = self.uct_select(node)

    def expand(self, selected_leaf, selected_board, color):
        if selected_leaf in self.children:
            return
        
        # Add the children of the leaf to the store
        new_children = [selected_board.make_move(move, color).hash_code(color) for move in self.get_possible_moves(selected_board)]
        self.children[selected_leaf] = new_children
            
    def simulate(self, selected_board, color, opposite_color):
        """Simulates a board until a terminal node is reached"""
        invert_reward = True
        player = color
        while True:
            if selected_board.game_over():
                reward = selected_board.get_reward(player)
                return 1 - reward if invert_reward else reward
            
            move = random.choice(self.get_possible_moves(selected_board))
            selected_board = selected_board.make_move(move, player)

            invert_reward = not invert_reward
            player = color if player == opposite_color else opposite_color

        logger.critical('Oops, this should not have happened.')

    def backpropagate(self, path, reward, color):
        for node_hc in reversed(path):
            # Count visits and sum rewards for this path, all the way back to the root node
            self.visits[node_hc] += 1
            self.rewards[node_hc] += reward
            reward = 1 - reward

    def uct_select(self, hash_code):
        """Calculate the UCB1 value for all moves and return the move with the highest value"""

        # TODO: remove this line
        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[hash_code])

        # TODO: fix this, self.visits[hash_code] should always be > 0
        ln_N = math.log(self.visits[hash_code]) if self.visits[hash_code] > 0 else math.log(1)

        def uct(hash_code):
            return self.rewards[hash_code] / self.visits[hash_code] + self.Cp * math.sqrt(ln_N / self.visits[hash_code])
        
        return max(self.children[hash_code], key=uct)