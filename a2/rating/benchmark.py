import unittest
import time
from tqdm import tqdm
import statistics

from util.hexboard import HexBoard
from search.minimax import Minimax
from evaluate.dijkstra import Dijkstra

def run_benchmark():
    """Runs a certain amount of games to test performance. Afterwards the results will be printed"""
    game_count = 100
    game_times = []

    for i in tqdm(range(game_count)):
        start_time = time.time()

        board_size = 3
        board = HexBoard(board_size)

        evaluate = Dijkstra()
        minimax = Minimax(board_size, 3, None, evaluate, False)

        next_color = HexBoard.RED
        while not board.game_over():
            board.board[minimax.get_next_move(board, next_color)] = next_color
            next_color = HexBoard.BLUE if next_color == HexBoard.RED else HexBoard.RED
        
        game_times.append(time.time() - start_time)
    
    print('Benchmark %d games, mean=%.3fs, std-dev=%.5fs' % (game_count, statistics.mean(game_times), statistics.stdev(game_times)))
