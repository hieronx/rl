import argparse
import sys
import itertools
from tqdm import tqdm
from trueskill import Rating, rate_1vs1
import time
from multiprocessing import Pool, freeze_support

from hexboard import HexBoard
from minimax import Minimax
from evaluate import Evaluate
from game import HexGame

def save_result(start_time, data):
    with open('results/' + start_time + '.csv','a') as fd:
        fd.write(','.join(map(str, data)) + '\n')

def play_game(game_input):
    process_id, board_size, game_cnt, start_time, p1, p2 = game_input

    r1, r2 = Rating(), Rating()
    m1, m2 = Minimax(board_size, p1['depth'], Evaluate(p1['eval']), False), Minimax(board_size, p2['depth'], Evaluate(p2['eval']), False)

    text = "Processor #{}".format(process_id)

    for game_id in tqdm(range(1, game_cnt + 1), desc=text, position=process_id):
        board = HexBoard(board_size)
        first_player, second_player = m1, m2

        while not board.game_over:
            first_player = m2 if first_player == m1 else m1
            second_player = m2 if second_player == m1 else m1

            first_move = first_player.get_next_move(board, HexBoard.RED)
            board.place(first_move, HexBoard.RED)

            if not board.game_over:
                second_move = second_player.get_next_move(board, HexBoard.BLUE)

                if not second_move:
                    board.print()
                else:
                    board.place(second_move, HexBoard.BLUE)
        
        winner = r1 if board.check_win(HexBoard.RED) else r2
        loser = r1 if board.check_win(HexBoard.BLUE) else r2
        drawn = board.check_draw()

        r1, r2 = rate_1vs1(winner, loser, drawn)
        save_result(start_time, (p1['depth'], p1['eval'], p2['depth'], p2['eval'], game_id, r1.mu, r1.sigma, r2.mu, r2.sigma))

    print(r1)
    print(r2)
    

def evaluate():
    freeze_support()  # for Windows support

    board_size = 3
    game_cnt = 100
    # players = [{ 'depth': 3, 'eval': 'random' }, { 'depth': 3, 'eval': 'Dijkstra' }, { 'depth': 4, 'eval': 'Dijkstra' }]
    players = [{ 'depth': 3, 'eval': 'random' }, { 'depth': 3, 'eval': 'Dijkstra' }]

    start_time = str(int(time.time()))
    save_result(start_time, ('p1_depth', 'p1_eval', 'p2_depth', 'p2_eval', 'game_id', 'r1_mu', 'r1_sigma', 'r2_mu', 'r2_sigma'))

    game_inputs = [(process_id, board_size, game_cnt, start_time, p1, p2) for process_id, (p1, p2) in enumerate(itertools.permutations(players, 2))]

    pool = Pool(len(game_inputs))
    pool.map(play_game, game_inputs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Minimax for Hex")
    parser.add_argument('--evaluate', action='store_true', help='If added, evaluate using TrueSkill')
    parser.add_argument('--simulate', action='store_true', help='If added, simulates both sides')
    parser.add_argument('--size', type=int, default=4, help='Set the board size')
    parser.add_argument('--depth', type=int, default=3, help='Set the search depth')
    parser.add_argument('--eval', choices=['Dijkstra', 'random'], default='Dijkstra', help='Choose the evaluation method')
    args = parser.parse_args(sys.argv[1:])

    game = HexGame(args.size, args.depth, args.eval)
    board = HexBoard(args.size)

    if args.evaluate:
        evaluate()  
    elif args.simulate:
        game.simulate(board)
    else:
        game.run_interactively(board)
