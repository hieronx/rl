import argparse
import sys
import numpy as np
import random

from hex_skeleton import HexBoard

char_to_row_idx = { 'a': 0, 'b': 1, 'c': 2, 'd': 3 }

class HexMinimax:

    def __init__(self, board_size):
        self.board_size = board_size

    def run_interactively(self, board):
        while not board.game_over:
            board.place(self.get_next_move(board), HexBoard.RED)
            board.print()
            print('\n')

            while True:
                move = input("Your move: ")

                if len(move) == 2:
                    x, y = move
                    if (x in char_to_row_idx and y.isdigit):
                        if board.is_empty((char_to_row_idx[x], int(y))): break
            
            board.place((char_to_row_idx[x], int(y)), HexBoard.BLUE)

    def simulate(self, board):
        while not board.game_over:
            board.place(self.get_next_move(board), HexBoard.RED)
            board.place(self.get_next_move(board), HexBoard.BLUE)

        if board.check_win(HexBoard.RED): print('Red won.')
        else: print('Blue won.')

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
    parser = argparse.ArgumentParser(description="Minimax for Hex", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--simulate', action='store_true', help='If added, simulates both sides')
    parser.add_argument('--size', type=int, default=4, help='Set the board size')
    args = parser.parse_args(sys.argv[1:])

    hex_minimax = HexMinimax(args.size)
    board = HexBoard(args.size)

    if args.simulate: hex_minimax.simulate(board)
    else: hex_minimax.run_interactively()