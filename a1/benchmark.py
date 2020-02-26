import unittest
import numpy as np
import time
from tqdm import tqdm

from hexboard import HexBoard
from minimax import Minimax
from evaluate import Evaluate

class BenchmarkHexMinimax(unittest.TestCase):
    """Contains the benchmarking code to test efficiency of different algorithmic implementations"""

    def test_games(self):
        """Runs a certain amount of games to test performance. Afterwards the results will be printed"""
        game_count = 100
        game_times = []

        for i in tqdm(range(game_count)):
            start_time = time.time()

            board_size = 3
            board = HexBoard(board_size)

            evaluate = Evaluate('Dijkstra')
            minimax = Minimax(board_size, 3, None, evaluate, False)

            next_color = HexBoard.RED
            while not board.game_over():
                board.place(minimax.get_next_move(board, next_color), next_color)
                next_color = HexBoard.BLUE if next_color == HexBoard.RED else HexBoard.RED
            
            game_times.append(time.time() - start_time)
        
        print('Benchmark %d games, mean=%.3fs, std-dev=%.5fs' % (game_count, np.mean(game_times, axis=0), np.std(game_times, axis=0)))


if __name__ == '__main__':
    unittest.main()
