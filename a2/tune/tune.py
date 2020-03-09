import logging
import random
from multiprocessing import Pool, freeze_support
from trueskill import Rating, rate_1vs1

from util.hexboard import HexBoard
from search.minimax import Minimax
from search.mcts import MCTS
from rating.configs import configs
from evaluate.dijkstra import Dijkstra
from util import progressbar

from tune.export import save_configuration_result

logger = logging.getLogger(__name__)

# Inspiration: https://arxiv.org/pdf/1903.08129.pdf and https://arxiv.org/pdf/1812.06855.pdf

def run_hyperparameter_search(args):
    freeze_support() # for Windows support

    N_min, N_max = 5, 50
    Cp_min, Cp_max = 0.5, 2.0

    hyperparameter_configs = []
    for i in range(args.num_configs):
        N = random.uniform(N_min, N_max)
        Cp = random.uniform(Cp_min, Cp_max)
        hyperparameter_configs.append((i, N, Cp, args.num_games, args.size))

    save_configuration_result(('N', 'Cp', 'num_games', 'baseline_mu', 'baseline_sigma', 'config_mu', 'config_sigma'), clear=True)

    pool = Pool()
    pool.map(test_configuration, hyperparameter_configs)

    logger.info('Finished hyperparameter search.')

# TODO: most of this code is duplicated from the rating module,
# so it should be refactored into a separate calculate_ratings() method.
def test_configuration(config_input):
    process_id, N, Cp, num_games, board_size = config_input

    baseline = Minimax(board_size, None, 0.1, Dijkstra(), False, False)

    r1 = Rating()
    r2 = Rating()
    r1_col, r2_col = HexBoard.RED, HexBoard.BLUE
    r1_first = True

    for game_id in progressbar(range(1, num_games + 1), desc='N=%.2f, Cp=%.2f' % (N, Cp), position=process_id):
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