import argparse
import sys
import time

from hexboard import HexBoard
from minimax import Minimax
from evaluate import Evaluate
from game import HexGame

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Minimax for Hex")
    parser.add_argument('--simulate', action='store_true', help='If added, simulates both sides')
    parser.add_argument('--size', type=int, default=3, help='Set the board size')
    parser.add_argument('--depth', type=int, default=3, help='Set the search depth')
    args = parser.parse_args(sys.argv[1:])

    game = HexGame(args.size, args.depth)
    board = HexBoard(args.size)

    if args.simulate:
        game.simulate(board)
    else:
        game.run_interactively(board)
