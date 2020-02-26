import argparse
import sys

from hexboard import HexBoard
from minimax import Minimax
from evaluate import Evaluate
from game import HexGame
from rating import run_trueskill

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Minimax for Hex")
    parser.add_argument('--trueskill', action='store_true', help='If added, evaluate using TrueSkill')
    parser.add_argument('--disable-tt', action='store_true', help='If added, disables the transposition table')
    parser.add_argument('--size', type=int, default=4, help='Set the board size')
    parser.add_argument('--depth', type=int, default=4, help='Set the search depth')
    parser.add_argument('--eval', choices=['Dijkstra', 'random'], default='Dijkstra', help='Choose the evaluation method')
    args = parser.parse_args(sys.argv[1:])

    game = HexGame(args.size, args.depth, args.eval, args.disable_tt)
    board = HexBoard(args.size)

    if args.trueskill:
        run_trueskill(args)
    else:
        game.run_interactively(board)
