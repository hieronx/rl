import argparse
import sys
import logging

from hexboard import HexBoard
from game import HexGame
from rating import run_trueskill

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt = '%m/%d/%Y %H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reinforcement learning for Hex")
    parser.add_argument('task', choices=['play', 'trueskill'])
    parser.add_argument('--config', choices=['random-vs-Dijkstra', 'depth-vs-time-limit', 'Dijkstra-performance', 'Minimax-vs-MCTS'], default=None, help='If added, evaluate using TrueSkill using the chosen configuration set')
    parser.add_argument('--plot', action='store_true', help='If added, save the plots of the TrueSkill evaluations')
    parser.add_argument('--disable-tt', action='store_true', help='If added, disables the transposition table')
    parser.add_argument('--search', choices=['Minimax', 'MCTS'], default='MCTS', help='Set the search method')
    parser.add_argument('--size', type=int, default=4, help='Set the board size')
    parser.add_argument('--depth', type=int, default=None, help='Set the search depth')
    parser.add_argument('--time-limit', type=float, default=None, help='Set the time limit')
    parser.add_argument('--eval', choices=['Dijkstra', 'random', 'AStar'], default='Dijkstra', help='Choose the evaluation method')
    args = parser.parse_args(sys.argv[1:])

    if args.task == 'trueskill' and not args.config:
        logger.warn('--config needs to be set.')
        exit()

    if args.search == 'Minimax' and not (args.depth or args.time_limit):
        logger.warn('Either depth or time limit needs to be set when using Minimax search.')
        exit()

    if args.depth and args.time_limit:
        logger.warn('Depth and time limit cannot both be set.')
        exit()

    if args.task == 'trueskill':
        run_trueskill(args)
    else:
        game = HexGame(args)
        board = HexBoard(args.size)
        game.run_interactively(board)
