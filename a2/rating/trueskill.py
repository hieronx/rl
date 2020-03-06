from trueskill import Rating, rate_1vs1
from multiprocessing import Pool, freeze_support
import logging

from util import progressbar
from util.hexboard import HexBoard
from search.minimax import Minimax
from rating.configs import configs
from rating.export import save_result, save_plots

from evaluate.dijkstra import Dijkstra
from evaluate.astar import AStar
from evaluate.random import RandomEval

logger = logging.getLogger(__name__)

def get_eval_class(eval_method):
    if eval_method == 'Dijkstra':
        return Dijkstra()
    elif eval_method == 'AStar':
        return AStar()
    elif eval_method == 'random':
        return RandomEval()

def run_trueskill(args):
    """Surprise, starts a trueskill comparison for each of the possible permutations of the input players, using multi-threading"""
    freeze_support() # for Windows support

    config = configs[args.config]

    player_permutations = []
    for i in range(len(config['players'])):
        for j in range(i + 1, len(config['players'])):
            player_permutations.append((config['players'][i], config['players'][j]))

    save_result(args.config, ('p1_search', 'p1_depth', 'p1_time_limit', 'p1_eval', 'p2_search', 'p2_depth', 'p2_time_limit', 'p2_eval', 'game_id', 'r1_mu', 'r1_sigma', 'r2_mu', 'r2_sigma'), clear=True)
    
    game_inputs = [(process_id, config['board_size'], config['game_count'], args.config, p1, p2, args.disable_tt) for process_id, (p1, p2) in enumerate(player_permutations)]

    pool = Pool(len(game_inputs))
    pool.map(play_game, game_inputs)

    fn = 'output/%s.csv' % args.config
    logger.info('Saved %s' % fn)

    if args.plot:
        save_plots(args, player_permutations)

def play_game(game_input):
    """Plays a series of games according to the provided game input object which packs all the settings into one object"""
    process_id, board_size, game_cnt, config, p1, p2, disable_tt = game_input

    r1 = Rating()
    r2 = Rating()
    r1_col, r2_col = HexBoard.RED, HexBoard.BLUE
    r1_first = True

    for game_id in progressbar(range(1, game_cnt + 1), desc="Processor %d" % (process_id + 1), position=process_id):
        m1, m2 = Minimax(board_size, p1['depth'], p1['time_limit'], get_eval_class(p1['eval']), False, disable_tt=disable_tt), Minimax(board_size, p2['depth'], p2['time_limit'], get_eval_class(p2['eval']), False, disable_tt=disable_tt)
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
        
        save_result(config, (p1['search'], p1['depth'], p1['time_limit'], p1['eval'], p2['search'], p2['depth'], p2['time_limit'], p2['eval'], game_id, r1.mu, r1.sigma, r2.mu, r2.sigma))
        
    logger.info('[p1=%s] %s' % (p1['eval'], r1))
    logger.info('[p2=%s] %s' % (p2['eval'], r2))