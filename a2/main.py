import argparse
import sys
import logging

from util.hexboard import HexBoard
from util.game import HexGame
from rating.trueskill import run_trueskill
from rating.benchmark import run_benchmark
from rating.configs import configs

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt = '%m/%d/%Y %H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reinforcement learning for Hex")
    subparsers = parser.add_subparsers(dest='command')

    play = subparsers.add_parser('play', help='Play against the RL algorithm')
    play.add_argument('--disable-tt', action='store_true', help='If added, disables the transposition table')
    play.add_argument('--search', choices=['Minimax', 'MCTS'], default='MCTS', help='Set the search method')
    play.add_argument('--size', type=int, default=4, help='Set the board size')
    play.add_argument('--depth', type=int, default=None, help='Set the search depth')
    play.add_argument('--time-limit', type=float, default=None, help='Set the time limit')
    play.add_argument('--eval', choices=['Dijkstra', 'random', 'AStar'], default='Dijkstra', help='Choose the evaluation method')

    trueskill = subparsers.add_parser('trueskill', help='Evaluate the RL algorithm using TrueSkill')
    trueskill.add_argument('--config', choices=configs.keys(), default=None, help='If added, evaluate using TrueSkill using the chosen configuration set')
    trueskill.add_argument('--plot', action='store_true', help='If added, save the plots of the TrueSkill evaluations')
    trueskill.add_argument('--disable-tt', action='store_true', help='If added, disables the transposition table')

    benchmark = subparsers.add_parser('benchmark', help='Run a standardized benchmarking script')

    args = parser.parse_args(sys.argv[1:])

    # Play command
    if args.command == 'play':
        if args.search == 'Minimax' and not (args.depth or args.time_limit):
            logger.warn('Either depth or time limit needs to be set when using Minimax search.')
            exit()

        if args.depth and args.time_limit:
            logger.warn('Depth and time limit cannot both be set.')
            exit()

        logger.info('Booting gameplay script...')
        game = HexGame(args)
        board = HexBoard(args.size)
        game.run_interactively(board)
    
    # TrueSkill command
    elif args.command == 'trueskill':
        if not args.config:
            logger.warn('--config needs to be set.')
            exit()

        logger.info('Booting TrueSkill rating script...')
        run_trueskill(args)
    
    # Benchmark command
    elif args.command == 'benchmark':
        logger.info('Booting benchmark script...')
        run_benchmark()