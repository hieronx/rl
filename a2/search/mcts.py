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

        self.visits = defaultdict(int)
        self.rewards = defaultdict(int)
        self.children = dict()

        self.debug = True
        self.debug_output = []

    def get_next_move(self, board, color):
        self.start_time = time.time()

        if self.debug: self.log(0, 'Root', board)

        # Run the main MCTS loop iterations times
        for _ in range(self.iterations):
            selected_path, selected_leaf = self.select(board) # Select
            selected_board = HexBoard.from_hash_code(selected_leaf)
            self.expand(selected_leaf, selected_board, color) # Expand
            reward = self.simulate(selected_board, color, board.get_opposite_color(color)) # Simulate
            self.backpropagate(selected_path, reward) # Backpropagate
            if self.debug: self.log()

        if self.live_play:
            elapsed_time = time.time() - self.start_time
            cls()
            print("Generation of this next move took %f seconds." % elapsed_time)

        # If the root node wasn't visited, then return a random move (not sure why it wouldn't be visited?)
        if board.hash_code() not in self.children:
            return random.choice(self.get_possible_moves(board))
        
        # Return move with the highest number of visits
        # NOTE: This first line is different from the reference implementation, so it should be fixed and removed
        self.visits.pop(board.hash_code(), None)

        if self.debug:
            sorted_visits = {k: v for k, v in sorted(self.visits.items(), reverse=True, key=lambda item: item[1])}
            [self.log(1, 'Visits = %d, rewards = %d' % (sorted_visits[hc], self.rewards[hc]), HexBoard.from_hash_code(hc)) for hc in sorted_visits]
            self.save_debug_output()

        best_hash_code = max(self.visits, key=(lambda key: self.visits[key]))
        return board.get_move_between_boards(HexBoard.from_hash_code(best_hash_code))
        
    def select(self, board):
        self.log(1, 'Select')
        path = []
        node = board.hash_code()
        
        while True:
            path.append(node)

            # First visit the root node
            if node not in self.children or not self.children[node]:
                if self.debug: self.log(2, 'Select - root node', HexBoard.from_hash_code(path[-1]))
                return path, path[-1]
            
            # Every key in self.children is a visited node, while every child without these parents is an unvisited node
            unvisited = self.children[node] - self.children.keys()

            if unvisited:
                path.append(unvisited.pop())
                if self.debug: self.log(2, 'Select - found unvisited', HexBoard.from_hash_code(path[-1]))
                return path, path[-1]
            
            if self.debug: self.log(2, 'Select - add to path', HexBoard.from_hash_code(path[-1]))
            node = self.uct_select(node)

    def expand(self, selected_leaf, selected_board, color):
        if selected_leaf in self.children:
            if self.debug: self.log(1, 'Expand - already visited')
            return
        
        if self.debug: self.log(1, 'Expand')

        # Add the children of the leaf to the store
        new_children = [selected_board.make_move(move, color).hash_code() for move in self.get_possible_moves(selected_board)]
        self.children[selected_leaf] = new_children

        if self.debug: [self.log(2, 'Expand', selected_board.make_move(move, color)) for move in self.get_possible_moves(selected_board)]
    
    def simulate(self, selected_board, color, opposite_color):
        """Simulates a board until a terminal node is reached"""
        player = color

        children = self.children[selected_board.hash_code()]

        if len(children) > 0:
            node = HexBoard.from_hash_code(random.choice(children))

            if self.debug: self.log(1, 'Simulate', node)
            while True:
                if node.game_over():
                    if self.debug: self.log(2, 'Simulate - terminal', node)
                    reward = node.get_reward(player)
                    return reward
                
                if self.debug: self.log(2, 'Simulate', node)

                move = random.choice(self.get_possible_moves(node))
                node = node.make_move(move, player)

                player = color if player == opposite_color else opposite_color
        
        return 0


    def backpropagate(self, path, reward):
        if self.debug: self.log(1, 'Backpropagate')
        for node_hc in reversed(path):
            # Count visits and sum rewards for this path, all the way back to the root node
            self.visits[node_hc] += 1
            self.rewards[node_hc] += reward
            reward = 1 - reward
            if self.debug: self.log(2, 'Backpropagate', HexBoard.from_hash_code(node_hc))

    def uct_select(self, root_hc):
        """Calculate the UCB1 value for all moves and return the move with the highest value"""
        ln_N = math.log(self.visits[root_hc])

        def uct(node_hc):
            return self.rewards[node_hc] / self.visits[node_hc] + self.Cp * math.sqrt(ln_N / self.visits[node_hc])
        
        return max(self.children[root_hc], key=uct)
    
    def log(self, level = None, desc = None, hc = ''):
        if self.debug:
            self.debug_output.append((level, desc, hc))

    def save_debug_output(self):
        fn = 'output/mcts-debug.txt'
        with open(fn, 'w+', encoding='utf8') as output_file:
            for log in self.debug_output:
                if log[0] is None:
                    output_file.write('\n')
                else:
                    out = ('\t' * log[0]) + log[1] + ': ' + str(log[2]) + '\n'
                    output_file.write(out)
        
        logger.info('Saved %s' % fn)