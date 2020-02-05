import argparse
import sys
import numpy as np
import random

from hex_skeleton import HexBoard

class HexMinimax:

    def __init__(self, board_size):
        self.board_size = board_size

    def simulate(self):
        board = HexBoard(self.board_size)

        while not board.game_over:
            board.place(self.get_next_move(board), HexBoard.RED)
            board.place(self.get_next_move(board), HexBoard.BLUE)

        assert(board.game_over == True)
        board.print()

    def get_next_move(self, board):
        moves = self.get_possible_moves(board)

        return random.choice(moves)
    
    def get_possible_moves(self, board):
        empty_coordinates = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board.is_empty((x, y)):
                    empty_coordinates.append((x, y))

        return empty_coordinates
    
    def evaluate_board(self, board):
        return np.random.uniform(0, 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Minimax for Hex", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--size', type=int, default=4, help='Set the board size')
    
    args = parser.parse_args(sys.argv[1:])

    hex_minimax = HexMinimax(args.size)
    hex_minimax.simulate()