import argparse
import sys
import logging

from util.hexboard import HexBoard
from util.game import HexGame
from rating.trueskill import run_trueskill
from rating.benchmark import run_benchmark
from rating.configs import configs
from tune.tune import run_tune
from tune.searches import searches

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt = '%H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reinforcement learning for Hex")
    subparsers = parser.add_subparsers(dest='command')

    play = subparsers.add_parser('play', help='Play against the RL algorithm')
    search_sp = play.add_subparsers(dest='search')

    minimax = search_sp.add_parser('minimax', help='Play against Minimax')
    minimax.add_argument('--disable-tt', action='store_true', help='If added, disables the transposition table')
    minimax.add_argument('--size', type=int, default=4, help='Set the board size')
    minimax.add_argument('--depth', type=int, default=None, help='Set the search depth for Minimax')
    minimax.add_argument('--time-limit', type=float, default=None, help='Set the time limit for Minimax')
    minimax.add_argument('--eval', choices=['Dijkstra', 'random', 'AStar'], default='Dijkstra', help='Choose the evaluation method')
    
    mcts = search_sp.add_parser('mcts', help='Play against MCTS')
    mcts.add_argument('--num-iterations', type=int, default=None, help='Set the number of iterations for MCTS')
    mcts.add_argument('--cp', type=float, default=1.4, help='Set the exploration-exploitation tradeoff constant for MCTS')
    mcts.add_argument('--time-limit', type=float, default=None, help='Set the time limit for MCTS')
    mcts.add_argument('--size', type=int, default=4, help='Set the board size')
    mcts.add_argument('--eval', choices=['Dijkstra', 'random', 'AStar'], default='Dijkstra', help='Choose the evaluation method')

    trueskill = subparsers.add_parser('trueskill', help='Evaluate the RL algorithm using TrueSkill')
    trueskill.add_argument('--config', choices=configs.keys(), required=True, help='If added, evaluate using TrueSkill using the chosen configuration set')
    trueskill.add_argument('--max-threads', type=int, help='Set the maximum number of threads')
    trueskill.add_argument('--plot', action='store_true', help='If added, save the plots of the TrueSkill evaluations')
    trueskill.add_argument('--disable-tt', action='store_true', help='If added, disables the transposition table')

    tune = subparsers.add_parser('tune', help='Run a hyperparameter search for MCTS')
    tune.add_argument('--search', choices=searches.keys(), help='If added, run hyperparameter search for the chosen settings')
    tune.add_argument('--all', action='store_true', help='Whether to run all saved searches')
    tune.add_argument('--max-threads', type=int, help='Set the maximum number of threads')
    tune.add_argument('--num-configs', type=int, default=50, help='Set the number of configurations to try')
    tune.add_argument('--num-games', type=int, default=50, help='Set the number of games to play per configuration')
    tune.add_argument('--overwrite', action='store_true', help='Whether to overwrite the previous run')
    tune.add_argument('--plot-steps', type=int, default=None, help='Save plots every X number of configurations')

    benchmark = subparsers.add_parser('benchmark', help='Run a standardized benchmarking script')

    args = parser.parse_args(sys.argv[1:])

    # Play command
    if args.command == 'play':
        if args.search == 'minimax':
            if not (args.depth or args.time_limit):
                logger.critical('Either --depth or --time-limit needs to be set when using Minimax search.')
                exit()

            if args.depth and args.time_limit:
                logger.critical('--depth and --time-limit cannot both be set.')
                exit()
        elif args.search == 'mcts':
            if not (args.num_iterations or args.time_limit):
                logger.critical('Either --num-iterations or --time-limit needs to be set when using MCTS search.')
                exit()

            if args.num_iterations and args.time_limit:
                logger.critical('--num-iterations and --time-limit cannot both be set.')
                exit()

        logger.info('Booting gameplay script...')
        game = HexGame(args)
        board = HexBoard(args.size)
        game.run_interactively(board)
    
    # TrueSkill command
    elif args.command == 'trueskill':
        logger.info('Booting TrueSkill rating script...')
        run_trueskill(args)
    
    # Tune command
    elif args.command == 'tune':
        if not args.search and not args.all:
            logger.critical('--search or --all needs to be set.')
            exit()

        logger.info('Booting hyperparameter tuning script...')
        run_tune(args)
    
    # Benchmark command
    elif args.command == 'benchmark':
        logger.info('Booting benchmark script...')
        run_benchmark()