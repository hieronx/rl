from trueskill import Rating, rate_1vs1
from multiprocessing import Pool, freeze_support
from copy import deepcopy
import time
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
import logging

from util import progressbar
from util.hexboard import HexBoard
from search.minimax import Minimax

from evaluate.dijkstra import Dijkstra
from evaluate.astar import AStar
from evaluate.random import Random

logger = logging.getLogger(__name__)

def get_eval_class(eval_method):
    if eval_method == 'Dijkstra':
        return Dijkstra()
    elif eval_method == 'AStar':
        return AStar()
    elif eval_method == 'random':
        return Random()

def run_trueskill(args):
    """Surprise, starts a trueskill comparison for each of the possible permutations of the input players, using multi-threading"""
    freeze_support() # for Windows support

    if args.config == 'random-vs-Dijkstra':
        board_size = 4
        game_cnt = 200

        players = [
            { 'depth': 3, 'time_limit': None, 'eval': 'random' },
            { 'depth': 3, 'time_limit': None, 'eval': 'Dijkstra' },
            { 'depth': 4, 'time_limit': None, 'eval': 'Dijkstra' },
        ]
    elif args.config == 'depth-vs-time-limit':
        board_size = 4
        game_cnt = 200

        players = [
            { 'depth': 3, 'time_limit': None, 'eval': 'Dijkstra' },
            { 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra' },
            { 'depth': None, 'time_limit': 1.0, 'eval': 'Dijkstra' },
        ]
    elif args.config == 'Minimax-vs-MCTS':
        board_size = 3
        game_cnt = 5

        players = [
            { 'depth': None, 'time_limit': 0.1, 'search': 'Minimax', 'eval': 'Dijkstra' },
            { 'depth': None, 'time_limit': 0.1, 'search': 'MCTS', 'eval': 'Dijkstra' },
        ]
    elif args.config == 'Dijkstra-performance':
        board_size = 3
        game_cnt = 200

        players = [{ 'depth': 3, 'time_limit': None, 'eval': 'random' }, { 'depth': 3, 'time_limit': None, 'eval': 'Dijkstra' }]

    player_permutations = []
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            player_permutations.append((players[i], players[j]))

    save_result(args.config, ('p1_search', 'p1_depth', 'p1_time_limit', 'p1_eval', 'p2_search', 'p2_depth', 'p2_time_limit', 'p2_eval', 'game_id', 'r1_mu', 'r1_sigma', 'r2_mu', 'r2_sigma'), clear=True)

    game_inputs = [(process_id, board_size, game_cnt, args.config, p1, p2, args.disable_tt) for process_id, (p1, p2) in enumerate(player_permutations)]

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

    # text = "Processor %d" % (process_id)

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
        
    # logger.info('[p1=%s] %s' % (p1['eval'], r1))
    # logger.info('[p2=%s] %s' % (p2['eval'], r2))

def save_result(config, data, clear=False):
    """Saves the provided data to the disk using the provided start_time as .csv"""
    if not os.path.exists('output'): os.makedirs('output')

    fn = 'output/%s.csv' % config
    if clear and os.path.isfile(fn): os.remove(fn)

    with open(fn,'a') as fd:
        fd.write(','.join(map(str, data)) + '\n')

def save_plots(args, player_permutations):
    """Saves the plots that were generated from the player permutations to the disk using the timestamp as part of the filename"""
    df = pd.read_csv("output/" + args.config + ".csv", index_col=None, header=0)
    if not os.path.exists('output'): os.makedirs('output')

    for i, (p1, p2) in enumerate(player_permutations):
        games = df[(df['p1_search'] == p1['search']) & (df['p1_depth'].astype(str) == str(p1['depth'])) & (df['p1_eval'] == p1['eval']) & (df['p1_time_limit'].astype(str) == str(p1['time_limit']))
                & (df['p2_search'] == p2['search']) & (df['p2_depth'].astype(str) == str(p2['depth'])) & (df['p2_time_limit'].astype(str) == str(p2['time_limit'])) & (df['p2_eval'] == p2['eval'])] 
       
        ax = games.plot(x='game_id', y=['r1_mu', 'r2_mu'], figsize=(8,5), grid=True)
        
        ax.set_xlabel("Number of games")
        ax.set_ylabel("TrueSkill μ-value")
        
        p1_name = p1['search'] + ', ' + p1['eval'] + (" (depth " + str(p1['depth']) + ")" if p1['depth'] is not None else " (time limit " + str(p1['time_limit']) + "s)")
        p2_name = p2['search'] + ', ' + p2['eval'] + (" (depth " + str(p2['depth']) + ")" if p2['depth'] is not None else " (time limit " + str(p2['time_limit']) + "s)")
        ax.legend([p1_name, p2_name]);
        
        fn = 'output/%s_%s.png' % (args.config, i+1)
        ax.get_figure().savefig(fn)
        logger.info('Saved %s' % fn)