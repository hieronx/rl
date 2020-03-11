from trueskill import Rating, rate_1vs1
from multiprocessing import Pool, freeze_support, cpu_count
import logging

from util import progressbar
from util.hexboard import HexBoard
from rating.configs import configs
from rating.export import save_result, save_plots
from rating.simulate import simulate_single_game
from . import get_search_class

logger = logging.getLogger(__name__)

def run_trueskill(args):
    """Surprise, starts a trueskill comparison for each of the possible permutations of the input players, using multi-threading"""
    freeze_support()

    # Load the TrueSkill config to evaluate
    config = configs[args.config]

    # Create all possible unique permutations of the players in the config
    player_permutations = []
    for i in range(len(config['players'])):
        for j in range(i + 1, len(config['players'])):
            player_permutations.append((config['players'][i], config['players'][j]))

    game_inputs = [(process_id, config['board_size'], config['game_count'], args.config, p1, p2, args.disable_tt) for process_id, (p1, p2) in enumerate(player_permutations)]

    save_result(args.config, ('p1_search', 'p1_depth', 'p1_time_limit', 'p1_eval', 'p2_search', 'p2_depth', 'p2_time_limit', 'p2_eval', 'game_id', 'r1_mu', 'r1_sigma', 'r2_mu', 'r2_sigma'), clear=True)
    
    # Start multi-threaded evaluation
    thread_count = min(args.max_threads or (4 * cpu_count()), len(game_inputs))
    logger.info('Creating %d threads for parallel search.' % thread_count)

    pool = Pool(thread_count)
    pool.map(play_game, game_inputs)

    # Save output and plots
    fn = 'output/%s.csv' % args.config
    logger.info('Saved %s' % fn)

    if args.plot:
        save_plots(args, player_permutations)

def play_game(game_input):
    """Plays a series of games according to the provided game input object which packs all the settings into one object"""
    process_id, board_size, game_cnt, config, p1, p2, disable_tt = game_input

    r1 = Rating()
    r2 = Rating()
    r1_color, r2_color = HexBoard.RED, HexBoard.BLUE
    r1_first = True

    for game_id in progressbar(range(1, game_cnt + 1), desc="Processor %d" % (process_id + 1), position=process_id):
        m1, m2 = get_search_class(p1, disable_tt), get_search_class(p2, disable_tt)
        r1, r2, r1_first = simulate_single_game(board_size, r1, r2, m1, m2, r1_first, r1_color, r2_color)
        save_result(config, (p1['search'], p1['depth'], p1['time_limit'], p1['eval'], p2['search'], p2['depth'], p2['time_limit'], p2['eval'], game_id, r1.mu, r1.sigma, r2.mu, r2.sigma))
        
    logger.info('[p1=%s] %s' % (p1['eval'], r1))
    logger.info('[p2=%s] %s' % (p2['eval'], r2))