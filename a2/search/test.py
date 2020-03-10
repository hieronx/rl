import unittest
import random
import time

from util.hexboard import HexBoard
from search.minimax import Minimax
from search.mcts import MCTS
from evaluate.dijkstra import Dijkstra
from evaluate.astar import AStar

class TestSearch(unittest.TestCase):
    """All unit tests for search used to determine if the code we wrote is still running as intended"""

    def test_minimax(self):
        """"Tests to see if Minimax returns the expected best moves for specific board states"""
        dijkstra = Dijkstra()
        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.RED
        board.board[(0, 1)] = HexBoard.RED

        self.assertFalse(board.game_over())

        minimax = Minimax(3, 3, None, dijkstra, False)
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (0, 2))

    def test_mcts(self):
        """"Tests to see if MCTS returns the expected best moves for specific board states"""
        dijkstra = Dijkstra()
        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.RED
        board.board[(0, 1)] = HexBoard.RED

        self.assertFalse(board.game_over())

        mcts = MCTS(500, 0.5, dijkstra, False)
        move = mcts.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (0, 2))

    def test_simulate(self):
        """Tests the board simulation function. Since this is random playout we can't be sure of the result"""
        dijkstra = Dijkstra()
        board = HexBoard(3)
        
        mcts = MCTS(3, 0.5, dijkstra, False)
        simulate_result = mcts.simulate(board, HexBoard.RED, HexBoard.BLUE)
        
        self.assertTrue(simulate_result >= 0.0 and simulate_result <= 1.0)

    def test_minimax_top_left(self):
        """"Another scenario which tests a specific minimax scenario"""
        dijkstra = Dijkstra()
        board = HexBoard(4)

        board.board[(1, 0)] = HexBoard.RED
        board.board[(1, 1)] = HexBoard.RED
        board.board[(1, 2)] = HexBoard.RED
        board.board[(0, 1)] = HexBoard.BLUE
        board.board[(0, 2)] = HexBoard.BLUE
        board.board[(0, 3)] = HexBoard.BLUE

        good_board = board.make_move((1, 3), HexBoard.RED)
        eval_good_board = dijkstra.evaluate_board(good_board, HexBoard.RED)

        bad_board = board.make_move((0, 0), HexBoard.RED)
        eval_bad_board = dijkstra.evaluate_board(bad_board, HexBoard.RED)

        self.assertTrue(eval_good_board > eval_bad_board)

        minimax = Minimax(4, 3, None, dijkstra, False)
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (1, 3))

    def test_tp_table(self):
        """Tests if the transposition table is working as intended"""
        dijkstra = Dijkstra()
        board = HexBoard(3)
        minimax = Minimax(3, 3, None, dijkstra, False)

        board.board[(0, 0)] = HexBoard.RED
        board.board[(0, 1)] = HexBoard.RED
        self.assertEqual(minimax.tp_table, {})
        
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertTrue(len(minimax.tp_table) > 0)
    
if __name__ == '__main__':
    unittest.main()
