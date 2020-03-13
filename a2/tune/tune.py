import logging
import random
from multiprocessing import Pool, freeze_support, cpu_count
from trueskill import Rating, rate_1vs1
import pickle

from util.hexboard import HexBoard
from search.mcts import MCTS
from util import progressbar
from tune.export import save_configuration_result, print_results, save_plots, save_search_settings, load_search_settings, resume_previous_run
from rating.simulate import simulate_single_game
from tune.configs import tune_configs

logger = logging.getLogger(__name__)

def run_searches(args):
    if args.config:
        run_hyperparameter_search(args.config, args)
    else:
        for config_name in tune_configs.keys():
            run_hyperparameter_search(config_name, args)

def run_hyperparameter_search(config_name, args):
    freeze_support()

    # Load the config to evaluate
    config = tune_configs[config_name]
    logger.info('Searching config %s: N=[%d, %d] and Cp=[%.2f, %.2f] for board size %d.' % (config_name, config['N']['min'], config['N']['max'], config['Cp']['min'], config['Cp']['max'], config['size']))

    # Ability to resume hyperparameter search runs
    new_settings = (args.num_games, config['size'], config['N']['min'], config['N']['max'], config['Cp']['min'], config['Cp']['max'])
    continue_previous_run, remaining_num_configs = resume_previous_run(args, new_settings)

    if not continue_previous_run:
        save_search_settings(new_settings)
        save_configuration_result(('N', 'Cp', 'num_games', 'baseline_mu', 'baseline_sigma', 'config_mu', 'config_sigma'), clear=True)

    # Create the randomly sampled configurations
    random.seed(1)
    hyperparameter_configs = [(i, int(random.uniform(config['N']['min'], config['N']['max'])), round(random.uniform(config['Cp']['min'], config['Cp']['max']), 4), args.num_games, config['size'], config['baseline']) for i in range(remaining_num_configs)]

    # Start the multi-threaded hyperparameter search
    thread_count = min(args.max_threads or (4 * cpu_count()), remaining_num_configs)
    logger.info('Creating %d threads for parallel search.' % thread_count)

    pool = Pool(thread_count)
    finished_count = args.num_configs - remaining_num_configs
    for _ in progressbar(pool.imap_unordered(test_configuration, hyperparameter_configs), desc='Running hyperparameter search', start=args.num_configs - remaining_num_configs, total=args.num_configs):
        finished_count += 1
        
        # Print results and save plots every once in a while
        if args.plot_steps and finished_count % args.plot_steps == 0:
            print_results()
            save_plots()

        pass
    
    logger.info('Finished hyperparameter search of %d randomly sampled configurations.' % args.num_configs)
    logger.info('Saved output/hyperparameter-search.csv')

    print_results()
    save_plots()
    
def test_configuration(config_input):
    process_id, N, Cp, num_games, board_size, baseline = config_input

    r1 = Rating()
    r2 = Rating()
    r1_color, r2_color = HexBoard.RED, HexBoard.BLUE
    r1_first = True

    for _ in range(num_games):
        m1, m2 = baseline, MCTS(N, None, Cp, False)
        r1, r2, r1_first = simulate_single_game(board_size, r1, r2, m1, m2, r1_first, r1_color, r2_color)
        
    save_configuration_result((N, Cp, num_games, r1.mu, r1.sigma, r2.mu, r2.sigma))