import unittest
import random
import time

from util.hexboard import HexBoard
from search.minimax import Minimax
from evaluate.dijkstra import Dijkstra
from evaluate.astar import AStar

class TestEval(unittest.TestCase):
    """All unit tests for eval used to determine if the code we wrote is still running as intended"""

    def test_dijkstra(self):
        """First scenario to see if dijkstra returns sane data"""
        dijkstra = Dijkstra()
        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.BLUE
        board.board[(1, 0)] = HexBoard.BLUE

        self.assertEqual(dijkstra.get_score(board, (0,0), [(2,0)], HexBoard.BLUE, HexBoard.RED), 1)

    def test_astar_second_row(self):
        """Another test scenario to see if AStar returns the correct path length"""
        astar = AStar()
        board = HexBoard(4)

        board.board[(1, 0)] = HexBoard.RED
        board.board[(2, 0)] = HexBoard.RED
        board.board[(3, 0)] = HexBoard.RED
        board.board[(0, 2)] = HexBoard.RED

        board.board[(1, 1)] = HexBoard.BLUE
        board.board[(2, 1)] = HexBoard.BLUE
        board.board[(3, 1)] = HexBoard.BLUE

        self.assertEqual(astar.get_score(board, (0, 1), [(3, 1)], HexBoard.BLUE, HexBoard.RED), 1)
        self.assertEqual(astar.get_score(board, (0, 0), [(0, 3)], HexBoard.RED, HexBoard.BLUE), 3)
        self.assertEqual(astar.get_score(board, (3, 0), [(0, 3)], HexBoard.RED, HexBoard.BLUE), 2)

        minimax = Minimax(2, None, astar, False)
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (0, 1))

    def test_board_evaluation(self):
        """Checks to see if the board evaluation returns the expected result in several synthetic board states"""
        dijkstra = Dijkstra()
        board = HexBoard(3)
        
        board.board[(0, 0)] = HexBoard.BLUE
        board.board[(1, 0)] = HexBoard.BLUE

        self.assertTrue(dijkstra.evaluate_board(board, HexBoard.BLUE) > dijkstra.evaluate_board(board, HexBoard.RED))

        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.RED
        board.board[(0, 1)] = HexBoard.RED

        self.assertTrue(dijkstra.evaluate_board(board, HexBoard.RED) > dijkstra.evaluate_board(board, HexBoard.BLUE))

if __name__ == '__main__':
    unittest.main()
