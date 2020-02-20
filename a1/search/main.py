import argparse
import sys
import itertools
from tqdm import tqdm
from trueskill import Rating, rate_1vs1

from hexboard import HexBoard
from minimax import Minimax
from evaluate import Evaluate
from game import HexGame

def evaluate():
    board_size = 2
    game_cnt = 100
    players = [{ 'depth': 3, 'eval': 'random' }, { 'depth': 3, 'eval': 'Dijkstra' }, { 'depth': 4, 'eval': 'Dijkstra' }]

    for p1, p2 in itertools.permutations(players, 2):
        print('Playing search depth %d and %s evaluation against search depth %d and %s evaluation...' % (p1['depth'], p1['eval'], p2['depth'], p2['eval']))

        r1, r2 = Rating(), Rating()
        m1, m2 = Minimax(board_size, p1['depth'], Evaluate(p1['eval']), False), Minimax(board_size, p2['depth'], Evaluate(p2['eval']), False)

        for _ in tqdm(range(game_cnt)):
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
        
        print(r1)
        print(r2)

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
