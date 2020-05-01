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

        board.place((0, 0), HexBoard.RED)
        board.place((0, 1), HexBoard.RED)

        self.assertEquals(board.get_winner(), None)

        minimax = Minimax(3, None, dijkstra, False)
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (0, 2))

    def test_mcts(self):
        """"Tests to see if MCTS returns the expected best moves for specific board states"""
        board = HexBoard(4)

        board.place((2, 0), HexBoard.RED)
        board.place((1, 1), HexBoard.BLUE)

        self.assertEquals(board.get_winner(), None)

        mcts = MCTS(10000, None, 0.4, False, rave_k=5000, debug=True)
        move = mcts.get_next_move(board, HexBoard.RED)
        new_board = board.make_move(move, HexBoard.RED)
        self.assertEqual(move, (2, 1))
        
    def test_minimax_top_left(self):
        """"Another scenario which tests a specific minimax scenario"""
        dijkstra = Dijkstra()
        board = HexBoard(4)

        board.place((1, 0), HexBoard.RED)
        board.place((1, 1), HexBoard.RED)
        board.place((1, 2), HexBoard.RED)
        board.place((0, 1), HexBoard.BLUE)
        board.place((0, 2), HexBoard.BLUE)
        board.place((0, 3), HexBoard.BLUE)

        minimax = Minimax(3, None, dijkstra, False)
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (1, 3))

    def test_mcts_top_left(self):
        """"Another scenario which tests a specific MCTS scenario"""
        board = HexBoard(4)

        board.place((1, 0), HexBoard.RED)
        board.place((1, 1), HexBoard.RED)
        board.place((1, 2), HexBoard.RED)
        board.place((0, 1), HexBoard.BLUE)
        board.place((0, 2), HexBoard.BLUE)
        board.place((0, 3), HexBoard.BLUE)

        mcts = MCTS(5000, None, 0.4, False)
        move = mcts.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (1, 3))

    def test_tp_table(self):
        """Tests if the transposition table is working as intended"""
        dijkstra = Dijkstra()
        board = HexBoard(3)
        minimax = Minimax(3, None, dijkstra, False)

        board.place((0, 0), HexBoard.RED)
        board.place((0, 1), HexBoard.RED)
        self.assertEqual(minimax.tp_table, {})
        
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertTrue(len(minimax.tp_table) > 0)
    
if __name__ == '__main__':
    unittest.main()
