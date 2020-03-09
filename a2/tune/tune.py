import logging
import random
from multiprocessing import Pool, freeze_support, cpu_count
from trueskill import Rating, rate_1vs1
import pickle

from util.hexboard import HexBoard
from search.minimax import Minimax
from search.mcts import MCTS
from evaluate.dijkstra import Dijkstra
from util import progressbar
from tune.export import save_configuration_result, save_search_settings, load_search_settings

logger = logging.getLogger(__name__)

# Inspiration: https://arxiv.org/pdf/1903.08129.pdf and https://arxiv.org/pdf/1812.06855.pdf

def run_hyperparameter_search(args):
    freeze_support() # for Windows support

    # Ranges for the hyperparameters
    N_min, N_max = 5, 50
    Cp_min, Cp_max = 0.5, 2.0

    # Ability to resume hyperparameter search runs
    new_settings = (args.num_configs, args.num_games, args.size, N_min, N_max, Cp_min, Cp_max)
    continue_previous_run = False
    remaining_num_configs = args.num_configs
    if not args.overwrite:
        cached_settings = load_search_settings()
        if cached_settings is not None and cached_settings == new_settings:
            completed_num_configs = sum(1 for line in open('output/hyperparameter-search.csv')) - 1
            remaining_num_configs = args.num_configs - completed_num_configs

            if remaining_num_configs <= 0:
                logger.critical('Hyperparameter search was already completed, call with --overwrite to re-run.')
                exit()

            else:
                continue_previous_run = True
                logger.info('Resuming from previous hyperparameter search, for the remaining %d/%d configurations.' % (remaining_num_configs, args.num_configs))

    if not continue_previous_run: save_search_settings(new_settings)
    save_configuration_result(('N', 'Cp', 'num_games', 'baseline_mu', 'baseline_sigma', 'config_mu', 'config_sigma'), clear=not continue_previous_run)

    # Create the random permutations
    hyperparameter_configs = []
    for i in range(remaining_num_configs):
        N = random.uniform(N_min, N_max)
        Cp = random.uniform(Cp_min, Cp_max)
        hyperparameter_configs.append((i, N, Cp, args.num_games, args.size))

    # Start the multi-threaded hyperparameter search
    thread_count = args.threads or cpu_count()
    logger.info('Creating %d threads for parallel search.' % thread_count)

    pool = Pool(thread_count)
    for _ in progressbar(pool.imap_unordered(test_configuration, hyperparameter_configs), desc='Running hyperparameter search', total=len(hyperparameter_configs)):
        pass
    
    logger.info('Finished hyperparameter search of %d randomly sampled configurations.' % args.num_configs)
    logger.info('Saved output/hyperparameter-search.csv')

# TODO: most of this code is duplicated from the rating module,
# so it should be refactored into a separate calculate_ratings() method.
def test_configuration(config_input):
    process_id, N, Cp, num_games, board_size = config_input

    baseline = Minimax(board_size, None, 0.1, Dijkstra(), False, False)

    r1 = Rating()
    r2 = Rating()
    r1_col, r2_col = HexBoard.RED, HexBoard.BLUE
    r1_first = True

    for _ in range(num_games + 1):
        m1, m2 = baseline, MCTS(N, Cp, board_size, Dijkstra(), False)
        board = HexBoard(board_size)

        r1_first = True if not r1_first else False
        r1_turn = True if r1_first else False

        first_color = r1_col if r1_first else r2_col
        second_color =  r2_col if r1_first else r1_col
        
        while not board.game_over():
            move = (m1 if r1_turn else m2).get_next_move(board, r1_col if r1_turn else r2_col)
            board.board[move] = r1_col if r1_turn else r2_col
            r1_turn = False if r1_turn else True

        if board.check_draw():
            r1, r2 = rate_1vs1(r1, r2, drawn=True)
        elif board.check_win(r1_col):
            r1, r2 = rate_1vs1(r1, r2, drawn=False)
        elif board.check_win(r2_col):
            r2, r1 = rate_1vs1(r2, r1, drawn=False)
        
    save_configuration_result((N, Cp, num_games, r1.mu, r1.sigma, r2.mu, r2.sigma))