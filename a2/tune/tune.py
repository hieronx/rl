import logging
import random
from multiprocessing import Pool, freeze_support, cpu_count
from trueskill import Rating, rate_1vs1
import pickle

from util.hexboard import HexBoard
from search.mcts import MCTS
from util import progressbar
from tune.export import save_configuration_result, print_results, save_plots, resume_previous_run
from rating.simulate import simulate_single_game
from tune.searches import searches

logger = logging.getLogger(__name__)

def run_tune(args):
    if args.search:
        run_hyperparameter_search(args.search, args)
    else:
        for search_name in searches.keys():
            args.search = search_name
            if 'num-configs' in searches[search_name]: args.num_configs = searches[search_name]['num-configs']
            if 'confidence-threshold' in searches[search_name]: args.confidence_threshold = searches[search_name]['confidence-threshold']
            run_hyperparameter_search(args)
            print()

def run_hyperparameter_search(args):
    freeze_support()

    # Load the config to evaluate
    search = searches[args.search]
    logger.info('Searching %s: N=[%d, %d] and Cp=[%.2f, %.2f] for board size %d.' % (args.search, search['N']['min'], search['N']['max'], search['Cp']['min'], search['Cp']['max'], search['size']))

    # Ability to resume hyperparameter search runs
    already_finished, continue_previous_run, remaining_num_configs = resume_previous_run(args)
    if already_finished: return
    if not continue_previous_run: save_configuration_result(args.search, ('N', 'Cp', 'num_games', 'baseline_mu', 'baseline_sigma', 'config_mu', 'config_sigma'), clear=True)

    # Create the randomly sampled configurations
    random.seed(1)
    hyperparameter_configs = [(i, args.search, int(random.uniform(search['N']['min'], search['N']['max'])), round(random.uniform(search['Cp']['min'], search['Cp']['max']), 4), args.num_games, args.confidence_threshold, search['size'], search['baseline']) for i in range(remaining_num_configs)]

    # Start the multi-threaded hyperparameter search
    thread_count = min(args.max_threads or (4 * cpu_count()), remaining_num_configs)
    logger.info('Creating %d threads for parallel search.' % thread_count)

    pool = Pool(thread_count)
    finished_count = args.num_configs - remaining_num_configs
    for _ in progressbar(pool.imap_unordered(test_configuration, hyperparameter_configs), desc='Running hyperparameter search', start=args.num_configs - remaining_num_configs, total=args.num_configs):
        finished_count += 1
        
        # Print results and save plots every once in a while
        if args.plot_steps and finished_count % args.plot_steps == 0:
            print_results(args.search)
            save_plots(args.search, search)

        pass
    
    logger.info('Finished hyperparameter search of %d randomly sampled configurations.' % args.num_configs)
    logger.info('Saved output/hyperparameter-search_%s.csv' % args.search)

    print_results(args.search)
    save_plots(args.search, search)
    
def test_configuration(config_input):
    process_id, search_name, N, Cp, num_games, confidence_threshold, board_size, baseline = config_input

    r1 = Rating()
    r2 = Rating()
    r1_color, r2_color = HexBoard.RED, HexBoard.BLUE
    r1_first = True

    if confidence_threshold:
        actual_num_games = 0
        while r1.sigma > confidence_threshold or r2.sigma > confidence_threshold:
            m1, m2 = baseline, MCTS(N, None, Cp, False)
            r1, r2, r1_first = simulate_single_game(board_size, r1, r2, m1, m2, r1_first, r1_color, r2_color)
            actual_num_games += 1

    for _ in range(num_games):
        m1, m2 = baseline, MCTS(N, None, Cp, False)
        r1, r2, r1_first = simulate_single_game(board_size, r1, r2, m1, m2, r1_first, r1_color, r2_color)
        
    save_configuration_result(search_name, (N, Cp, actual_num_games or num_games, r1.mu, r1.sigma, r2.mu, r2.sigma))