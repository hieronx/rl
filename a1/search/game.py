import math
import numpy as np

from util import cls
from hexboard import HexBoard
from minimax import Minimax
from evaluate import Evaluate
import time

char_to_row_idx = {'a': 0, 'b': 1, 'c': 2, 'd': 3}

class HexGame:

    def __init__(self, size, depth, eval_method):
        self.board_size = size
        self.search_depth = depth
        self.minimax = Minimax(size, depth, Evaluate(eval_method))

    def run_interactively(self, board):
        while not board.game_over:
            print("Waiting for CPU move...")
            move = self.minimax.get_next_move(board, HexBoard.RED)
            board.place(move, HexBoard.RED)
            board.print()
            print('\n')

            if board.game_over:
                break

            while True:
                move = input("Your move: ")

                if len(move) == 2:
                    x, y = move
                    if (x in char_to_row_idx and y.isdigit):
                        if board.is_empty((char_to_row_idx[x], int(y))):
                            break

            board.place((char_to_row_idx[x], int(y)), HexBoard.BLUE)

        if board.check_win(HexBoard.RED):
            print('The AI won.')
        else:
            print('You won.')

    def simulate(self, board):
        while not board.game_over:
            board.place(self.minimax.get_next_move(board, HexBoard.RED), HexBoard.RED)
            board.place(self.minimax.get_next_move(board, HexBoard.BLUE), HexBoard.BLUE)

        if board.check_win(HexBoard.RED):
            print('Red won.')
        else:
            print('Blue won.')

        board.print()