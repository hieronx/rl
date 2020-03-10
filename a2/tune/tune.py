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
from tune.export import save_configuration_result, print_results, save_plots, save_search_settings, load_search_settings, resume_previous_run
from rating.simulate import simulate_single_game

logger = logging.getLogger(__name__)

def run_hyperparameter_search(args):
    freeze_support()

    # Ranges for the hyperparameters
    N_min, N_max = 5, 50
    Cp_min, Cp_max = 0.5, 2.0

    # Ability to resume hyperparameter search runs
    new_settings = (args.num_games, args.size, N_min, N_max, Cp_min, Cp_max)
    continue_previous_run, remaining_num_configs = resume_previous_run(args, new_settings)

    if not continue_previous_run:
        save_search_settings(new_settings)
        save_configuration_result(('N', 'Cp', 'num_games', 'baseline_mu', 'baseline_sigma', 'config_mu', 'config_sigma'), clear=True)

    # Create the randomly sampled configurations
    random.seed(1)
    hyperparameter_configs = [(i, int(random.uniform(N_min, N_max)), round(random.uniform(Cp_min, Cp_max), 4), args.num_games, args.size) for i in range(remaining_num_configs)]

    # Start the multi-threaded hyperparameter search
    thread_count = min(args.max_threads or (4 * cpu_count()), remaining_num_configs)
    logger.info('Creating %d threads for parallel search.' % thread_count)

    pool = Pool(thread_count)
    for _ in progressbar(pool.imap_unordered(test_configuration, hyperparameter_configs), desc='Running hyperparameter search', start=args.num_configs - remaining_num_configs, total=args.num_configs):
        pass
    
    logger.info('Finished hyperparameter search of %d randomly sampled configurations.' % args.num_configs)
    logger.info('Saved output/hyperparameter-search.csv')

    print_results()
    save_plots()
    
def test_configuration(config_input):
    process_id, N, Cp, num_games, board_size = config_input

    r1 = Rating()
    r2 = Rating()
    r1_color, r2_color = HexBoard.RED, HexBoard.BLUE
    r1_first = True

    for _ in range(num_games):
        m1, m2 = Minimax(board_size, None, 0.01, Dijkstra(), False, False), MCTS(N, Cp, board_size, Dijkstra(), False)
        r1, r2, r1_first = simulate_single_game(board_size, r1, r2, m1, m2, r1_first, r1_color, r2_color)
        
    save_configuration_result((N, Cp, num_games, r1.mu, r1.sigma, r2.mu, r2.sigma))