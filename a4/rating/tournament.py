import copy
import logging
import os
import random
import time
from multiprocessing import Array, Pool, Value, cpu_count, freeze_support
from multiprocessing.pool import ThreadPool

from trueskill import Rating, rate_1vs1

from rating.simulate import simulate_single_game_winner
from util import print_progressbar
from util.hexboard import HexBoard

from . import get_search_class

logger = logging.getLogger(__name__)

board_size = 7

def run_tournament(args):
    freeze_support()

    players = [
        { 'id': 'alphazero-50it-1', 'search': 'alphazero', 'model_path': 'alphazero/tests/50iterations_1.pt', 'name': 'AlphaZero, 50 iterations (1)' },
        { 'id': 'alphazero-50-after-fix', 'search': 'alphazero', 'model_path': 'alphazero/tests/50iterations_bugfixed.pt', 'name': 'AlphaZero, 50 bugfixed' },
        { 'id': 'alphazero-147it', 'search': 'alphazero', 'model_path': 'alphazero/tests/147it.pt', 'name': 'AlphaZero, 147 iterations' },
        { 'id': 'alphazero-random', 'search': 'alphazero', 'model_path': 'alphazero/tests/random.pt', 'name': 'AlphaZero, random weights' },
        { 'id': 'alphazero-random-2', 'search': 'alphazero', 'model_path': 'alphazero/tests/random2.pt', 'name': 'AlphaZero, random weights, v2' },
    ]
    # { 'id': 'minimax', 'search': 'minimax', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
    # { 'id': 'mcts', 'search': 'mcts', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },

    pairs = []
    opponents = copy.deepcopy(players)
    for player in players:
        random.shuffle(opponents)
        for i, opponent in enumerate(opponents):
            if player != opponent:
                pairs.append((player, opponent))
    
    results = {}
    for player in players:
        results[player['id']] = Rating()
    
    pairs = pairs

    # Start the multi-threaded hyperparameter search
    thread_count = args.max_threads or cpu_count()
    logger.info('Creating %d threads for parallel search.' % thread_count)

    pool = ThreadPool(thread_count) if os.name == 'nt' else Pool(thread_count)
    
    max_sigma = max(results[r].sigma for r in results)
    i = 1
    args.sigma_threshold = 0.85
    while max_sigma > args.sigma_threshold:
        print('Max sigma %.2f > %.2f.' % (max_sigma, args.sigma_threshold))

        completed_pairs = 0
        start_time = time.time()
        print_progressbar(desc='Running tournament', completed=0, start_time=start_time, total=len(pairs))
        
        for winner, player_id, opponent_id in pool.imap_unordered(run_matchup, pairs):
            completed_pairs += 1
            print_progressbar(desc='Running tournament', completed=completed_pairs, start_time=start_time, total=len(pairs))
            
            # Calculate new ratings
            r1 = results[player_id]
            r2 = results[opponent_id]

            if winner == -1:
                r1, r2 = rate_1vs1(r1, r2, drawn=True)
            elif winner == player_id:
                r1, r2 = rate_1vs1(r1, r2, drawn=False)
            elif winner == opponent_id:
                r2, r1 = rate_1vs1(r2, r1, drawn=False)

            results[player_id] = r1
            results[opponent_id] = r2
            
        max_sigma = max(results[r].sigma for r in results)
        i += 1

        print()
        for player_id in results:
            print('%s: μ = %.2f, σ = %.2f' % (player_id, results[player_id].mu, results[player_id].sigma))
    
    print()
    for player_id in results:
        print('%s: μ = %.2f, σ = %.2f' % (player_id, results[player_id].mu, results[player_id].sigma))

def run_matchup(matchup_input):
    """Runs a single matchup and updates the winner accordingly"""
    player, opponent = matchup_input

    m1, m2 = get_search_class(player, board_size=board_size), get_search_class(opponent, board_size=board_size)
    r1_color, r2_color = HexBoard.RED, HexBoard.BLUE
    r1_first = bool(random.getrandbits(1))
    
    winner, r1_first = simulate_single_game_winner(board_size, m1, m2, r1_first, r1_color, r2_color)

    if winner == HexBoard.EMPTY:
        return (-1, player['id'], opponent['id'])
    elif winner == r1_color:
        return (player['id'], player['id'], opponent['id'])
    elif winner == r2_color:
        return (opponent['id'], player['id'], opponent['id'])
