import logging
import random
from multiprocessing import Pool, freeze_support, cpu_count, Value
import threading
from trueskill import Rating, rate_1vs1
import pickle
import time

from util.hexboard import HexBoard
from search.mcts import MCTS
from util import print_progressbar
from tune.export import save_configuration_result, print_results, save_plots, has_already_completed
from rating.simulate import simulate_single_game_winner
from tune.searches import searches

logger = logging.getLogger(__name__)

hyperparameter_configs = []
num_games_per_matchup = 1

completed_num_games = Value('i', 0)
total_num_games = 0

def run_tune(args):
    if args.search:
        if 'num-configs' in searches[args.search]: args.num_configs = searches[args.search]['num-configs']
        run_hyperparameter_search(args)
    else:
        for search_name in searches.keys():
            args.search = search_name
            if 'num-configs' in searches[search_name]: args.num_configs = searches[search_name]['num-configs']
            run_hyperparameter_search(args)
            print()

def run_hyperparameter_search(args):
    global total_num_games, max_num_games_per_config, hyperparameter_configs
    freeze_support()

    if args.num_configs == 0 or has_already_completed(args): return

    # Load the config to evaluate
    search = searches[args.search]
    logger.info('Searching %s: N=[%d, %d] and Cp=[%.2f, %.2f] for board size %d.' % (args.search, search['N']['min'], search['N']['max'], search['Cp']['min'], search['Cp']['max'], search['size']))

    # Create the randomly sampled configurations
    hyperparameter_configs = [{
        'search': args.search,
        'N': int(random.uniform(search['N']['min'], search['N']['max'])),
        'Cp': round(random.uniform(search['Cp']['min'], search['Cp']['max']), 4),
        'size': search['size'],
        'trueskill_mu': Value('d', 25.0),
        'trueskill_sigma': Value('d', 25/3)
    } for _ in range(args.num_configs)]

    # Start the multi-threaded hyperparameter search
    thread_count = min(args.max_threads or (4 * cpu_count()), args.num_configs)
    logger.info('Creating %d threads for parallel search.' % thread_count)

    t = threading.Thread(target=print_progress, args=(args.plot_steps, args.search, search))
    t.start()

    pool = Pool(thread_count)
    total_num_games = (len(hyperparameter_configs)**2 - len(hyperparameter_configs)) * args.num_games
    save_results(args.search)

    for _ in pool.imap_unordered(run_matchups, [(player_id, args.num_games) for player_id in range(len(hyperparameter_configs))]):        
        pass

    save_results(args.search)
    
    logger.info('Finished hyperparameter search of %d randomly sampled configurations.' % args.num_configs)
    logger.info('Saved output/hyperparameter-search_%s.csv' % args.search)

    print_results(args.search)
    save_plots(args.search, search)
    
def run_matchups(matchup_input):
    global completed_num_games, hyperparameter_configs
    player_id, num_games = matchup_input
    player = hyperparameter_configs[player_id]

    for opponent in hyperparameter_configs:
        if player == opponent:
            continue
            
        m1, m2 = MCTS(player['N'], None, player['Cp'], False), MCTS(opponent['N'], None, opponent['Cp'], False)
        r1_color, r2_color = HexBoard.RED, HexBoard.BLUE
        r1_first = True
        
        for _ in range(num_games):
            winner, r1_first = simulate_single_game_winner(player['size'], m1, m2, r1_first, r1_color, r2_color)

            prev_r1 = Rating(mu=player['trueskill_mu'].value, sigma=player['trueskill_sigma'].value)
            prev_r2 = Rating(mu=opponent['trueskill_mu'].value, sigma=opponent['trueskill_sigma'].value)
            
            if winner == HexBoard.EMPTY:
                r1, r2 = rate_1vs1(prev_r1, prev_r2, drawn=True)
            elif winner == r1_color:
                r1, r2 = rate_1vs1(prev_r1, prev_r2, drawn=False)
            elif winner == r2_color:
                r2, r1 = rate_1vs1(prev_r2, prev_r1, drawn=False)

            player_mu_diff, player_sigma_diff = r1.mu - prev_r1.mu, r1.sigma - prev_r1.sigma
            opponent_mu_diff, opponent_sigma_diff = r2.mu - prev_r2.mu, r2.sigma - prev_r2.sigma

            # Only after completing the game and calculating the mu and sigma difference, do we get a lock, so it's locked for as short a time as possible
            with player['trueskill_mu'].get_lock(), player['trueskill_sigma'].get_lock(), opponent['trueskill_mu'].get_lock(), opponent['trueskill_sigma'].get_lock():
                player['trueskill_mu'].value += player_mu_diff
                player['trueskill_sigma'].value += player_sigma_diff
                opponent['trueskill_mu'].value += opponent_mu_diff
                opponent['trueskill_sigma'].value += opponent_sigma_diff
                
            with completed_num_games.get_lock():
                completed_num_games.value += 1

def save_results(search_name):
    global hyperparameter_configs
    save_configuration_result(search_name, ('size', 'N', 'Cp', 'trueskill_mu', 'trueskill_sigma'), clear=True)

    for player in hyperparameter_configs:
        save_configuration_result(player['search'], (player['size'], player['N'], player['Cp'], player['trueskill_mu'].value, player['trueskill_sigma'].value))

def print_progress(plot_steps, search_name, search):
    global completed_num_games, total_num_games

    start_time = time.time()
    last_logged_perc = 0.0

    while total_num_games == 0 or int(completed_num_games.value) < total_num_games:
        if total_num_games > 0:
            if plot_steps is not None:
                current_perc = int(completed_num_games.value) / total_num_games
                if current_perc >= (last_logged_perc + (plot_steps / 100)):
                    last_logged_perc = current_perc
                    save_results(search_name)
                    # save_plots(search_name, search)

            print_progressbar(desc='Running hyperparameter search', completed=int(completed_num_games.value), start_time=start_time, total=total_num_games)

        time.sleep(0.5)