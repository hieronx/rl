import argparse
import sys
import numpy as np
import math

from util import cls
from hexboard import HexBoard

char_to_row_idx = {'a': 0, 'b': 1, 'c': 2, 'd': 3}


class HexMinimax:

    def __init__(self, size, depth, eval_method):
        self.board_size = size
        self.search_depth = depth
        self.eval_method = eval_method

    def run_interactively(self, board):
        while not board.game_over:
            print("Waiting for CPU move...")
            move = self.get_next_move(board, self.search_depth, HexBoard.RED)
            board.place(move, HexBoard.RED)
            board.print()
            print('\n')

            while True:
                move = input("Your move: ")

                if len(move) == 2:
                    x, y = move
                    if (x in char_to_row_idx and y.isdigit):
                        if board.is_empty((char_to_row_idx[x], int(y))):
                            break

            board.place((char_to_row_idx[x], int(y)), HexBoard.BLUE)

        if board.check_win(HexBoard.RED):
            print('The AI won.')
        else:
            print('You won.')

    def simulate(self, board):
        while not board.game_over:
            board.place(self.get_next_move(board, self.search_depth), HexBoard.RED)
            board.place(self.get_next_move(board, self.search_depth), HexBoard.BLUE)

        if board.check_win(HexBoard.RED):
            print('Red won.')
        else:
            print('Blue won.')

        board.print()

    def alpha_beta_search(self, board, depth, color, lower_bound_a, upper_bound_b, maximizing = True):
        if depth == 0:
            return (None, self.evaluate_board(board, color), 1, 0)

        moves = self.get_possible_moves(board)

        best_score = math.inf if not maximizing else -math.inf
        best_move = None
        total_nodes_searched = 0
        total_cutoffs = 0
        for move in moves:
            new_board = board.make_move(move, color)
            _, score, nodes_searched, cutoffs = self.alpha_beta_search(new_board, depth - 1, board.get_opposite_color(color), lower_bound_a, upper_bound_b, not maximizing)
            total_nodes_searched += nodes_searched
            total_cutoffs += cutoffs

            
            if maximizing and score > best_score:
                best_move = move
                best_score = score
                
                if score >= lower_bound_a:
                    lower_bound_a = score

                    if lower_bound_a >= upper_bound_b:
                        return (best_move, best_score, total_nodes_searched, 1)

            elif not maximizing and score < best_score:
                best_move = move
                best_score = score

                if score <= upper_bound_b:
                    upper_bound_b = score
                    
                    if upper_bound_b <= lower_bound_a:
                        return (best_move, best_score, total_nodes_searched, 1)

        return (best_move, best_score, total_nodes_searched, total_cutoffs)


    def get_next_move(self, board, depth, color):
        lower_bound_a = -math.inf
        upper_bound_b = math.inf
        
        move, _, nodes_searched, cutoffs = self.alpha_beta_search(board, depth, color, lower_bound_a, upper_bound_b, True)
        cls()
        print("Searched %d nodes and experienced %d cutoffs" % (nodes_searched, cutoffs))
        return move

    def get_possible_moves(self, board):
        empty_coordinates = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board.is_empty((x, y)):
                    empty_coordinates.append((x, y))

        return empty_coordinates

    def evaluate_board(self, board, color):
        # TODO: implement Dijkstra
        # For each color
        #   source_positions = positions of color on the source border
        #   paths = [find_shortest_path_to_border(board, color, position_source_border) for position in source_positions]
        #   shortest_path =  min(paths)
        # return shortest_path_red - shortest_path_blue
        if self.eval_method == 'dijkstra':
            return np.random.uniform(0, 1)
        else:
            return np.random.uniform(0, 1)

    def find_shortest_path_to_border(self, board, color, from_coordinate):
        # Only count nodes without placed positions of this color
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Minimax for Hex")
    parser.add_argument('--simulate', action='store_true',
                        help='If added, simulates both sides')
    parser.add_argument('--size', type=int, default=4,
                        help='Set the board size')
    parser.add_argument('--depth', type=int, default=3,
                        help='Set the search depth')
    parser.add_argument('--eval', choices=['dijkstra', 'random'],
                        default='dijkstra', help='Choose the evaluation method')
    args = parser.parse_args(sys.argv[1:])

    hex_minimax = HexMinimax(args.size, args.depth, args.eval)
    board = HexBoard(args.size)

    if args.simulate:
        hex_minimax.simulate(board)
    else:
        hex_minimax.run_interactively(board)
