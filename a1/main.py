import argparse
import sys

from hexboard import HexBoard
from minimax import Minimax
from evaluate import Evaluate
from game import HexGame
from rating import run_trueskill

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Minimax for Hex")
    parser.add_argument('--trueskill', choices=['random-vs-Dijkstra', 'depth-vs-time-limit', 'Dijkstra-performance'], default=None, help='If added, evaluate using TrueSkill using the chosen configuration set')
    parser.add_argument('--disable-tt', action='store_true', help='If added, disables the transposition table')
    parser.add_argument('--size', type=int, default=4, help='Set the board size')
    parser.add_argument('--depth', type=int, default=None, help='Set the search depth')
    parser.add_argument('--time-limit', type=float, default=None, help='Set the time limit')
    parser.add_argument('--eval', choices=['Dijkstra', 'random', 'AStar'], default='Dijkstra', help='Choose the evaluation method')
    args = parser.parse_args(sys.argv[1:])

    if args.depth and args.time_limit:
        print('Depth and time limit cannot both be set.')
        exit()

    if args.trueskill:
        run_trueskill(args)
    else:
        game = HexGame(args.size, args.depth, args.time_limit, args.eval, args.disable_tt)
        board = HexBoard(args.size)
        game.run_interactively(board)
