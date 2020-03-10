import logging
import random
from collections import defaultdict

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
        for _ in range(self.N):
            selected_path, selected_leaf = self.select(board, color)
            self.expand(selected_leaf, color)
            reward = self.simulate(selected_leaf, color, board.get_opposite_color(color))
            self.backpropagate(selected_path, reward, color)
        
        # Return move with the highest number of visits
        if board.hash_code(color) not in self.children:
            return random.choice(self.get_possible_moves(board))
            
        board.print()
        best_hash_code = max(self.visits, key=(lambda key: self.visits[key]))
        HexBoard.from_hash_code(best_hash_code).print()
        return board.get_move_between_boards(HexBoard.from_hash_code(best_hash_code))
        
    def select(self, board, color):
        path = []
        while True:
            path.append(board)

            if board.hash_code(color) not in self.children or not self.children[board.hash_code(color)]:
                return path, path[-1]
            
            unexplored = self.children[board.hash_code(color)] - self.children.keys()

            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path, path[-1]
            
            board = self.uct_select(board)

    def expand(self, selected_leaf, color):
        if selected_leaf.hash_code(color) in self.children:
            return
        
        new_children = [selected_leaf.make_move(move, color) for move in self.get_possible_moves(selected_leaf)]
        self.children[selected_leaf.hash_code(color)] = new_children
            
    def simulate(self, board, color, opposite_color):
        """Simulates a board until a terminal node is reached"""
        invert_reward = True
        player = color
        while True:
            if board.game_over():
                reward = board.get_reward(player)
                return 1 - reward if invert_reward else reward
            
            move = random.choice(self.get_possible_moves(board))
            board = board.make_move(move, player)

            invert_reward = not invert_reward
            player = color if player == opposite_color else opposite_color

        logger.critical('Oops, this should not have happened.')

    def backpropagate(self, path, reward, color):
        for board in reversed(path):
            board_hash_code = board.hash_code(color)
            self.visits[board_hash_code] += 1
            self.rewards[board_hash_code] += reward
            reward = 1 - reward

    def uct_select(self, board):
        """Calculate the UCB1 value for all moves and return the move with the highest value"""
        ln_N = math.log(self.visits[board.hash_code])

        def uct(board):
            hash_code = board.hash_code()
            return self.rewards[hash_code] / self.visits[hash_code] + self.Cp * math.sqrt(ln_N / self.visits[hash_code])
        
        return max(self.children[board.hash_code()], key=uct)