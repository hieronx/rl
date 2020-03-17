from trueskill import Rating, rate_1vs1
from multiprocessing import Pool, freeze_support, cpu_count
from multiprocessing.pool import ThreadPool
import os, time, logging, itertools, random

from util import print_progressbar
from util.hexboard import HexBoard
from rating.configs import configs
from rating.export import save_result, save_plots
from rating.simulate import simulate_single_game_winner
from . import get_search_class

logger = logging.getLogger(__name__)

def run_trueskill(args):
    """Surprise, starts a trueskill comparison for each of the possible permutations of the input players, using multi-threading"""
    freeze_support()

    # Load the TrueSkill config to evaluate
    config = configs[args.config]

    # Create all possible unique permutations of the players in the config
    unique_permutations = []
    for i in range(len(config['players'])):
        for j in range(i + 1, len(config['players'])):
            unique_permutations.append((i, j, config['players'][i], config['players'][j]))
    
    # Repeat every permutation game_count times
    permutations = list(itertools.chain.from_iterable(itertools.repeat(x, config['game_count']) for x in unique_permutations))

    # Create inputs and default ratings
    game_inputs = [(config['board_size'], config['game_count'], args.config, p1_id, p2_id, p1, p2, args.disable_tt) for (p1_id, p2_id, p1, p2) in permutations]
    ratings = { player_id: Rating() for player_id in range(len((config['players']))) }

    save_result(args.config, ('p1', 'p2', 'game_id', 'r1_mu', 'r1_sigma', 'r2_mu', 'r2_sigma'), clear=True)
    
    # Start multi-threaded evaluation
    thread_count = min(args.max_threads or (1 * cpu_count()), len(game_inputs))
    logger.info('Creating %d threads for parallel search.' % thread_count)

    pool = ThreadPool(thread_count) if os.name == 'nt' else Pool(thread_count)
    completed_permutations = 0
    start_time = time.time()
    print_progressbar(desc='Running hyperparameter search', completed=0, start_time=start_time, total=len(game_inputs))

    for winner, player_id, opponent_id in pool.imap(play_game, game_inputs):
        completed_permutations += 1
        print_progressbar(desc='Running hyperparameter search', completed=completed_permutations, start_time=start_time, total=len(game_inputs))

        # Calculate new ratings
        r1 = ratings[player_id]
        r2 = ratings[opponent_id]

        if winner == -1:
            r1, r2 = rate_1vs1(r1, r2, drawn=True)
        elif winner == player_id:
            r1, r2 = rate_1vs1(r1, r2, drawn=False)
        elif winner == opponent_id:
            r2, r1 = rate_1vs1(r2, r1, drawn=False)

        ratings[player_id] = r1
        ratings[opponent_id] = r2

        m1, m2 = get_search_class(config['players'][player_id], args.disable_tt), get_search_class(config['players'][opponent_id], args.disable_tt)
        save_result(args.config, (str(m1), str(m2), completed_permutations, r1.mu, r1.sigma, r2.mu, r2.sigma))

    fn = 'output/%s.csv' % args.config
    logger.info('Saved %s' % fn)

    if args.plot:
        save_plots(args, unique_permutations)

def play_game(game_input):
    """Plays a series of games according to the provided game input object which packs all the settings into one object"""
    board_size, game_cnt, config, p1_id, p2_id, p1, p2, disable_tt = game_input

    m1, m2 = get_search_class(p1, disable_tt), get_search_class(p2, disable_tt)
    r1_color, r2_color = HexBoard.RED, HexBoard.BLUE
    r1_first = bool(random.getrandbits(1))
    
    winner, r1_first = simulate_single_game_winner(board_size, m1, m2, r1_first, r1_color, r2_color)

    if winner == HexBoard.EMPTY:
        return (-1, p1_id, p2_id)
    elif winner == r1_color:
        return (p1_id, p1_id, p2_id)
    elif winner == r2_color:
        return (p2_id, p1_id, p2_id)
