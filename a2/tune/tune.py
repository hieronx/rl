from multiprocessing import Pool, freeze_support, cpu_count, Value, Array
from multiprocessing.pool import ThreadPool
import threading
from trueskill import Rating, rate_1vs1
import logging, os, time, copy, random

from util.hexboard import HexBoard
from search.mcts import MCTS
from util import print_progressbar, progressbar
from tune.export import save_configuration_result, print_results, save_plots, has_already_completed
from rating.simulate import simulate_single_game_winner
from tune.searches import searches

logger = logging.getLogger(__name__)

def run_tune(args):
    if args.search:
        if 'num-configs' in searches[args.search]: args.num_configs = searches[args.search]['num-configs']
        run_hyperparameter_search(args)
    else:
        for search_name in searches.keys():
            args.search = search_name
            args.overwrite = True
            if 'num-configs' in searches[search_name]: args.num_configs = searches[search_name]['num-configs']
            
            run_hyperparameter_search(args)
            print()

def run_hyperparameter_search(args):
    freeze_support()

    if args.num_configs == 0 or has_already_completed(args): return

    # Load the config to evaluate
    search = searches[args.search]
    logger.info('Searching %s: N=[%d, %d] and Cp=[%.2f, %.2f] for board size %d.' % (args.search, search['N']['min'], search['N']['max'], search['Cp']['min'], search['Cp']['max'], search['size']))

    # Create the randomly sampled configurations
    hyperparameter_configs = [{
        'id': i,
        'search': args.search,
        'N': int(random.uniform(search['N']['min'], search['N']['max'])),
        'Cp': round(random.uniform(search['Cp']['min'], search['Cp']['max']), 4),
        'size': search['size'],
        'trueskill': Rating()
    } for i in range(args.num_configs)]

    pairs = []
    opponents = copy.deepcopy(hyperparameter_configs)
    for player in hyperparameter_configs:
        random.shuffle(opponents)
        for i, opponent in enumerate(opponents):
            if 'num-opponents' in search and i >= search['num-opponents']:
                break
                
            if player != opponent:
                pairs.append((player, opponent))

    # Start the multi-threaded hyperparameter search
    thread_count = min(args.max_threads or (4 * cpu_count()), args.num_configs)
    logger.info('Creating %d threads for parallel search.' % thread_count)

    pool = ThreadPool(thread_count) if os.name == 'nt' else Pool(thread_count)

    completed_pairs = 0
    start_time = time.time()
    print_progressbar(desc='Running hyperparameter search', completed=0, start_time=start_time, total=len(pairs))
    
    for winner, player_id, opponent_id in pool.imap_unordered(run_matchup, pairs):
        completed_pairs += 1
        print_progressbar(desc='Running hyperparameter search', completed=completed_pairs, start_time=start_time, total=len(pairs))
        
        # Calculate new ratings
        r1 = hyperparameter_configs[player_id]['trueskill']
        r2 = hyperparameter_configs[opponent_id]['trueskill']

        if winner == -1:
            r1, r2 = rate_1vs1(r1, r2, drawn=True)
        elif winner == player_id:
            r1, r2 = rate_1vs1(r1, r2, drawn=False)
        elif winner == opponent_id:
            r2, r1 = rate_1vs1(r2, r1, drawn=False)

        hyperparameter_configs[player_id]['trueskill'] = r1
        hyperparameter_configs[opponent_id]['trueskill'] = r2

    # Save the results and plots
    save_results(args.search, hyperparameter_configs)

    logger.info('Finished hyperparameter search of %d randomly sampled configurations.' % args.num_configs)
    logger.info('Saved output/hyperparameter-search_%s.csv' % args.search)

    save_plots(args.search, search)
    
def run_matchup(matchup_input):
    player, opponent = matchup_input

    m1, m2 = MCTS(player['N'], None, player['Cp'], False), MCTS(opponent['N'], None, opponent['Cp'], False)
    r1_color, r2_color = HexBoard.RED, HexBoard.BLUE
    r1_first = bool(random.getrandbits(1))
    
    winner, r1_first = simulate_single_game_winner(player['size'], m1, m2, r1_first, r1_color, r2_color)

    if winner == HexBoard.EMPTY:
        return (-1, player['id'], opponent['id'])
    elif winner == r1_color:
        return (player['id'], player['id'], opponent['id'])
    elif winner == r2_color:
        return (opponent['id'], player['id'], opponent['id'])

def save_results(search_name, hyperparameter_configs):
    save_configuration_result(search_name, ('size', 'N', 'Cp', 'trueskill_mu', 'trueskill'), clear=True)

    for player in hyperparameter_configs:
        save_configuration_result(player['search'], (player['size'], player['N'], player['Cp'], player['trueskill'].mu, player['trueskill'].sigma))
